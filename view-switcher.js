/* Shared "eye" view-switcher for the Recursive Tarot static site.
 * One eye icon that flips the current grammar through every view (Cards, Tree,
 * Thumbnails, Timeline, Tree of Life, Genealogy, Print). Preserves the loaded
 * grammar (?src / ?github / ?id). Course is intentionally NOT here (it lives in
 * the header nav). Style-isolated via Shadow DOM.
 *
 * Usage:  <script src="<path>/view-switcher.js"></script>
 *         <view-switcher active="cards"></view-switcher>
 */
(function () {
  if (customElements.get('view-switcher')) return;

  const inViewers = location.pathname.includes('/viewers/');
  const toViewers = inViewers ? '' : 'viewers/';
  const toRoot = inViewers ? '../' : '';

  // preserve the loaded grammar across views
  const p = new URLSearchParams(location.search);
  const keep = new URLSearchParams();
  for (const k of ['src', 'github', 'id', 'type', 'item']) if (p.get(k)) keep.set(k, p.get(k));
  const qs = keep.toString() ? '?' + keep.toString() : '';
  const amp = keep.toString() ? '&' : '?';

  // [key, label, href]
  const VIEWS = [
    ['cards',      'Cards',        toViewers + 'cards.html' + qs],
    ['tree',       'Tree',         toViewers + 'tree-viewer.html' + qs],
    ['thumbnails', 'Thumbnails',   toViewers + 'cards.html' + qs + amp + 'layout=thumbnails'],
    ['timeline',   'Timeline',     toViewers + 'timeline.html' + qs],
    ['treeoflife', 'Tree of Life', toViewers + 'genealogy-tree.html' + qs],
    ['genealogy',  'Genealogy',    toRoot + 'genealogy.html'],
    ['print',      'Print',        toRoot + 'pages/print-viewer.html' + qs],
  ];

  const EYE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>';

  const VIEW_MAP = Object.fromEntries(VIEWS.map(([k, , href]) => [k, href]));

  class ViewSwitcher extends HTMLElement {
    connectedCallback() {
      const active = this.getAttribute('active') || '';
      // Portable deep-link: ?lens=<view> redirects to that lens, preserving
      // src/item (the target href already carries them; lens is dropped, no loop).
      const wantLens = p.get('lens');
      if (wantLens && wantLens !== active && VIEW_MAP[wantLens]) {
        location.replace(VIEW_MAP[wantLens]);
        return;
      }
      const root = this.attachShadow({ mode: 'open' });
      const items = VIEWS.map(([k, label, href]) =>
        `<a class="vs-item${k === active ? ' active' : ''}" href="${href}">${label}</a>`
      ).join('');
      root.innerHTML = `
        <style>
          :host{ display:inline-block; position:relative; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
          details{ position:relative; }
          summary{ list-style:none; cursor:pointer; display:inline-flex; align-items:center; gap:6px;
            padding:6px 11px; border:1px solid #3a3450; border-radius:8px; background:#1d1830; color:#cfc8e2;
            font-size:13px; font-weight:600; user-select:none; }
          summary::-webkit-details-marker{ display:none; }
          summary:hover{ border-color:#d4af37; color:#d4af37; }
          summary .cap{ font-size:12px; opacity:.85; }
          .menu{ position:absolute; top:calc(100% + 6px); left:0; z-index:60; min-width:170px;
            background:#161227; border:1px solid #3a3450; border-radius:10px; padding:6px; box-shadow:0 8px 24px rgba(0,0,0,.5); }
          .vs-item{ display:block; padding:7px 12px; border-radius:7px; text-decoration:none; color:#cfc8e2; font-size:13px; }
          .vs-item:hover{ background:#241d3a; color:#ece8f5; }
          .vs-item.active{ background:#d4af37; color:#0f0d17; font-weight:700; }
        </style>
        <details>
          <summary title="Switch view">${EYE}<span class="cap">View</span></summary>
          <div class="menu">${items}</div>
        </details>`;
      // close on outside click
      const det = root.querySelector('details');
      document.addEventListener('click', (e) => { if (!this.contains(e.target)) det.removeAttribute('open'); });
    }
  }
  customElements.define('view-switcher', ViewSwitcher);
})();
