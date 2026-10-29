'use client';
import { useEffect, useRef } from 'react';
import { shell } from './shell';
export default function Cinema(){const started=useRef(false);useEffect(()=>{if(started.current)return;started.current=true;(async()=>{for(const name of ['app','upgrade','discovery','cloud','final'])await new Promise<void>((resolve,reject)=>{const s=document.createElement('script');s.src='/web/'+name+'.js';s.onload=()=>resolve();s.onerror=()=>reject(new Error('Application scripts could not load.'));document.body.appendChild(s)})})().catch(()=>{const e=document.getElementById('app');if(e)e.innerHTML='<div class="empty"><h2>Unable to load the cinema.</h2><p>Please refresh the page to try again.</p></div>'})},[]);return <div dangerouslySetInnerHTML={{__html:shell}}/>}
