'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('fs');
const os=require('os');
const path=require('path');
const crypto=require('crypto');
const {JSDOM}=require('jsdom');
const {validate,cairoDay}=require('../tools/daily/schema');
const {refresh,boundedFetch}=require('../tools/daily/cache');
const {applyDaily}=require('../tools/daily/render');
const now=new Date('2026-11-04T10:00:00Z');
const href='https://brokers.estavo.space/register?redirect=%2Fprojects%2F1';
function fixture() {
 const text={ar:'مشروع اختباري',en:'Test project'};
 return {schema_version:1,snapshot_date:'2026-11-04',timezone:'Africa/Cairo',generated_at:'2026-11-04T09:00:00Z',expires_at:'2026-11-04T22:00:00Z',revision:'a'.repeat(64),
 projects:[{key:'p1',name:text,city:text,developer:text,image:null,updated_at:'2026-11-03T10:00:00Z',href}],
 units:[{key:'u1',project_key:'p1',project:text,type:text,price_from:8000000,currency:'EGP',area_sqm:140,bedrooms:3,delivery:null,selection:'daily_rotation',href}],
 developers:[{key:'d1',name:text,logo:null,selection:'daily_rotation',href}],
 news:[{key:'n1',title:text,summary:text,published_at:'2026-11-04T08:00:00Z',sources:[{name:'Publisher',url:'https://example.com/news'}],selection:'recent',href}],
 launches:[],jobs:[],games:[{key:'exclusive',name:{ar:'تغيير وش',en:'Taghyeer Wesh'},prompt:'سمي مشروع في القاهرة الجديدة',selection:'daily_rotation',href:'https://brokers.estavo.space/games/exclusive'}]};
}
const reply=bytes=>new Response(bytes,{status:200,headers:{'content-type':'application/json'}});
test('Cairo editions respect midnight and DST independently of the build host',()=>{
 assert.equal(cairoDay(new Date('2026-11-04T21:59:59Z')),'2026-11-04');
 assert.equal(cairoDay(new Date('2026-11-04T22:00:00Z')),'2026-11-05');
 assert.equal(cairoDay(new Date('2026-07-04T21:00:00Z')),'2026-07-05');
});
test('schema refuses overflow, unknown fields, origin images, inconsistent units and dangerous links',()=>{
 assert.equal(validate(fixture(),now).units.length,1);
 const mutations=[d=>d.developers=Array.from({length:7},(_,i)=>({...d.developers[0],key:'d'+i})),d=>d.projects[0].image='https://example.com/original.jpg',d=>d.units[0].price_from=-1,d=>d.units[0].project_key='unknown',d=>d.developers[0].phone='private',d=>d.games[0].answers=['secret'],d=>d.news[0].sources[0].url='javascript:alert(1)',d=>d.projects[0].href='https://brokers.estavo.space.evil.test/',d=>d.generated_at='2026-11-10T00:00:00Z',d=>d.snapshot_date='2026-11-03'];
 for(const change of mutations) {const d=fixture();change(d);assert.throws(()=>validate(d,now));}
 assert.throws(()=>validate(fixture(),new Date('2026-11-08T10:00:00Z')));
});
test('refresh makes one daily request, and retains the last complete edition on failure',async t=>{
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'estavo-daily-'));t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
 const opts={cacheDir:path.join(root,'cache'),assetDir:path.join(root,'assets'),now};let calls=0;
 const fetcher=async()=>{calls++;return reply(JSON.stringify(fixture()));};
 assert.equal((await refresh({...opts,fetcher})).status,'updated');
 assert.equal((await refresh({...opts,fetcher})).status,'unchanged');assert.equal(calls,1);
 const before=fs.readFileSync(path.join(opts.cacheDir,'current.json'),'utf8');
 const bad=async()=>{throw new Error('network unavailable');};
 assert.equal((await refresh({...opts,now:new Date('2026-11-05T10:00:00Z'),fetcher:bad})).status,'last-good');
 assert.equal(fs.readFileSync(path.join(opts.cacheDir,'current.json'),'utf8'),before);
 await assert.rejects(refresh({...opts,now:new Date('2026-11-08T10:00:00Z'),fetcher:bad}));
 await assert.rejects(refresh({...opts,endpoint:'http://169.254.169.254/latest/meta-data',fetcher}));
});
test('a missing or invalid thumbnail cannot publish a partial edition',async t=>{
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'estavo-media-'));t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
 const opts={cacheDir:path.join(root,'cache'),assetDir:path.join(root,'assets'),now};
 const d=fixture();d.projects[0].image='/api/public/landing-content/media/'+ 'b'.repeat(64)+'.webp';
 await assert.rejects(refresh({...opts,fetcher:async url=>reply(url.endsWith('.webp')?'not-webp':JSON.stringify(d))}));
 assert.equal(fs.existsSync(path.join(opts.cacheDir,'current.json')),false);
});
test('downloads have hard streaming byte limits',async()=>{
 await assert.rejects(boundedFetch('https://example.com',10,async()=>reply('x'.repeat(11))));
});
test('daily rendering cannot replace approved scenes or inject an extra section',()=>{
 const html='<!doctype html><html><head></head><body><main><section><div class="es-hero__copy"><h1>الصفحة</h1><a href="/original">ابدأ</a></div><div class="pd"><div class="pd-win"><img src="hero-ar.svg"></div></div></section></main></body></html>';
 const d=fixture();d.units[0].project.ar='<img src=x onerror=alert(1)>';
 for(const edition of [d,{...d,news:[],jobs:[],units:[]}]) {
  const output=applyDaily(html,'market','ar',edition);
  assert.equal(output.replace('<meta name="estavo-content-mode" content="approved-examples">\n',''),html);
 }
});
test('all 32 pages preserve the authored artwork and exclude the rejected selections UI',()=>{
 const root=path.resolve(__dirname,'..');let count=0;
 for(const r of require('../tools/routes.json').routes)for(const lang of ['ar','en']){
  const filename=lang==='ar'?'index.html':'en.html';
  const html=fs.readFileSync(path.join(root,r.path,filename),'utf8');
  const source=fs.readFileSync(path.join(root,'tools',r.key==='home'?'home/'+filename:'pages/'+r.key+'.'+lang+'.html'),'utf8');
  const dom=new JSDOM(html);const authored=new JSDOM(source);
  const scenes=doc=>[...doc.querySelectorAll('.pd-win,.pd-phone,.pd-doc,.pd-chip,.dest-cover,.es-home-today__grid,.ns-cards,.ns-anat,.dv-mini')].map(el=>el.outerHTML.replace(/(?:\.\.\/|\/)?assets\//g,'assets/'));
  assert.deepEqual(scenes(dom.window.document),scenes(authored.window.document),r.key+' '+lang);
  assert.equal(dom.window.document.querySelector('.daily-edition,.daily-empty,.daily-screen,.daily-illustrative'),null);
  assert.doesNotMatch(html,/مختارات إستاڤو|Estavo selections|daily-content\.css/);
  dom.window.close();authored.window.close();count++;
 }
 assert.equal(count,32);
});
