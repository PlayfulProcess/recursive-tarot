/* Oracle Ribbon — the "rolling disclaimer" (Phase 5 proposal, TAROT-REVAMP-PLAN-2026-08-07.md).
 * Part of the ritual, not a legal warning: a single thin line beneath the casting board,
 * shown once a cast lands, that slow-crossfades through a handful of short fragments —
 * "Keep your agency. The cards ask; you decide." — like a votive inscription being re-lit.
 *
 * To the left of the text sits a small spiral mark — the same golden-ratio curve as the
 * site's hero/header spiral (public/spiral/spiral.js generateSpiralPath), reproduced inline
 * below so this file has no external asset dependency. It's the visible "this is thinking"
 * cue: the rolling text alone read as a static disclaimer, not an active process.
 *
 * Fixed Aug 8 2026, mirroring the flow app's OracleRibbon.tsx (same builder feedback: a bare
 * rotation didn't read as active — a logarithmic spiral turning about its own centre is close
 * to rotationally self-similar, so a slow spin barely changes the silhouette frame to frame).
 * Now the mark draws/undraws via stroke-dashoffset (the same idiom as the flow app's brand
 * SpiralLoader) at a slow ~7.2s cycle (her call: same tempo family as the loader, 3x slower), with the previous 7s rotation layered on top as
 * secondary texture rather than the primary cue. Static (no motion at all) under
 * prefers-reduced-motion — this ribbon isn't a busy/loading state (it appears once a cast has
 * already landed, as a reflective note), so there's no "Interpreting…"-style text fallback to
 * add here the way the flow app's waiting-state twin needed one; a frozen mark is honest, not
 * a broken loading cue, in this context. Colour follows --orb-ink via currentColor, same as
 * the text.
 *

 * DEFAULT-ON, SITEWIDE (Aug 10 2026): Fernando approved the fragments + placement (plan
 * Phase 5 gate), so the ribbon is no longer preview-gated behind ?ribbon=1. site-footer.js
 * now loads this script and calls show(anchor, { gated: false }) on every page that carries
 * the shared footer, so the ribbon appears ambiently near the page's footer everywhere —
 * not just on caster-studio.html's post-cast board. The `gated` option (default true) still
 * exists for any future caller that *does* want the old ?ribbon=1 preview behavior; it's
 * just unused by the sitewide footer call, which always passes gated:false.
 *
 * Self-contained: injects its own <style>, no external CSS dependency beyond the Fraunces
 * font already loaded site-wide. Exposes window.OracleRibbon = { show(afterEl) } so other
 * sites (astro, iching) can adopt the same component later — call show() with the element
 * the ribbon should be inserted directly after (e.g. the casting board) once a reading has
 * landed.
 *
 * Usage:  <script src="oracle-ribbon.js?v=4"></script>
 *         ... after a cast completes ...
 *         if (window.OracleRibbon) OracleRibbon.show(document.getElementById('board'), { gated: false });
 */
