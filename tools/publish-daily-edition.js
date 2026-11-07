#!/usr/bin/env node
'use strict';
// Runs on the static host, never in a visitor request. The server document root
// points at <state>/current; only a fully built release becomes that symlink.
const fs=require('fs');
const path=require('path');
const crypto=require('crypto');
const {execFileSync}=require('child_process');
const {refresh,read}=require('./daily/cache');
const {cairoDay,MEDIA}=require('./daily/schema');
const ROOT=path.resolve(__dirname,'..');
const STATE=path.resolve(process.env.LANDING_STATE_DIR||path.join(ROOT,'.daily-releases'));
const routes=JSON.parse(fs.readFileSync(path.join(ROOT,'tools/routes.json'))).routes;
// Copy everything the checkout used to serve directly, so switching the
// document root to a release never drops a page (privacy.html, verification
// files, …). Only private build state and VCS data stay out.
const PRIVATE=new Set(['.git','node_modules','.cache','.daily-releases','.daily-current','.artifacts','.impeccable','.publish-lock']);
function copyPublic(destination) {
  for(const name of fs.readdirSync(ROOT)) {
    if(PRIVATE.has(name)) continue;
    const source=path.join(ROOT,name);
    if(fs.lstatSync(source).isSymbolicLink()) continue;
    fs.cpSync(source,path.join(destination,name),{recursive:true,filter:p=>!p.startsWith(path.join(ROOT,'assets','daily')+path.sep) && !fs.lstatSync(p).isSymbolicLink()});
  }
}
// A code deploy (git pull) must reach visitors even when the edition is unchanged.
function sourceRevision() {
  try { return execFileSync('git',['-C',ROOT,'rev-parse','HEAD'],{stdio:['ignore','pipe','ignore']}).toString().trim(); }
  catch { return 'nogit'; }
}
async function publish() {
  fs.mkdirSync(STATE,{recursive:true});
  const lock=path.join(STATE,'.publish-lock');let fd;
  try{fd=fs.openSync(lock,'wx');}catch(e){if(e.code==='EEXIST') throw new Error('Another daily publication is running; inspect the lock if its process ended');throw e;}
  let stage;
  try {
    const cacheDir=path.join(STATE,'cache'),assetDir=path.join(STATE,'media');
    let result;
    try { result=await refresh({cacheDir,assetDir,...(process.argv.includes('--local')?{endpoint:'http://127.0.0.1:81/api/public/landing-content',allowLocal:true}:{})}); }
    catch(e){result={data:read(cacheDir),status:'unavailable',warning:e.message};}
    const day=cairoDay(),edition=result.data;
    const signature=(edition?.revision||'unavailable')+':'+day+':'+sourceRevision();
    const current=path.join(STATE,'current');
    let prior;
    try{prior=JSON.parse(fs.readFileSync(path.join(current,'edition.json'),'utf8'));}catch{}
    if(prior?.signature===signature && !process.argv.includes('--rebuild')) {console.log(JSON.stringify({status:'unchanged',date:edition?.snapshot_date||null,warning:result.warning}));return;}
    stage=path.join(STATE,'release-'+day+'-'+crypto.randomBytes(5).toString('hex'));
    fs.mkdirSync(stage);copyPublic(stage);
    if(edition) {
      fs.mkdirSync(path.join(stage,'assets/daily'),{recursive:true});
      for(const item of [...edition.projects.map(r=>r.image),...edition.developers.map(r=>r.logo)].filter(Boolean)) {
        const name=MEDIA.exec(item)[1]+'.webp';
        fs.copyFileSync(path.join(assetDir,name),path.join(stage,'assets/daily',name));
      }
    }
    execFileSync(process.execPath,[path.join(ROOT,'tools/build-pages.js')],{cwd:ROOT,env:{...process.env,LANDING_OUTPUT_DIR:stage,LANDING_CACHE_DIR:cacheDir},stdio:'pipe'});
    // Every current page must be from one edition, with local media present.
    for(const r of routes) for(const lang of ['ar','en']) {
      const file=path.join(stage,r.path,lang==='ar'?'index.html':'en.html');
      const html=fs.readFileSync(file,'utf8');
      if(!html.includes('name="estavo-content-mode" content="approved-examples"')) throw new Error('Incomplete page edition: '+r.key);
      for(const m of html.matchAll(/src="([^"<>]*assets\/daily\/[^"<>]+)"/g)) if(!fs.existsSync(path.resolve(path.dirname(file),m[1]))) throw new Error('Missing daily image');
    }
    fs.writeFileSync(path.join(stage,'edition.json'),JSON.stringify({signature,date:edition?.snapshot_date||null,status:result.status,built_at:new Date().toISOString()}));
    const next=path.join(STATE,'current.next');
    try { fs.unlinkSync(next); } catch(e) { if(e.code!=='ENOENT') throw e; }
    fs.symlinkSync(stage,next,'dir');fs.renameSync(next,current);
    // Keep the two previous releases for rollback; never retain a public archive.
    const releases=fs.readdirSync(STATE).filter(n=>/^release-\d{4}-\d{2}-\d{2}-[a-f0-9]{10}$/.test(n)).map(n=>path.join(STATE,n)).sort((a,b)=>fs.statSync(b).mtimeMs-fs.statSync(a).mtimeMs);
    for(const obsolete of releases.slice(3)) if(obsolete!==stage) fs.rmSync(obsolete,{recursive:true});
    // Private image cache only: prune unreferenced derivatives older than a week.
    const referenced=new Set(edition?[...edition.projects.map(r=>r.image),...edition.developers.map(r=>r.logo)].filter(Boolean).map(u=>MEDIA.exec(u)[1]+'.webp'):[]);
    for(const name of fs.readdirSync(assetDir)) if(/^[a-f0-9]{64}\.webp$/.test(name) && !referenced.has(name) && Date.now()-fs.statSync(path.join(assetDir,name)).mtimeMs>7*86400000) fs.unlinkSync(path.join(assetDir,name));
    console.log(JSON.stringify({status:result.status,date:edition?.snapshot_date||null,pages:32,current,warning:result.warning}));
  } catch(e) { if(stage && fs.existsSync(stage) && (!fs.existsSync(path.join(STATE,'current')) || fs.realpathSync(path.join(STATE,'current'))!==stage)) fs.rmSync(stage,{recursive:true});throw e; }
  finally {fs.closeSync(fd);fs.unlinkSync(lock);}
}
publish().catch(e=>{console.error(e.message);process.exitCode=1;});
