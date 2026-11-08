'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { validate, cairoDay, MEDIA } = require('./schema');
const DEFAULT_ENDPOINT = 'https://api-brokers.estavo.space/api/public/landing-content';
async function boundedFetch(url, max, fetcher = fetch) {
  const res = await fetcher(url, {redirect:'error',signal:AbortSignal.timeout(15000),headers:{Accept:url.endsWith('.webp')?'image/webp':'application/json','User-Agent':'EstavoLandingBuild/1.0'}});
  if (!res.ok) throw new Error(`Landing source returned ${res.status}`);
  if (Number(res.headers.get('content-length')) > max) throw new Error('Landing source exceeds byte limit');
  const chunks=[];let size=0;
  for await (const chunk of res.body) { size+=chunk.length;if(size>max) throw new Error('Landing source exceeds byte limit');chunks.push(chunk); }
  return Buffer.concat(chunks);
}
function read(cacheDir, now = new Date()) {
  try { return validate(JSON.parse(fs.readFileSync(path.join(cacheDir,'current.json'),'utf8')),now); }
  catch { return null; }
}
async function refresh({cacheDir,assetDir,endpoint=DEFAULT_ENDPOINT,now=new Date(),fetcher=fetch,allowLocal=false}) {
  const url=new URL(endpoint);
  const production = url.origin === 'https://api-brokers.estavo.space';
  const local = allowLocal && url.origin === 'http://127.0.0.1:81';
  if ((!production && !local) || url.pathname !== '/api/public/landing-content' || url.search || url.hash || url.username || url.password) throw new Error('Unapproved landing source');
  fs.mkdirSync(cacheDir,{recursive:true});fs.mkdirSync(assetDir,{recursive:true});
  const lock=path.join(cacheDir,'.refresh-lock');
  // Exclusive local process lock; publication jobs also use flock at the service layer.
  let fd;
  try { fd=fs.openSync(lock,'wx'); } catch(e) { if(e.code==='EEXIST') throw new Error('Another landing refresh is running; inspect a stale lock before removing it');throw e; }
  try {
    const previous=read(cacheDir,now);
    const complete = previous && [...previous.projects.map(r=>r.image),...previous.developers.map(r=>r.logo),...previous.showcase.map(r=>r.image)].filter(Boolean).every(item => {
      const hash=MEDIA.exec(item)[1],file=path.join(assetDir,hash+'.webp');
      return fs.existsSync(file) && crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')===hash;
    });
    if(previous?.snapshot_date===cairoDay(now) && complete) return {data:previous,status:'unchanged'};
    try {
      const bytes=await boundedFetch(endpoint,65536,fetcher);
      const data=validate(JSON.parse(bytes.toString('utf8')),now);
      if(previous && data.snapshot_date<previous.snapshot_date) throw new Error('Landing source moved backwards');
      const media=[...new Set([...data.projects.map(r=>r.image),...data.developers.map(r=>r.logo),...data.showcase.map(r=>r.image)].filter(Boolean))];
      // At most twelve sequential downloads, capped at 100KB each; no source URLs.
      for(const item of media) {
        const hash=MEDIA.exec(item)[1],file=path.join(assetDir,hash+'.webp');
        if(fs.existsSync(file) && crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')===hash) continue;
        const image=await boundedFetch(url.origin+item,100000,fetcher);
        if(image.toString('ascii',0,4)!=='RIFF' || image.toString('ascii',8,12)!=='WEBP' || crypto.createHash('sha256').update(image).digest('hex')!==hash) throw new Error('Invalid landing thumbnail');
        fs.writeFileSync(file+'.tmp',image);fs.renameSync(file+'.tmp',file);
      }
      fs.writeFileSync(path.join(cacheDir,'current.json.tmp'),bytes,{mode:0o640});
      fs.renameSync(path.join(cacheDir,'current.json.tmp'),path.join(cacheDir,'current.json'));
      return {data,status:data.snapshot_date===cairoDay(now)?'updated':'last-good'};
    } catch(e) {
      if(previous && complete) return {data:previous,status:'last-good',warning:e.message};
      throw e;
    }
  } finally { fs.closeSync(fd);fs.unlinkSync(lock); }
}
module.exports={refresh,read,boundedFetch,DEFAULT_ENDPOINT};
