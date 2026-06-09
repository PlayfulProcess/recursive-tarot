/* Shared site header for the Recursive Tarot static site.
 * One definition, used by every page (root + viewers/). Style-isolated via
 * Shadow DOM so each viewer's own CSS can't override it. Path-aware so links
 * resolve from both the repo root and the /viewers/ subdir.
 *
 * Usage:  <script src="<path-to>/site-header.js"></script>
 *         <site-header active="cards"></site-header>
 * The `active` attribute highlights the matching tab; if omitted it is
 * auto-detected from the filename.
 */
(function () {
  if (customElements.get('site-header')) return;

  const inViewers = location.pathname.includes('/viewers/');
  const toRoot = inViewers ? '../' : '';
  const toViewers = inViewers ? '' : 'viewers/';

  // [key, label, href, external?]
  const TABS = [
    ['cards',      'Cards',        toViewers + 'cards.html'],
    ['treeoflife', 'Tree of Life', toViewers + 'genealogy-tree.html'],
    ['timeline',   'Timeline',     toViewers + 'timeline.html'],
    ['tree',       'Tree',         toViewers + 'tree-viewer.html'],
    ['caster',     'Caster',       toViewers + 'caster.html'],
    ['genealogy',  'Genealogy',    toRoot + 'genealogy.html'],
    ['course',     'Course',       toRoot + 'pages/course.html'],
    ['github',     'GitHub ↗', 'https://github.com/PlayfulProcess/recursive-tarot', true],
  ];

  function autoActive() {
    const f = location.pathname.split('/').pop() || 'index.html';
    if (f.startsWith('cards')) return 'cards';
    if (f.startsWith('genealogy-tree')) return 'treeoflife';
    if (f.startsWith('timeline')) return 'timeline';
    if (f.startsWith('tree-viewer')) return 'tree';
    if (f.startsWith('caster')) return 'caster';
    if (f.startsWith('genealogy')) return 'genealogy';
    return 'home';
  }

  class SiteHeader extends HTMLElement {
    connectedCallback() {
      const active = this.getAttribute('active') || autoActive();
      const root = this.attachShadow({ mode: 'open' });
      const tabs = TABS.map(([key, label, href, ext]) =>
        `<a class="tab${key === active ? ' active' : ''}" href="${href}"${ext ? ' target="_blank" rel="noopener"' : ''}>${label}</a>`
      ).join('');
      root.innerHTML = `
        <style>
          :host{ display:block; position:sticky; top:0; z-index:50;
                 background:#0f0d17; padding:0; margin:0; border:0; font-size:14px; }
          .bar{
            display:flex; align-items:center; gap:16px; flex-wrap:wrap;
            padding:11px 18px; background:#0f0d17;
            border-bottom:1px solid #2a2440;
            font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
          }
          .brand{ display:flex; flex-direction:column; line-height:1.05; text-decoration:none; margin-right:4px; }
          .brand .name{ font-size:15px; font-weight:800; letter-spacing:.3px; color:#ece8f5; white-space:nowrap; }
          .brand .name .gold{ color:#d4af37; }
          .brand .sub{ font-size:10px; color:#7c7596; letter-spacing:.02em; }
          .brand .sub a{ color:#9b8fc4; text-decoration:none; }
          .spacer{ flex:1 1 auto; }
          nav{ display:flex; gap:6px; flex-wrap:wrap; align-items:center; }
          .tab{
            color:#a99fc6; text-decoration:none; font-size:13px; font-weight:500;
            padding:6px 11px; border-radius:8px; white-space:nowrap; transition:.15s;
          }
          .tab:hover{ color:#ece8f5; background:#1d1830; }
          .tab.active{ color:#0f0d17; background:#d4af37; font-weight:700; }
          @media (max-width:560px){
            .brand .sub{ display:none; }
            .tab{ padding:5px 8px; font-size:12px; }
          }
        </style>
        <div class="bar">
          <a class="brand" href="${toRoot}index.html">
            <span class="name">The <span class="gold">Recursive Tarot</span></span>
            <span class="sub">part of <a href="https://recursive.eco" target="_blank" rel="noopener">recursive.eco</a></span>
          </a>
          <span class="spacer"></span>
          <nav>${tabs}</nav>
        </div>`;
    }
  }
  customElements.define('site-header', SiteHeader);
})();
