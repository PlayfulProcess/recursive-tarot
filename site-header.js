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
    ['lenses',   'Lenses', PFX + 'viewers/prototypes/lenses.html'],
    ['tree',     'Tree',     PFX + 'viewers/tree-viewer.html'],
  ];
  const GRAMMAR_VIEWS = [
    ['treeoflife', 'Tree of Life', PFX + 'viewers/genealogy-tree.html'],
    ['timeline',   'Timeline',     PFX + 'viewers/timeline.html'],
    ['genealogy',  'Genealogy',    PFX + 'genealogy.html'],
  ];
  // [key, label, href, cssClass, external?]
  const TOOLS = [
    ['contribute', 'Contribute', PFX + 'pages/contribute.html', 't-contribute'],
    ['shop',   'Shop',    PFX + 'pages/shop.html',          't-shop'],
    ['github', 'GitHub ↗',  'https://github.com/PlayfulProcess/recursive-tarot', 't-github', true],
  ];
  // Play — a dropdown of the games + readings (the pill itself links to the Play hub).
  const PLAY_MENU = [
    [PFX + 'pages/games/tarocchino.html', 'Tarocchino di Bologna'],
    [PFX + 'pages/games/madiao.html',     'Ma Diao 馬吊'],
    [PFX + 'pages/games/trionfi.html',    'Trionfi'],
    [PFX + 'viewers/caster.html',         'Caster'],
    [PFX + 'pages/spread-builder.html',   'Spread Builder'],
    ['https://flow.recursive.eco/',   'Oracle ↗', true],
    [PFX + 'pages/play.html',             'All games & readings →'],
  ];
  // Home — a dropdown that uncollapses to About (the pill itself links to the homepage).
  const HOME_MENU = [
    [PFX + 'index.html',        'Home'],
    [PFX + 'pages/about.html',  'About'],
    [PFX + 'pages/wishlist.html', 'Wish List'],
  ];
  // Courses — grouped into three topics; each is a course-viewer ?course=… (deep-linkable with #section).
  const COURSE_GROUPS = [
    ['History', [
      ['history-of-tarot',                'A History of Tarot'],
    ]],
    ['Reading the cards', [
      ['reading-the-cards',               'The full course — all 12 chapters'],
    ]],
    ['Tarot today', [
      ['tarot-today',                     'Tarot Today — a living question'],
    ]],
    ['How to Contribute', [
      ['how-to-contribute',               'How to Contribute'],
    ]],
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
    if (f.startsWith('contribute')) return 'contribute';
    return 'home';
  }

  class SiteHeader extends HTMLElement {
    connectedCallback() {
      // Embedded (iframed into a course/book): render no header at all.
      if (new URLSearchParams(location.search).get('embed') === '1') { this.style.display = 'none'; return; }
      // Museum/Editorial webfonts — injected once into the document head so every page
      // (light DOM and this shadow DOM) renders in Cormorant / Fraunces / Inter.
      if (!document.getElementById('rt-fonts')) {
        const fl = document.createElement('link'); fl.id = 'rt-fonts'; fl.rel = 'stylesheet';
        fl.href = 'https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600&display=swap';
        document.head.appendChild(fl);
      }
      // The shared SVG icon library — one source, available as <rt-icon name="…"> on every page.
      if (!document.getElementById('rt-icons-lib')) {
        const si = document.createElement('script'); si.id = 'rt-icons-lib'; si.src = PFX + 'icons.js';
        document.head.appendChild(si);
      }
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
                 background:#fbf9f3; padding:0; margin:0; border:0; font-size:14px;
                 transition:transform .25s ease; will-change:transform; }
          @media (prefers-reduced-motion: reduce){ :host{ transition:none; } .tab, .dd-menu a, .brand{ transition:none !important; } }
          .bar{
            display:flex; align-items:center; gap:14px; flex-wrap:wrap;
            padding:13px 20px; background:#fbf9f3;
            border-bottom:1px solid #d8d2c6;
            font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;
          }
          .brand{ display:flex; flex-direction:row; align-items:center; gap:10px; margin-right:4px; }
          .brand-logo, .brand-name{ display:inline-flex; align-items:center; text-decoration:none; }
          .brand-logo{ border-radius:50%; }
          .brand-name .name{ font-family:"Fraunces",Georgia,serif; font-size:21px; font-weight:600; letter-spacing:.4px; color:#221f1a; white-space:nowrap; }
          .brand-name:hover .name{ color:#000; }
          .brand-name .name .gold{ color:#9a7322; }
          .brand svg{ flex-shrink:0; }
          .spacer{ flex:1 1 auto; }
          nav{ display:flex; gap:4px; flex-wrap:wrap; align-items:center; }
          .cap{ font-size:9.5px; text-transform:uppercase; letter-spacing:.16em;
                color:#8a8273; margin:0 2px 0 6px; user-select:none; }
          .cap.card-cap{ color:#9a7322; }
          .cap.gram-cap{ color:#6b6457; }
          .sep{ width:1px; height:20px; background:#d8d2c6; margin:0 6px; }
          /* one restrained editorial language for every nav item — text links,
             gold on hover, a hairline underline when active. No pills, no per-tool colour. */
          .tab{
            color:#6b6457; text-decoration:none; font-size:13px; font-weight:500;
            padding:7px 9px; white-space:nowrap; transition:color .15s;
            border:0; border-bottom:1.5px solid transparent; border-radius:0;
          }
          .tab:hover{ color:#9a7322; }
          .tab.active{ color:#9a7322; font-weight:600; border-bottom-color:#9a7322; }
          .t-caster,.t-course,.t-shop,.t-github,.t-contribute{ color:#6b6457; border:0; border-bottom:1.5px solid transparent; border-radius:0; }
          .t-caster:hover,.t-course:hover,.t-shop:hover,.t-github:hover,.t-contribute:hover{ color:#9a7322; background:transparent; }
          /* dropdowns */
          .dd{ position:relative; }
          .dd-btn{ background:none; font-family:inherit; cursor:pointer; }
          .dd-btn::after{ content:""; display:inline-block; width:5px; height:5px; margin-left:7px;
            border-right:1.4px solid currentColor; border-bottom:1.4px solid currentColor;
            transform:rotate(45deg) translateY(-2px); opacity:.5; }
          .dd-menu{ position:absolute; top:calc(100% + 8px); right:0; min-width:220px;
            max-width:min(300px,calc(100vw - 24px)); background:#ffffff; border:1px solid #d8d2c6;
            border-radius:8px; padding:7px; box-shadow:0 16px 44px -18px rgba(60,45,20,.45); display:none; z-index:60; }
          @media (max-width:760px){ .dd-menu{ position:fixed; left:12px; right:12px; top:54px; min-width:0; max-width:none; } }
          .dd:hover .dd-menu, .dd:focus-within .dd-menu{ display:block; }
          .dd-menu a{ display:block; color:#4a4439; text-decoration:none; font-size:13px;
            padding:8px 10px; border-radius:7px; white-space:nowrap; }
          .dd-menu a:hover{ background:#f1ece1; color:#221f1a; }
          .dd-menu a[href*="recursive.eco"]{ color:#9333ea; }
          .dd-menu a.on{ color:#221f1a; background:#f1ece1; font-weight:600; }
          .dd-cap{ display:block; font-family:Inter,sans-serif; font-size:9px; text-transform:uppercase; letter-spacing:.16em;
            color:#8a8273; padding:8px 10px 3px; user-select:none; }
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
              <span style="display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;background:#fff;border-radius:50%;flex-shrink:0"><img src="${PFX}public/spiral-purple.svg" width="30" height="30" alt="" aria-hidden="true" style="display:block"></span>
            </a>
            <a class="brand-name" href="${PFX}index.html" title="The Recursive Tarot — home">
              <span class="name">The <span class="gold">Recursive Tarot</span></span>
            </a>
          </span>
          <span class="spacer"></span>
          <nav aria-label="Site sections">
            <span class="dd">
              <a class="tab dd-btn${active === 'home' ? ' active' : ''}" href="${PFX}index.html" aria-haspopup="true" aria-expanded="false" aria-label="Home menu">Home</a>
              <span class="dd-menu">
                ${HOME_MENU.map(([href, label]) => `<a href="${href}">${label}</a>`).join('')}
              </span>
            </span>
            <span class="dd">
              <a class="tab dd-btn${viewActive ? ' active' : ''}" role="button" tabindex="0" aria-haspopup="true" aria-expanded="false" aria-label="Views menu">Views</a>
              <span class="dd-menu">
                <span class="dd-cap">By card</span>
                ${CARD_VIEWS.map(menuItem).join('')}
                <span class="dd-cap">Across the collection</span>
                ${GRAMMAR_VIEWS.map(menuItem).join('')}
              </span>
            </span>
            <span class="dd">
              <a class="tab t-course dd-btn${active === 'course' ? ' active' : ''}" role="button" tabindex="0" aria-haspopup="true" aria-expanded="false" aria-label="Courses menu">Courses</a>
              <span class="dd-menu">
                ${COURSE_GROUPS.map(([cap, items]) => `<span class="dd-cap">${cap}</span>` + items.map(([id, label]) => `<a href="${PFX}pages/course-viewer.html?course=${id}">${label}</a>`).join('')).join('')}
                <a href="${PFX}pages/sources.html" style="border-top:1px solid #d8d2c6;margin-top:4px;padding-top:9px">All courses &amp; sources →</a>
              </span>
            </span>
            <span class="dd">
              <a class="tab t-caster dd-btn${active === 'play' ? ' active' : ''}" href="${PFX}pages/play.html" aria-haspopup="true" aria-expanded="false" aria-label="Play menu">Play</a>
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
