#!/usr/bin/env node
'use strict';
const path=require('path');
const {refresh}=require('./daily/cache');
const root=path.resolve(__dirname,'..');
const args=process.argv.slice(2);
const local=args.includes('--local');
refresh({cacheDir:process.env.LANDING_CACHE_DIR||path.join(root,'.cache/landing'),assetDir:path.join(root,'assets/daily'),
  ...(local?{endpoint:'http://127.0.0.1:81/api/public/landing-content',allowLocal:true}:{})})
 .then(r=>console.log(`Landing edition ${r.data.snapshot_date}: ${r.status}${r.warning?' ('+r.warning+')':''}`))
 .catch(e=>{console.error(e.message);process.exitCode=1;});
