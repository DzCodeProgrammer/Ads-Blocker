"""
Scriptlet Engine — built-in JS snippets injected into pages via content script.

Scriptlets defeat common anti-adblock techniques:
  - Neutralise eval-based detection
  - Abort property reads (adblock detection checks)
  - Block specific setTimeout/setInterval callbacks
  - Remove classes added by ad scripts
  - Auto-defeat cookie consent prompts
  - Block WebRTC IP leaks
  - Silence notification prompts
  - Anti-anti-adblock: make fake ad elements visible to detectors
"""
from __future__ import annotations

# name → JS IIFE template; {PLACEHOLDER} are replaced by ScriptletEngine.get()
SCRIPTLETS: dict[str, str] = {

    # ── Defeat anti-adblock detectors ────────────────────────────────────────
    "anti-adblock-killer": """(function(){
  const _noop = function(){};
  const _fakeDetector = { onDetected:_noop, onNotDetected:_noop, check:()=>false,
                          bait:_noop, setOption:_noop };
  ['adblock','AdBlock','adBlocker','AdBlocker','blockAdBlock','BlockAdBlock',
   'fuckadblock','FuckAdBlock','adblockplus','AdBlockPlus'].forEach(p=>{
    try{ Object.defineProperty(window,p,{get:()=>_fakeDetector,set:_noop,configurable:true}); }catch(_){}
  });
  // Make fake ad divs look real (offsetHeight trick)
  const _origCreate = document.createElement.bind(document);
  document.createElement = function(tag){
    const el = _origCreate(tag);
    if(tag==='div'||tag==='ins'){
      try{ Object.defineProperty(el,'offsetHeight',{get:()=>1}); }catch(_){}
      try{ Object.defineProperty(el,'offsetParent',{get:()=>document.body}); }catch(_){}
    }
    return el;
  };
})();""",

    # ── Abort property read (prevents window.X access) ────────────────────────
    "abort-on-property-read": """(function(prop){
  if(!prop) return;
  const parts = prop.split('.');
  let obj = window;
  for(let i=0;i<parts.length-1;i++){ if(obj==null) return; obj=obj[parts[i]]; }
  const last = parts[parts.length-1];
  try{ Object.defineProperty(obj,last,{
    get(){ throw new ReferenceError(prop+' is not defined'); },
    set(){}, configurable:true
  }); }catch(_){}
})('{PROP}');""",

    # ── Abort property write ──────────────────────────────────────────────────
    "abort-on-property-write": """(function(prop){
  if(!prop) return;
  const parts = prop.split('.');
  let obj = window;
  for(let i=0;i<parts.length-1;i++){ if(!obj) return; obj=obj[parts[i]]; }
  const last = parts[parts.length-1];
  try{ Object.defineProperty(obj,last,{
    set(){ throw new ReferenceError('blocked write: '+prop); },
    get(){ return undefined; }, configurable:true
  }); }catch(_){}
})('{PROP}');""",

    # ── Block specific setTimeout callbacks ───────────────────────────────────
    "no-setTimeout-if": """(function(needle){
  const orig = window.setTimeout;
  window.setTimeout = function(fn, delay, ...args){
    const s = typeof fn==='function'?fn.toString():String(fn);
    if(needle && s.includes(needle)) return 0;
    return orig.call(this,fn,delay,...args);
  };
  window.setTimeout.toString = orig.toString.bind(orig);
})('{NEEDLE}');""",

    # ── Block specific setInterval callbacks ──────────────────────────────────
    "no-setInterval-if": """(function(needle){
  const orig = window.setInterval;
  window.setInterval = function(fn, delay, ...args){
    const s = typeof fn==='function'?fn.toString():String(fn);
    if(needle && s.includes(needle)) return 0;
    return orig.call(this,fn,delay,...args);
  };
  window.setInterval.toString = orig.toString.bind(orig);
})('{NEEDLE}');""",

    # ── Set a constant window property ────────────────────────────────────────
    "set-constant": """(function(prop, raw){
  if(!prop) return;
  const val = raw==='true'?true:raw==='false'?false:raw==='null'?null:
              raw==='undefined'?undefined:!isNaN(raw)?Number(raw):raw;
  const parts = prop.split('.');
  let obj = window;
  for(let i=0;i<parts.length-1;i++){ obj = obj[parts[i]] = obj[parts[i]]||{}; }
  const last = parts[parts.length-1];
  try{ Object.defineProperty(obj,last,{get:()=>val,set:()=>{},configurable:false}); }catch(_){}
})('{PROP}','{VALUE}');""",

    # ── Remove CSS classes ─────────────────────────────────────────────────────
    "remove-class": """(function(cls, sel){
  const rm = ()=>{
    const els = document.querySelectorAll(sel||(cls?'.'+cls:'*'));
    els.forEach(el=>el.classList.remove(...cls.split('|')));
  };
  if(document.readyState!=='loading') rm();
  else document.addEventListener('DOMContentLoaded',rm);
  new MutationObserver(rm).observe(document.documentElement,{attributes:true,childList:true,subtree:true});
})('{CLASS}','{SELECTOR}');""",

    # ── Block fetch to specific URL patterns ──────────────────────────────────
    "no-fetch-if": """(function(needle){
  const orig = window.fetch;
  window.fetch = function(url,...args){
    if(needle && String(url).includes(needle))
      return Promise.reject(new TypeError('AdBlocker: blocked fetch to '+url));
    return orig.call(this,url,...args);
  };
})('{NEEDLE}');""",

    # ── Block XMLHttpRequest to specific URLs ──────────────────────────────────
    "no-xhr-if": """(function(needle){
  const OrigXHR = window.XMLHttpRequest;
  function PatchedXHR(){ OrigXHR.call(this); }
  PatchedXHR.prototype = Object.create(OrigXHR.prototype);
  PatchedXHR.prototype.open = function(method,url,...args){
    if(needle && String(url).includes(needle)){
      Object.defineProperty(this,'status',{get:()=>200});
      Object.defineProperty(this,'responseText',{get:()=>''});
      this._blocked=true; return;
    }
    return OrigXHR.prototype.open.call(this,method,url,...args);
  };
  PatchedXHR.prototype.send = function(...args){
    if(this._blocked){ setTimeout(()=>this.dispatchEvent(new Event('load')),0); return; }
    return OrigXHR.prototype.send.call(this,...args);
  };
  window.XMLHttpRequest = PatchedXHR;
})('{NEEDLE}');""",

    # ── Disable WebRTC (prevents IP leak via STUN) ────────────────────────────
    "no-webrtc": """(function(){
  const noop=()=>{};
  ['RTCPeerConnection','webkitRTCPeerConnection','mozRTCPeerConnection'].forEach(k=>{
    if(!window[k]) return;
    const orig=window[k];
    window[k]=function(cfg){
      if(cfg&&cfg.iceServers) cfg.iceServers=[];
      const pc=new orig(cfg);
      const origAdd=pc.addIceCandidate.bind(pc);
      pc.addIceCandidate=function(c){
        if(c&&c.candidate&&c.candidate.includes('.local')) return Promise.resolve();
        return origAdd(c);
      };
      return pc;
    };
    window[k].prototype=orig.prototype;
  });
})();""",

    # ── Block notification permission requests ─────────────────────────────────
    "no-notification-if": """(function(){
  const orig=Notification.requestPermission.bind(Notification);
  Notification.requestPermission=function(callback){
    const p=Promise.resolve('denied');
    if(typeof callback==='function') p.then(callback);
    return p;
  };
  try{ Object.defineProperty(Notification,'permission',{get:()=>'denied'}); }catch(_){}
})();""",

    # ── Cookie remover ────────────────────────────────────────────────────────
    "cookie-remover": """(function(name){
  const remove=n=>{
    const exp='expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
    document.cookie=`${n}=; ${exp}`;
    document.cookie=`${n}=; ${exp}; domain=${location.hostname}`;
    document.cookie=`${n}=; ${exp}; domain=.${location.hostname}`;
  };
  if(name){ remove(name); }
  else{ document.cookie.split(';').forEach(c=>remove(c.split('=')[0].trim())); }
})('{NAME}');""",

    # ── Neutralise eval() for anti-adblock scripts ─────────────────────────────
    "noeval": """(function(){
  const orig=window.eval;
  window.eval=function(code){
    if(/adbl|blockad|adblocker|ad.blocker/i.test(String(code))) return undefined;
    return orig.call(this,code);
  };
  window.eval.toString=orig.toString.bind(orig);
})();""",

    # ── YouTube: skip overlay ads & dismiss pre-roll ──────────────────────────
    "youtube-ad-skip": """(function(){
  const skip=()=>{
    const btn=document.querySelector('.ytp-ad-skip-button,.ytp-skip-ad-button');
    if(btn){ btn.click(); return; }
    const overlay=document.querySelector('.ad-showing video');
    if(overlay){ overlay.currentTime=overlay.duration; }
    // Dismiss overlay ads
    document.querySelectorAll('.ytp-ad-overlay-close-button').forEach(b=>b.click());
    // Hide banner ads
    const banners=document.querySelectorAll('.ytd-banner-promo-renderer,.ytd-statement-banner-renderer');
    banners.forEach(b=>b.remove());
  };
  const id=setInterval(skip,300);
  // Stop checking after 2 minutes per page
  setTimeout(()=>clearInterval(id),120000);
  // Also observe DOM for new ads
  new MutationObserver(skip).observe(document.documentElement,{childList:true,subtree:true});
})();""",
}


class ScriptletEngine:
    """Resolve scriptlet names to injectable JS code."""

    def get(self, name: str, **params: str) -> str | None:
        template = SCRIPTLETS.get(name)
        if not template:
            return None
        for key, value in params.items():
            template = template.replace(f"{{{key.upper()}}}", str(value))
        return template

    def get_bundle(self, names: list[str], params_map: dict | None = None) -> str:
        """Get multiple scriptlets concatenated into one injectable block."""
        parts = []
        for name in names:
            p = (params_map or {}).get(name, {})
            code = self.get(name, **p)
            if code:
                parts.append(f"/* scriptlet: {name} */\n{code}")
        return "\n\n".join(parts)

    def list_all(self) -> list[str]:
        return list(SCRIPTLETS.keys())
