/**
 * Scriptlet Injector — fetches scriptlet bundle from backend and injects at document_start.
 *
 * Scriptlets are injected as <script> tags into the page's main world,
 * giving them access to the page's window object to neutralise anti-adblock detectors.
 */

(function () {
  'use strict';

  const BACKEND = 'http://127.0.0.1:8765';
  const domain = location.hostname.replace(/^www\./, '');

  async function injectScriptlets() {
    try {
      const res = await fetch(`${BACKEND}/api/scriptlets/bundle`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ domain, include_defaults: true }),
      });
      if (!res.ok) return;
      const { code } = await res.json();
      if (!code) return;

      // Inject into the main world via <script> tag
      const script = document.createElement('script');
      script.id = '__adblock_scriptlets__';
      script.textContent = `(function(){\n${code}\n})();`;
      (document.head || document.documentElement).prepend(script);
      // Remove tag after execution to keep DOM clean
      script.remove();
    } catch (_) {
      // Backend offline — fall back to inline defaults
      injectInlineDefaults();
    }
  }

  function injectInlineDefaults() {
    // Minimal inline anti-adblock defeat (does not require backend)
    const code = `(function(){
      const _noop = function(){};
      ['adblock','AdBlock','blockAdBlock'].forEach(function(p){
        try{ Object.defineProperty(window,p,{get:function(){return {onDetected:_noop,check:function(){return false;}};},configurable:true}); }catch(e){}
      });
    })();`;
    const script = document.createElement('script');
    script.textContent = code;
    (document.head || document.documentElement).prepend(script);
    script.remove();
  }

  injectScriptlets();
})();
