/* deck-picker.js — shared deck multiselect popover for cards + explorer.
 * Usage:
 *   DeckPicker.open(anchorEl, { collection, selected: ['slug',...], onLoad(slugs) {} })
 * collection = parsed _collection.json  (needs collection.grammars[])
 * selected   = currently active slug array (for checkmarks)
 * onLoad     = called with the chosen slug array when user clicks "Load selected"
 *
 * Oct 14 2026 (her report: "a weird black bar, not scrolling right, not fixing to the decks
 * dropdown"). Three causes, fixed here:
 *  - the search box kept a dark-theme fill (#110e1d): every colour now comes from theme.css
 *    tokens (light only, CLAUDE.md "Theme & colour"), with the old values as fallbacks;
 *  - the list is a flex child without min-height:0, so it grew past the popover's max-height
 *    instead of scrolling, and pushed All / None / Load off the bottom;
 *  - the popover was position:fixed at the button's on-screen spot, so it stayed put while the
 *    page scrolled. It is now absolute in page coordinates, under its button, and re-placed on
 *    resize. Its height fits the room below the button (or it opens above when there is none).
 */
(function (global) {
  'use strict';

  const T = (name, fallback) => `var(${name}, ${fallback})`;
  const GAP = 6;       // px between the button and the popover
  const MARGIN = 12;   // px kept clear of the viewport edges
  const WIDTH = 300;

  const POP_STYLE = [
    'position:absolute', 'z-index:9001', 'box-sizing:border-box',
    `background:${T('--surface', '#ffffff')}`,
    `border:1px solid ${T('--line-soft', '#cfc8ba')}`, 'border-radius:10px', 'padding:10px',
    'box-shadow:0 14px 30px -12px rgba(60,45,20,.45)',
    `width:${WIDTH}px`, 'max-width:calc(100vw - 24px)',
    'display:flex', 'flex-direction:column', 'gap:6px',
    `font-family:${T('--sans', 'Inter,system-ui,sans-serif')}`
  ].join(';');

  // Place the popover under its anchor (above it when the room below is too small), in page
  // coordinates so it scrolls with the page, and size it to the room it has.
  function place(pop, anchor) {
    const r = anchor.getBoundingClientRect();
    const vw = document.documentElement.clientWidth;
    const vh = window.innerHeight;
    const width = Math.min(WIDTH, vw - 2 * MARGIN);
    const below = vh - r.bottom - GAP - MARGIN;
    const above = r.top - GAP - MARGIN;
    const openUp = below < 240 && above > below;
    const room = Math.max(180, Math.min(vh * 0.7, openUp ? above : below));
    pop.style.maxHeight = room + 'px';
    // Right-align with the button when it sits on the right half of the page.
    let left = r.left + r.width / 2 > vw / 2 ? r.right - width : r.left;
    left = Math.max(MARGIN, Math.min(left, vw - width - MARGIN));
    pop.style.left = (left + window.scrollX) + 'px';
    pop.style.top = openUp
      ? (r.top + window.scrollY - GAP - pop.offsetHeight) + 'px'
      : (r.bottom + window.scrollY + GAP) + 'px';
  }

  let current = null;   // { anchor, close } of the open popover

  function open(anchor, { collection, selected, onLoad }) {
    // A second click on the same button closes it; any other open popover goes first.
    if (current) {
      const same = current.anchor === anchor;
      current.close();
      if (same) return null;
    }
    document.querySelectorAll('.dp-pop').forEach(p => p.remove());
    const sel = new Set(selected || []);
    const decks = (collection?.grammars || [])
      .filter(g => !g.is_meta && g.slug !== 'tree-of-tarot')
      .sort((a, b) => (a.year ?? 9999) - (b.year ?? 9999) ||
                      (a.name || '').localeCompare(b.name || ''));

    const pop = document.createElement('div');
    pop.className = 'dp-pop';
    pop.setAttribute('role', 'dialog');
    pop.setAttribute('aria-label', 'Pick decks to load');
    pop.style.cssText = POP_STYLE;

    const hint = document.createElement('p');
    hint.style.cssText = `margin:0;font-size:11.5px;color:${T('--mut', '#6b6457')};line-height:1.45`;
    hint.innerHTML = 'Tick <b>several decks</b> and Load — patterns appear when collections overlap.';
    pop.appendChild(hint);

    const search = document.createElement('input');
    search.type = 'search'; search.placeholder = 'search decks…';
    search.setAttribute('aria-label', 'Search decks');
    search.style.cssText = `width:100%;padding:6px 9px;background:${T('--paper', '#faf8f3')};border:1px solid ${T('--line-soft', '#cfc8ba')};border-radius:6px;color:${T('--ink', '#221f1a')};font:inherit;font-size:12.5px;box-sizing:border-box;flex-shrink:0;outline-color:${T('--gold', '#9a7322')}`;
    pop.appendChild(search);

    const list = document.createElement('div');
    // min-height:0 is what lets a flex child scroll inside a max-height parent.
    list.style.cssText = 'overflow-y:auto;flex:1 1 auto;min-height:0;overscroll-behavior:contain;margin:0 -4px;padding:0 4px;';
    decks.forEach(g => {
      const label = document.createElement('label');
      label.style.cssText = `display:flex;align-items:center;gap:6px;padding:4px 6px;border-radius:4px;cursor:pointer;font-size:12.5px;color:${T('--ink-soft', '#4a4439')};`;
      label.onmouseenter = () => { label.style.background = T('--chip', '#faf3e6'); };
      label.onmouseleave = () => { label.style.background = ''; };
      const cb = document.createElement('input');
      cb.type = 'checkbox'; cb.value = g.slug; cb.checked = sel.has(g.slug);
      cb.style.accentColor = T('--gold', '#9a7322');
      const name = document.createElement('span');
      name.textContent = g.name.split(' — ')[0].slice(0, 34);
      label.append(cb, name);
      if (g.year_label) {
        const yr = document.createElement('span');
        yr.textContent = '(' + g.year_label + ')';
        yr.style.cssText = `margin-left:auto;padding-left:8px;color:${T('--faint', '#8a8273')};font-size:11px;white-space:nowrap;`;
        label.appendChild(yr);
      }
      list.appendChild(label);
    });
    pop.appendChild(list);

    search.oninput = e => {
      const q = e.target.value.toLowerCase();
      list.querySelectorAll('label').forEach(l => {
        l.style.display = l.textContent.toLowerCase().includes(q) ? '' : 'none';
      });
    };

    const btns = document.createElement('div');
    btns.style.cssText = 'display:flex;gap:6px;flex-shrink:0;flex-wrap:wrap;';

    const mkBtn = (text, fn, isPrimary) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = text;
      b.style.cssText = `flex:1;padding:5px 8px;border-radius:6px;font:inherit;font-size:12px;white-space:nowrap;cursor:pointer;${
        isPrimary
          ? `background:${T('--gold', '#9a7322')};border:1px solid ${T('--gold', '#9a7322')};color:#fff;`
          : `background:transparent;border:1px solid ${T('--line-soft', '#cfc8ba')};color:${T('--ink-soft', '#4a4439')};`
      }`;
      b.onclick = fn;
      return b;
    };

    btns.appendChild(mkBtn('All', () => list.querySelectorAll('input[type=checkbox]').forEach(i => { i.checked = true; })));
    btns.appendChild(mkBtn('None', () => list.querySelectorAll('input[type=checkbox]').forEach(i => { i.checked = false; })));
    btns.appendChild(mkBtn('Load selected', () => {
      const v = [...list.querySelectorAll('input[type=checkbox]:checked')].map(i => i.value);
      close();
      onLoad(v);
    }, true));
    pop.appendChild(btns);

    document.body.appendChild(pop);
    place(pop, anchor);
    anchor.setAttribute('aria-expanded', 'true');
    search.focus({ preventScroll: true });

    const onResize = () => place(pop, anchor);
    const onKey = e => { if (e.key === 'Escape') { close(); anchor.focus(); } };
    function onDocClick(e) {
      if (!pop.contains(e.target) && !anchor.contains(e.target)) close();
    }
    function close() {
      if (current && current.pop === pop) current = null;
      pop.remove();
      anchor.setAttribute('aria-expanded', 'false');
      window.removeEventListener('resize', onResize);
      document.removeEventListener('keydown', onKey);
      document.removeEventListener('click', onDocClick);
    }
    current = { anchor, pop, close };
    window.addEventListener('resize', onResize);
    document.addEventListener('keydown', onKey);
    setTimeout(() => document.addEventListener('click', onDocClick), 10);

    return pop;
  }

  global.DeckPicker = { open };
})(window);
