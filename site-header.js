/* Shared site header for the Recursive Tarot static site.
 * One definition, used by every page (root + viewers/ + pages/). Style-isolated
 * via Shadow DOM so each viewer's own CSS can't override it. Path-aware so links
 * resolve from both the repo root and the /viewers/ subdir.
 *
 * Usage:  <script src="<path-to>/site-header.js?v=7"></script>
 *         <site-header active="cards"></site-header>
 * The `active` attribute highlights the matching tab; if omitted it is
 * auto-detected from the filename.
 *
 * Nav model (June 2026): two groups, all right-aligned.
 *  - VIEWS  — previews of the same data (Cards, Explorer, Tree of Life, Timeline,
 *             Tree, Genealogy), introduced by a tiny "views" caption.
 *  - TOOLS  — different-natured pages, each colour-coded: Caster (violet),
 *             Course (green), Shop (gold), GitHub (muted, external).
 */
(function () {
  if (customElements.get('site-header')) return;

  // Path back to the repo root — depth-aware so it works at any nesting
  // (root, /viewers/, /pages/, AND /viewers/prototypes/, /pages/book/ …).
  const _segs = location.pathname.split('/').filter(Boolean);
  const PFX = '../'.repeat(Math.max(0, _segs.length - 1));

  // Figure-capture mode (?fig=1): hide a viewer's own control toolbars so headless
  // screenshots become clean static plates for the print book. Only when explicitly asked.
  if (new URLSearchParams(location.search).get('fig') === '1') {
    const s = document.createElement('style');
    s.textContent = '.hint,.controls,.toolbar{display:none!important}';
    (document.head || document.documentElement).appendChild(s);
  }

  // Shared-identity widget (reads the .recursive.eco session cookie; L1 of the
  // integration ladder). Loaded once; renders as <recursive-auth> in the bar.
  if (!document.querySelector('script[data-recursive-auth]')) {
    const s = document.createElement('script');
    s.src = PFX + 'auth-widget.js?v=2';
    s.dataset.recursiveAuth = '1';
    document.head.appendChild(s);
  }

  // [key, label, href] — split by level
  const CARD_VIEWS = [
    ['explorer', 'Explorer', PFX + 'viewers/explorer.html'],
    ['cards',    'Cards',    PFX + 'viewers/cards.html'],
    ['lenses',   '⚗ Lenses', PFX + 'viewers/prototypes/lenses.html'],
    ['tree',     'Tree',     PFX + 'viewers/tree-viewer.html'],
  ];
  const GRAMMAR_VIEWS = [
    ['treeoflife', 'Tree of Life', PFX + 'viewers/genealogy-tree.html'],
    ['timeline',   'Timeline',     PFX + 'viewers/timeline.html'],
    ['genealogy',  'Genealogy',    PFX + 'genealogy.html'],
  ];
  // [key, label, href, cssClass, external?]
  const TOOLS = [
    ['shop',   '🛒 Shop',    PFX + 'pages/shop.html',          't-shop'],
    ['github', 'GitHub ↗',  'https://github.com/PlayfulProcess/recursive-tarot', 't-github', true],
  ];
  // Play — a dropdown of the games + readings (the pill itself links to the Play hub).
  const PLAY_MENU = [
    [PFX + 'pages/games/tarocchino.html', '♛ Tarocchino di Bologna'],
    [PFX + 'pages/games/madiao.html',     '🀄 Ma Diao 馬吊'],
    [PFX + 'pages/games/trionfi.html',    '♛ Trionfi'],
    [PFX + 'viewers/caster.html',         '🔮 Caster'],
    ['https://flow.recursive.eco/',   '✦ Oracle ↗', true],
    [PFX + 'pages/play.html',             'All games & readings →'],
  ];
  // Courses — a dropdown under one "Courses" pill (each is a course-viewer ?course=…).
  const COURSES = [
    ['history-of-tarot',                'A History of Tarot'],
    ['tarot-and-the-crack',             'Tarot & the Crack'],
    ['kant-and-the-tarot',              'Kant Reads the Tarot'],
    ['marsha-linehan-reads-the-tarot',  'Marsha Linehan Reads the Tarot'],
    ['build-a-tarot-deck-with-claude',  'Contribute to the Commons'],
  ];

  function autoActive() {
    const f = location.pathname.split('/').pop() || 'index.html';
    if (f.startsWith('cards')) return 'cards';
    if (f.startsWith('explorer')) return 'explorer';
    if (f.startsWith('lenses')) return 'lenses';
    if (f.startsWith('genealogy-tree')) return 'treeoflife';
    if (f.startsWith('timeline')) return 'timeline';
    if (f.startsWith('tree-viewer')) return 'tree';
    if (f.startsWith('play') || f.startsWith('caster') || f.startsWith('trionfi') || location.pathname.includes('/games/')) return 'play';
    if (f.startsWith('genealogy')) return 'genealogy';
    if (f.startsWith('course')) return 'course';
    if (f.startsWith('shop')) return 'shop';
    return 'home';
  }

  class SiteHeader extends HTMLElement {
    connectedCallback() {
      // Embedded (iframed into a course/book): render no header at all.
      if (new URLSearchParams(location.search).get('embed') === '1') { this.style.display = 'none'; return; }
      const active = this.getAttribute('active') || autoActive();
      const root = this.attachShadow({ mode: 'open' });
      const tab = ([key, label, href, cls, ext]) =>
        `<a class="tab ${cls || ''}${key === active ? ' active' : ''}" href="${href}"${ext ? ' target="_blank" rel="noopener"' : ''}>${label}</a>`;
      // Dropdown menu item (used inside the Views menu) — highlights the current page.
      const menuItem = ([key, label, href, cls, ext]) =>
        `<a class="${key === active ? 'on' : ''}" href="${href}"${ext ? ' target="_blank" rel="noopener"' : ''}>${label}</a>`;
      const VIEW_KEYS = ['explorer', 'cards', 'lenses', 'tree', 'treeoflife', 'timeline', 'genealogy'];
      const viewActive = VIEW_KEYS.includes(active);
      root.innerHTML = `
        <style>
          :host{ display:block; position:sticky; top:0; z-index:50;
                 background:#0f0d17; padding:0; margin:0; border:0; font-size:14px;
                 transition:transform .25s ease; will-change:transform; }
          @media (prefers-reduced-motion: reduce){ :host{ transition:none; } .tab, .dd-menu a, .brand{ transition:none !important; } }
          .bar{
            display:flex; align-items:center; gap:14px; flex-wrap:wrap;
            padding:11px 18px; background:#0f0d17;
            border-bottom:1px solid #2a2440;
            font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
          }
          .brand{ display:flex; flex-direction:row; align-items:center; gap:9px; margin-right:4px; }
          .brand-logo, .brand-name{ display:inline-flex; align-items:center; text-decoration:none; }
          .brand-logo{ border-radius:50%; }
          .brand-name .name{ font-size:15px; font-weight:800; letter-spacing:.3px; color:#ece8f5; white-space:nowrap; }
          .brand-name:hover .name{ color:#fff; }
          .brand-name .name .gold{ color:#d4af37; }
          .brand svg{ flex-shrink:0; }
          .spacer{ flex:1 1 auto; }
          nav{ display:flex; gap:6px; flex-wrap:wrap; align-items:center; }
          .cap{ font-size:9.5px; text-transform:uppercase; letter-spacing:.14em;
                color:#5f5878; margin:0 2px 0 6px; user-select:none; }
          .cap.card-cap{ color:#b8860b; }
          .cap.gram-cap{ color:#6d4fa8; }
          .sep{ width:1px; height:20px; background:#2a2440; margin:0 6px; }
          .tab{
            color:#a99fc6; text-decoration:none; font-size:13px; font-weight:500;
            padding:6px 11px; border-radius:8px; white-space:nowrap; transition:.15s;
            border:1px solid transparent;
          }
          .tab:hover{ color:#ece8f5; background:#1d1830; }
          .tab.active{ color:#fff !important; background:#9333ea; font-weight:700; border-color:#9333ea; }
          /* tools — colour-coded, pill-outlined (a different nature than the views) */
          .t-caster{ color:#b9a3f5; border-color:rgba(139,92,246,.45); }
          .t-caster:hover{ color:#d4c5ff; background:rgba(139,92,246,.12); }
          .t-course{ color:#9ad0b5; border-color:rgba(129,178,154,.45); }
          .t-course:hover{ color:#bfe8d2; background:rgba(129,178,154,.10); }
          .t-shop{ color:#e7c96a; border-color:rgba(212,175,55,.5); }
          .t-shop:hover{ color:#f4dd92; background:rgba(212,175,55,.10); }
          .t-github{ color:#8f87a8; border-color:transparent; border-bottom:1px dashed #3a3450; border-radius:0; }
          .t-github:hover{ color:#cfc8e2; background:transparent; }
          /* Courses dropdown */
          .dd{ position:relative; }
          .dd-btn{ background:none; font-family:inherit; cursor:pointer; }
          .dd-menu{ position:absolute; top:calc(100% + 6px); right:0; min-width:230px;
            background:#15101f; border:1px solid #3a3450; border-radius:10px; padding:6px;
            box-shadow:0 12px 32px rgba(0,0,0,.5); display:none; z-index:60; }
          .dd:hover .dd-menu, .dd:focus-within .dd-menu{ display:block; }
          .dd-menu a{ display:block; color:#cdbff0; text-decoration:none; font-size:13px;
            padding:8px 10px; border-radius:7px; white-space:nowrap; }
          .dd-menu a:hover{ background:#241e38; color:#fff; }
          .dd-menu a.on{ color:#fff; background:#2b2442; font-weight:600; }
          .dd-cap{ display:block; font-size:9px; text-transform:uppercase; letter-spacing:.14em;
            color:#5f5878; padding:8px 10px 3px; user-select:none; }
          .dd-cap:first-child{ padding-top:2px; }
          @media (max-width:680px){
            .brand .sub{ display:none; }
            .tab{ padding:5px 8px; font-size:12px; }
            .cap{ display:none; } .sep{ display:none; }
          }
        </style>
        <div class="bar">
          <span class="brand">
            <a class="brand-logo" href="https://recursive.eco" target="_blank" rel="noopener" title="Part of recursive.eco — the parent project" aria-label="recursive.eco — the parent project">
              <span style="display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;background:#fff;border-radius:50%;flex-shrink:0"><img src="${PFX}recursive-logo.svg" width="30" height="30" alt="" aria-hidden="true" style="display:block"></span>
            </a>
            <a class="brand-name" href="${PFX}index.html" title="The Recursive Tarot — home">
              <span class="name">The <span class="gold">Recursive Tarot</span></span>
            </a>
          </span>
          <span class="spacer"></span>
          <nav aria-label="Site sections">
            <span class="dd">
              <a class="tab dd-btn${viewActive ? ' active' : ''}" role="button" tabindex="0" aria-haspopup="true" aria-expanded="false" aria-label="Views menu">⊞ Views ▾</a>
              <span class="dd-menu">
                <span class="dd-cap">🃏 By card</span>
                ${CARD_VIEWS.map(menuItem).join('')}
                <span class="dd-cap">⊞ Across the collection</span>
                ${GRAMMAR_VIEWS.map(menuItem).join('')}
              </span>
            </span>
            <span class="dd">
              <a class="tab t-course dd-btn${active === 'course' ? ' active' : ''}" role="button" tabindex="0" aria-haspopup="true" aria-expanded="false" aria-label="Courses menu">📓 Courses ▾</a>
              <span class="dd-menu">
                ${COURSES.map(([id, label]) => `<a href="${PFX}pages/course-viewer.html?course=${id}">${label}</a>`).join('')}
                <a href="${PFX}pages/sources.html" style="border-top:1px solid #3a3450;margin-top:4px;padding-top:9px">📚 All courses &amp; sources →</a>
              </span>
            </span>
            <span class="dd">
              <a class="tab t-caster dd-btn${active === 'play' ? ' active' : ''}" href="${PFX}pages/play.html" aria-haspopup="true" aria-expanded="false" aria-label="Play menu">🎴 Play ▾</a>
              <span class="dd-menu">
                ${PLAY_MENU.map(([href, label, ext]) => `<a href="${href}"${ext ? ' target="_blank" rel="noopener"' : ''}>${label}</a>`).join('')}
              </span>
            </span>
            ${TOOLS.map(tab).join('')}
            <recursive-auth></recursive-auth>
          </nav>
        </div>`;

      // Dropdowns: keyboard + ARIA on top of the hover/focus-within CSS.
      root.querySelectorAll('.dd').forEach(dd => {
        const btn = dd.querySelector('.dd-btn');
        const set = open => btn && btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        dd.addEventListener('mouseenter', () => set(true));
        dd.addEventListener('mouseleave', () => set(false));
        dd.addEventListener('focusin', () => set(true));
        dd.addEventListener('focusout', () => { if (!dd.matches(':focus-within')) set(false); });
        dd.addEventListener('keydown', e => {
          if (e.key === 'Escape') { set(false); btn && btn.focus(); }
          // Enter/Space opens the menu when the trigger has no own link to follow
          if ((e.key === 'Enter' || e.key === ' ') && e.target === btn && !btn.getAttribute('href')) {
            const first = dd.querySelector('.dd-menu a'); if (first) { e.preventDefault(); set(true); first.focus(); }
          }
        });
      });

      // Auto-hide on scroll down, reveal on scroll up — but never while the nav has keyboard focus.
      let lastY = window.scrollY || 0, host = this;
      window.addEventListener('scroll', () => {
        const y = window.scrollY || 0;
        const hide = y > 90 && y > lastY + 4 && !host.matches(':focus-within');
        host.style.transform = hide ? 'translateY(-100%)' : 'translateY(0)';
        lastY = y;
      }, { passive: true });
    }
  }
  customElements.define('site-header', SiteHeader);
})();
