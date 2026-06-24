/* Shared card-detail modal for the game pages (Tarocchino / Trionfi / Ma Diao).
   One light-themed inspector, included by every game so a card looks the same
   wherever you click it — in the hand, on the table, or in the play log.
   API:  GameCard.show({ img, title, lines:[[k,v],...], href, linkText })
         GameCard.close()
   Light-only, uses theme.css tokens (no dark blocks) per the project theme rule. */
(function () {
  if (window.GameCard) return;
  let root, imgEl, titleEl, metaEl, linkEl;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function build() {
    const css = `
.gcd-ov{position:fixed;inset:0;background:rgba(20,16,28,.5);display:none;align-items:center;justify-content:center;z-index:1000;padding:20px}
.gcd-ov.open{display:flex}
.gcd-panel{background:var(--panel,#fff);color:var(--ink,#221f1a);border:1px solid var(--line,#ddd);border-radius:14px;max-width:360px;width:100%;max-height:88vh;overflow:auto;box-shadow:0 20px 60px rgba(0,0,0,.28);padding:18px;font-family:Inter,system-ui,sans-serif}
.gcd-x{float:right;cursor:pointer;font-size:22px;line-height:1;color:var(--muted,#888);border:0;background:none;padding:0}
.gcd-img{display:block;width:62%;max-width:200px;margin:2px auto 12px;border-radius:8px;background:var(--panel2,#f4f1ea)}
.gcd-img[src=""]{display:none}
.gcd-title{font-size:18px;font-weight:700;margin:.1em 0 .55em;text-align:center;line-height:1.25}
.gcd-meta{list-style:none;margin:0 0 12px;padding:0;font-size:13px}
.gcd-meta li{display:flex;justify-content:space-between;gap:14px;padding:5px 1px;border-bottom:1px solid var(--line,#eee)}
.gcd-meta .k{color:var(--muted,#888);text-transform:uppercase;font-size:10px;letter-spacing:.06em;align-self:center}
.gcd-meta .v{font-weight:700;text-align:right}
.gcd-link{display:inline-block;margin-top:2px;font-size:13px;color:var(--accent,#9a7322);text-decoration:none;font-weight:600}
.gcd-link:hover{text-decoration:underline}`;
    const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    root = document.createElement('div'); root.className = 'gcd-ov';
    root.innerHTML = `<div class="gcd-panel" role="dialog" aria-modal="true">
      <button class="gcd-x" aria-label="Close">×</button>
      <img class="gcd-img" alt="">
      <div class="gcd-title"></div>
      <ul class="gcd-meta"></ul>
      <a class="gcd-link" target="_blank" rel="noopener" style="display:none"></a>
    </div>`;
    document.body.appendChild(root);
    imgEl = root.querySelector('.gcd-img'); titleEl = root.querySelector('.gcd-title');
    metaEl = root.querySelector('.gcd-meta'); linkEl = root.querySelector('.gcd-link');
    root.addEventListener('click', e => { if (e.target === root || e.target.classList.contains('gcd-x')) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  }

  function show(o) {
    if (!root) build();
    o = o || {};
    if (o.img) { imgEl.src = o.img; imgEl.style.display = ''; } else { imgEl.removeAttribute('src'); imgEl.style.display = 'none'; }
    titleEl.textContent = o.title || '';
    metaEl.innerHTML = (o.lines || [])
      .filter(l => l && l[1] != null && l[1] !== '')
      .map(l => `<li><span class="k">${esc(l[0])}</span><span class="v">${esc(l[1])}</span></li>`).join('');
    if (o.href) { linkEl.href = o.href; linkEl.textContent = o.linkText || 'Open in the deck viewer →'; linkEl.style.display = ''; }
    else linkEl.style.display = 'none';
    root.classList.add('open');
  }
  function close() { root && root.classList.remove('open'); }
  window.GameCard = { show, close };
})();
