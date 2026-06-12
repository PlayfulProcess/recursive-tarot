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

  // Path back to the repo root: '../' from any subdir (viewers/ OR pages/), '' at root.
  const inSub = /\/(viewers|pages)\//.test(location.pathname);
  const PFX = inSub ? '../' : '';

  // Shared-identity widget (reads the .recursive.eco session cookie; L1 of the
  // integration ladder). Loaded once; renders as <recursive-auth> in the bar.
  if (!document.querySelector('script[data-recursive-auth]')) {
    const s = document.createElement('script');
    s.src = PFX + 'auth-widget.js?v=2';
    s.dataset.recursiveAuth = '1';
    document.head.appendChild(s);
  }

  // [key, label, href]
  const VIEWS = [
    ['cards',      'Cards',        PFX + 'viewers/cards.html'],
    ['explorer',   'Explorer',     PFX + 'viewers/explorer.html'],
    ['treeoflife', 'Tree of Life', PFX + 'viewers/genealogy-tree.html'],
    ['timeline',   'Timeline',     PFX + 'viewers/timeline.html'],
    ['tree',       'Tree',         PFX + 'viewers/tree-viewer.html'],
    ['genealogy',  'Genealogy',    PFX + 'genealogy.html'],
  ];
  // [key, label, href, cssClass, external?]
  const TOOLS = [
    ['caster', '🔮 Caster',  PFX + 'viewers/caster.html',      't-caster'],
    ['course', '📓 Course',  PFX + 'pages/course-viewer.html', 't-course'],
    ['shop',   '🛒 Shop',    PFX + 'pages/shop.html',          't-shop'],
    ['github', 'GitHub ↗',  'https://github.com/PlayfulProcess/recursive-tarot', 't-github', true],
  ];

  function autoActive() {
    const f = location.pathname.split('/').pop() || 'index.html';
    if (f.startsWith('cards')) return 'cards';
    if (f.startsWith('explorer')) return 'explorer';
    if (f.startsWith('genealogy-tree')) return 'treeoflife';
    if (f.startsWith('timeline')) return 'timeline';
    if (f.startsWith('tree-viewer')) return 'tree';
    if (f.startsWith('caster')) return 'caster';
    if (f.startsWith('genealogy')) return 'genealogy';
    if (f.startsWith('course')) return 'course';
    if (f.startsWith('shop')) return 'shop';
    return 'home';
  }

  class SiteHeader extends HTMLElement {
    connectedCallback() {
      const active = this.getAttribute('active') || autoActive();
      const root = this.attachShadow({ mode: 'open' });
      const tab = ([key, label, href, cls, ext]) =>
        `<a class="tab ${cls || ''}${key === active ? ' active' : ''}" href="${href}"${ext ? ' target="_blank" rel="noopener"' : ''}>${label}</a>`;
      root.innerHTML = `
        <style>
          :host{ display:block; position:sticky; top:0; z-index:50;
                 background:#0f0d17; padding:0; margin:0; border:0; font-size:14px; }
          .bar{
            display:flex; align-items:center; gap:14px; flex-wrap:wrap;
            padding:11px 18px; background:#0f0d17;
            border-bottom:1px solid #2a2440;
            font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
          }
          .brand{ display:flex; flex-direction:row; align-items:center; gap:8px; text-decoration:none; margin-right:4px; }
          .brand .wordmark{ display:flex; flex-direction:column; line-height:1.05; }
          .brand .name{ font-size:15px; font-weight:800; letter-spacing:.3px; color:#ece8f5; white-space:nowrap; }
          .brand .name .gold{ color:#d4af37; }
          .brand .sub{ font-size:10px; color:#7c7596; letter-spacing:.02em; }
          .brand .sub a{ color:#9b8fc4; text-decoration:none; }
          .brand svg{ flex-shrink:0; }
          .spacer{ flex:1 1 auto; }
          nav{ display:flex; gap:6px; flex-wrap:wrap; align-items:center; }
          .cap{ font-size:9.5px; text-transform:uppercase; letter-spacing:.14em;
                color:#5f5878; margin:0 2px 0 6px; user-select:none; }
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
          @media (max-width:680px){
            .brand .sub{ display:none; }
            .tab{ padding:5px 8px; font-size:12px; }
            .cap{ display:none; } .sep{ display:none; }
          }
        </style>
        <div class="bar">
          <a class="brand" href="${PFX}index.html">
            <img src="${PFX}recursive-logo.svg" width="28" height="28" alt="" aria-hidden="true" style="display:block;flex-shrink:0">
            <span class="wordmark">
              <span class="name">The <span class="gold">Recursive Tarot</span></span>
              <span class="sub">part of <a href="https://recursive.eco" target="_blank" rel="noopener">recursive.eco</a></span>
            </span>
          </a>
          <span class="spacer"></span>
          <nav>
            <span class="cap" title="Different previews of the same decks">◫ views</span>
            ${VIEWS.map(tab).join('')}
            <span class="sep"></span>
            ${TOOLS.map(tab).join('')}
            <recursive-auth></recursive-auth>
          </nav>
        </div>`;
    }
  }
  customElements.define('site-header', SiteHeader);
})();
