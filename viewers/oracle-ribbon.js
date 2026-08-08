/* Oracle Ribbon — the "rolling disclaimer" (Phase 5 proposal, TAROT-REVAMP-PLAN-2026-08-07.md).
 * Part of the ritual, not a legal warning: a single thin line beneath the casting board,
 * shown once a cast lands, that slow-crossfades through a handful of short fragments —
 * "Keep your agency. The cards ask; you decide." — like a votive inscription being re-lit.
 *
 * PREVIEW-GATED: everything below is a no-op unless the page URL carries ?ribbon=1. This
 * lets the script ship on every page that includes it without changing default behavior
 * until Fernando approves the fragments + placement (plan Phase 5 gate).
 *
 * Self-contained: injects its own <style>, no external CSS dependency beyond the Fraunces
 * font already loaded site-wide. Exposes window.OracleRibbon = { show(afterEl) } so other
 * sites (astro, iching) can adopt the same component later — call show() with the element
 * the ribbon should be inserted directly after (e.g. the casting board) once a reading has
 * landed.
 *
 * Usage:  <script src="oracle-ribbon.js?v=1"></script>
 *         ... after a cast completes ...
 *         if (window.OracleRibbon) OracleRibbon.show(document.getElementById('board'));
 */
(function () {
  'use strict';
  if (window.OracleRibbon) return; // idempotent — safe to include more than once

  const FRAGMENTS = [
    'An oracle is a recursive process — make-believe becoming sense-making, sometimes becoming real.',
    'Keep your agency. The cards ask; you decide.',
    'The map is not the territory.',
    'A mirror, not a command.',
    'Gate, not fate.',
  ];
  const HOLD_MS = 8000;
  const FADE_MS = 2000;
  const SESSION_KEY = 'oracleRibbonDismissed';
  const STATIC_INDEX = 1; // "Keep your agency…" — the one fragment shown under reduced motion

  function ribbonEnabled() {
    try { return new URLSearchParams(location.search).get('ribbon') === '1'; }
    catch (_) { return false; }
  }

  function dismissedThisSession() {
    try { return sessionStorage.getItem(SESSION_KEY) === '1'; }
    catch (_) { return false; }
  }
  function markDismissed() {
    try { sessionStorage.setItem(SESSION_KEY, '1'); } catch (_) { /* private mode etc — fine to no-op */ }
  }

  function prefersReducedMotion() {
    try { return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches); }
    catch (_) { return false; }
  }

  function injectStyle() {
    if (document.getElementById('oracle-ribbon-style')) return;
    const style = document.createElement('style');
    style.id = 'oracle-ribbon-style';
    style.textContent = [
      '.oracle-ribbon{display:flex;align-items:baseline;justify-content:center;gap:10px;',
      'margin:10px auto 0;padding:2px 28px 2px 8px;max-width:640px;position:relative;',
      'font-family:"Fraunces",Georgia,serif;font-style:italic;font-size:12.5px;',
      'line-height:1.5;letter-spacing:.045em;text-align:center;',
      'color:#9a7322;opacity:.8;background:transparent;border:none;box-shadow:none;}',
      '.oracle-ribbon .orb-text{flex:1 1 auto;min-width:0;transition:opacity ' + FADE_MS + 'ms ease;opacity:1;}',
      '.oracle-ribbon .orb-text.orb-fade{opacity:0;}',
      '.oracle-ribbon .orb-close{position:absolute;right:4px;top:50%;transform:translateY(-50%);',
      'flex:0 0 auto;cursor:pointer;background:none;border:none;padding:2px 4px;',
      'font-family:inherit;color:inherit;opacity:.6;font-size:12px;line-height:1;}',
      '.oracle-ribbon .orb-close:hover{opacity:1;}',
      '@media (prefers-reduced-motion: reduce){.oracle-ribbon .orb-text{transition:none;}}',
    ].join('');
    document.head.appendChild(style);
  }

  let mounted = false;

  function show(afterEl) {
    if (!ribbonEnabled()) return;          // preview flag off — no-op
    if (dismissedThisSession()) return;
    if (mounted) return;
    if (!afterEl || !afterEl.parentNode) return;

    injectStyle();
    mounted = true;

    const reduced = prefersReducedMotion();

    const wrap = document.createElement('div');
    wrap.className = 'oracle-ribbon';
    wrap.setAttribute('role', 'note');
    wrap.setAttribute('aria-label', 'A note on how to read this');

    const textEl = document.createElement('span');
    textEl.className = 'orb-text';

    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'orb-close';
    closeBtn.setAttribute('aria-label', 'Dismiss this note for the rest of your session');
    closeBtn.textContent = '×';

    wrap.appendChild(textEl);
    wrap.appendChild(closeBtn);
    afterEl.parentNode.insertBefore(wrap, afterEl.nextSibling);

    let idx = reduced ? STATIC_INDEX : 0;
    textEl.textContent = FRAGMENTS[idx];

    let holdTimer = null, fadeTimer = null;
    function scheduleNext() {
      holdTimer = setTimeout(() => {
        textEl.classList.add('orb-fade');
        fadeTimer = setTimeout(() => {
          idx = (idx + 1) % FRAGMENTS.length;
          textEl.textContent = FRAGMENTS[idx];
          textEl.classList.remove('orb-fade');
          scheduleNext();
        }, FADE_MS);
      }, HOLD_MS);
    }
    if (!reduced) scheduleNext();

    closeBtn.addEventListener('click', () => {
      if (holdTimer) clearTimeout(holdTimer);
      if (fadeTimer) clearTimeout(fadeTimer);
      markDismissed();
      wrap.remove();
      mounted = false;
    });
  }

  window.OracleRibbon = { show };
})();