(function () {
  'use strict';
  if (window.OracleRibbon) return; // idempotent — safe to include more than once

  // Golden-ratio logarithmic spiral — identical algorithm to
  // public/spiral/spiral.js's generateSpiralPath (the site header/hero
  // spiral generator). Reproduced inline (not <script src>'d) so this file
  // stays self-contained per its own contract above: other sites adopting
  // oracle-ribbon.js get the exact brand curve with zero extra requests.
  // Computed once at module load, same turns/size as the header spiral.
  function generateSpiralPath(size, turns) {
    const center = size / 2;
    const maxRadius = size * 0.45;
    const goldenRatio = (1 + Math.sqrt(5)) / 2;
    const growthRate = Math.log(goldenRatio) / (Math.PI / 2);
    const minRadius = 0.5;
    const totalPoints = turns * 300;
    const points = [];
    for (let i = 0; i <= totalPoints; i++) {
      const t = (i / 300) * 2 * Math.PI;
      let r = minRadius * Math.exp(growthRate * t);
      if (r > maxRadius) r = maxRadius;
      const x = center + r * Math.cos(t);
      const y = center + r * Math.sin(t);
      points.push((i === 0 ? 'M ' : 'L ') + x.toFixed(2) + ' ' + y.toFixed(2));
    }
    return points.join(' ');
  }
  const SPIRAL_D = generateSpiralPath(100, 6);

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
      // Never paints a surface — no background, no border, no shadow. The ribbon is an
      // inscription on whatever page hosts it, so it must disappear into a light parchment
      // page AND a dark app panel. Colour follows the host's theme three ways (OS preference,
      // a data-theme attribute, or a .dark class — flow/Tailwind uses the last one).
      // Ink follows the HOST's declared theme, and deliberately NOT the OS preference:
      // this site is light-only, so honouring prefers-color-scheme painted pale dark-mode
      // gold onto cream parchment for anyone whose laptop is set to dark. A host that is
      // genuinely dark says so — data-theme="dark", a .dark class (Tailwind), or
      // color-scheme:dark — and only then does the ink lighten.
      ':root{--orb-ink:#9a7322;}',
      '[data-theme="dark"] , .dark, [style*="color-scheme:dark"], [style*="color-scheme: dark"]{--orb-ink:#d8b978;}',
      '.oracle-ribbon{display:flex;align-items:center;justify-content:center;gap:8px;',
      'margin:10px auto 0;padding:2px 28px 2px 8px;max-width:640px;position:relative;',
      'font-family:"Fraunces",Georgia,serif;font-style:italic;font-size:12.5px;',
      'line-height:1.5;letter-spacing:.045em;text-align:center;',
      'color:var(--orb-ink,#9a7322);opacity:.82;background:transparent;border:none;box-shadow:none;}',
      // Thinking mark: the same brand spiral (SPIRAL_D above). Fixed Aug 8 2026 — a bare
      // rotation read as nearly static (a logarithmic spiral turning about its own centre is
      // close to rotationally self-similar), so the primary motion cue is now the path
      // drawing/undrawing via stroke-dashoffset (same idiom as the flow app's brand
      // SpiralLoader), at a slow ~7.2s cycle (her call: same tempo family as the loader, 3x slower). The 7s rotation still turns the wrapper on top,
      // like a votive wheel, as secondary texture — not the thing carrying the "it is active"
      // signal anymore.
      '.oracle-ribbon .orb-spiral{flex:0 0 auto;width:17px;height:17px;display:inline-block;',
      'animation:orb-spiral-spin 7s linear infinite;}',
      '.oracle-ribbon .orb-spiral svg{display:block;width:100%;height:100%;}',
      '.oracle-ribbon .orb-spiral path{stroke-dasharray:1;',
      'animation:orb-spiral-draw 7.2s ease-in-out infinite alternate;}',
      '@keyframes orb-spiral-spin{from{transform:rotate(0deg);}to{transform:rotate(360deg);}}',
      // Draws (offset 1→0) then un-draws (0→1) via `alternate` — mirrors the flow app's
      // `spiral-draw` keyframe (globals.css / <SpiralLoader>) exactly, just sped up.
      '@keyframes orb-spiral-draw{from{stroke-dashoffset:1;}to{stroke-dashoffset:0;}}',
      '.oracle-ribbon .orb-text{flex:1 1 auto;min-width:0;transition:opacity ' + FADE_MS + 'ms ease;opacity:1;}',
      '.oracle-ribbon .orb-text.orb-fade{opacity:0;}',
      '.oracle-ribbon .orb-close{position:absolute;right:4px;top:50%;transform:translateY(-50%);',
      'flex:0 0 auto;cursor:pointer;background:none;border:none;padding:2px 4px;',
      'font-family:inherit;color:inherit;opacity:.6;font-size:12px;line-height:1;}',
      '.oracle-ribbon .orb-close:hover{opacity:1;}',
      // Reduced motion: freeze both layers. No "Interpreting…"-style text fallback is added
      // here (unlike the flow app's waiting-state twin) — this ribbon shows AFTER a cast has
      // already landed, as a reflective note, not while something is loading, so a frozen mark
      // is honest rather than a broken loading cue.
      '@media (prefers-reduced-motion: reduce){.oracle-ribbon .orb-text{transition:none;}',
      '.oracle-ribbon .orb-spiral{animation:none;}',
      '.oracle-ribbon .orb-spiral path{animation:none;}}',
    ].join('');
    document.head.appendChild(style);
  }

  let mounted = false;

  /* show(afterEl, opts)
   *   opts.gated      — default true: obey the ?ribbon=1 preview flag. Pass false when a host
   *                     surface (e.g. the app's waiting state) deliberately always shows it.
   *   opts.holdMs     — override the per-fragment dwell. A waiting state that lasts ~15s wants
   *                     a shorter hold than a board a reader sits with.
   *   opts.fragments  — override the lines.
   *   opts.dismissible— default true; a waiting state that disappears on its own sets false.  */
  function show(afterEl, opts) {
    const o = opts || {};
    if (o.gated !== false && !ribbonEnabled()) return;   // preview flag off — no-op
    if (dismissedThisSession()) return;
    if (mounted) return;
    if (!afterEl || !afterEl.parentNode) return;

    const FRAGS = Array.isArray(o.fragments) && o.fragments.length ? o.fragments : FRAGMENTS;
    const hold = typeof o.holdMs === 'number' ? o.holdMs : HOLD_MS;

    injectStyle();
    mounted = true;

    const reduced = prefersReducedMotion();

    const wrap = document.createElement('div');
    wrap.className = 'oracle-ribbon';
    wrap.setAttribute('role', 'note');
    wrap.setAttribute('aria-label', 'A note on how to read this');

    // Thinking mark — decorative, aria-hidden (the ribbon's role="note"
    // label already carries the meaning; this is purely the visible cue).
    const spiralWrap = document.createElement('span');
    spiralWrap.className = 'orb-spiral';
    spiralWrap.setAttribute('aria-hidden', 'true');
    const spiralSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    spiralSvg.setAttribute('viewBox', '0 0 100 100');
    const spiralPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    spiralPath.setAttribute('d', SPIRAL_D);
    // Normalizes the dash math for orb-spiral-draw (stroke-dasharray:1 / dashoffset 0-1)
    // the same way <SpiralLoader> uses pathLength={1} in the flow app.
    spiralPath.setAttribute('pathLength', '1');
    spiralPath.setAttribute('fill', 'none');
    spiralPath.setAttribute('stroke', 'currentColor');
    spiralPath.setAttribute('stroke-width', '7');
    spiralPath.setAttribute('stroke-linecap', 'round');
    spiralSvg.appendChild(spiralPath);
    spiralWrap.appendChild(spiralSvg);

    const textEl = document.createElement('span');
    textEl.className = 'orb-text';

    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'orb-close';
    closeBtn.setAttribute('aria-label', 'Dismiss this note for the rest of your session');
    closeBtn.textContent = '×';

    wrap.appendChild(spiralWrap);
    wrap.appendChild(textEl);
    if (o.dismissible !== false) wrap.appendChild(closeBtn);
    else wrap.style.paddingRight = '8px';
    afterEl.parentNode.insertBefore(wrap, afterEl.nextSibling);

    let idx = reduced ? Math.min(STATIC_INDEX, FRAGS.length - 1) : 0;
    textEl.textContent = FRAGS[idx];

    let holdTimer = null, fadeTimer = null;
    function scheduleNext() {
      holdTimer = setTimeout(() => {
        textEl.classList.add('orb-fade');
        fadeTimer = setTimeout(() => {
          idx = (idx + 1) % FRAGS.length;
          textEl.textContent = FRAGS[idx];
          textEl.classList.remove('orb-fade');
          scheduleNext();
        }, FADE_MS);
      }, hold);
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
