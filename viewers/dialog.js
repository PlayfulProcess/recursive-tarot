/* viewers/dialog.js — the one small modal dialog for the simple reading pages.
 *   SiteDialog.open({ title, label, className }) -> { body, close }
 * Closes on the X, Esc and a click on the backdrop; locks page scroll while open and returns
 * focus to what had it. Colours come from theme.css tokens only (light theme, CLAUDE.md).
 * Used by viewers/reading-actions.js (picture popup, chooser) and viewers/card-detail.js. */
(function (global) {
  'use strict';
  var CSS = '' +
    '.sd-back{position:fixed;inset:0;z-index:2000;background:rgba(60,45,20,.4);display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box}' +
    '.sd-box{position:relative;background:var(--surface,#fff);color:var(--ink,#221f1a);border:1px solid var(--line-soft,#cfc8ba);border-radius:12px;box-shadow:var(--shadow-lift,0 26px 46px -22px rgba(60,45,20,.6));width:100%;max-width:560px;max-height:calc(100vh - 32px);max-height:calc(100dvh - 32px);overflow:auto;padding:22px 20px 20px;box-sizing:border-box}' +
    '.sd-box.sd-wide{max-width:720px}' +
    '.sd-x{position:absolute;top:6px;right:6px;width:44px;height:44px;border:0;background:none;color:var(--ink-soft,#4a4439);font:400 26px/1 var(--sans,system-ui);cursor:pointer;border-radius:8px}' +
    '.sd-x:hover{color:var(--ink,#221f1a)}' +
    '.sd-x:focus-visible{outline:3px solid var(--gold,#9a7322);outline-offset:2px}' +
    '.sd-title{font-family:var(--serif-display,Georgia,serif);font-weight:600;font-size:22px;line-height:1.2;margin:0 44px 12px 0;color:var(--ink,#221f1a)}';
  function css() {
    if (document.getElementById('sd-css')) return;
    var s = document.createElement('style'); s.id = 'sd-css'; s.textContent = CSS; document.head.appendChild(s);
  }
  var stack = [];
  function open(o) {
    o = o || {}; css();
    var prev = document.activeElement;
    var back = document.createElement('div'); back.className = 'sd-back';
    var box = document.createElement('div'); box.className = 'sd-box' + (o.className ? ' ' + o.className : '');
    box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true');
    var x = document.createElement('button'); x.type = 'button'; x.className = 'sd-x'; x.setAttribute('aria-label', 'Close'); x.textContent = '×';
    var title = document.createElement('h2'); title.className = 'sd-title'; title.textContent = o.title || '';
    title.id = 'sd-t' + Math.random().toString(36).slice(2, 8);
    box.setAttribute('aria-labelledby', title.id);
    var body = document.createElement('div');
    box.appendChild(x); if (o.title) box.appendChild(title); box.appendChild(body);
    back.appendChild(box); document.body.appendChild(back);
    var prevOverflow = document.body.style.overflow; document.body.style.overflow = 'hidden';
    var closed = false;
    function close() {
      if (closed) return; closed = true;
      document.removeEventListener('keydown', onKey, true);
      back.remove(); document.body.style.overflow = prevOverflow;
      var i = stack.indexOf(handle); if (i >= 0) stack.splice(i, 1);
      if (prev && prev.focus) { try { prev.focus(); } catch (e) {} }
      if (typeof o.onClose === 'function') o.onClose();
    }
    function onKey(e) {
      if (stack[stack.length - 1] !== handle) return;
      if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); close(); }
      else if (e.key === 'Tab') {   // keep focus inside the dialog
        var f = box.querySelectorAll('a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])');
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    }
    var handle = { body: body, box: box, close: close };
    stack.push(handle);
    x.addEventListener('click', close);
    back.addEventListener('click', function (e) { if (e.target === back) close(); });
    document.addEventListener('keydown', onKey, true);
    setTimeout(function () { x.focus(); }, 0);
    return handle;
  }
  global.SiteDialog = { open: open };
})(window);
