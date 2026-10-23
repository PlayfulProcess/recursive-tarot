// The Cards and Tree views moved to the archive on Oct 20 2026. Since Oct 23 2026 their old
// addresses (viewers/cards.html, viewers/tree-viewer.html) open the same deck in recursive.eco's
// Play instead: ?src=../tarot/<slug>/grammar.json finds the deck's id in tarot/_eco_ids.json, and
// ?item=<node id> opens that card (the ids are the same there). No ?src= opens the all-decks grammar.
// A deck that is not public on recursive.eco, or any other query, still opens the archived page.
// The script tag carries data-archive (the archived page) and data-pane (cards | tree).
(function () {
  const tag = document.currentScript.dataset;
  const q = new URLSearchParams(location.search);
  const toArchive = () => location.replace(tag.archive + location.search + location.hash);
  const src = q.get('src');
  const m = src && src.match(/tarot\/([^/]+)\/grammar\.json$/);
  const slug = m ? m[1] : (!src && !location.search ? 'all-decks-many-lenses' : null);
  if (!slug) return toArchive();
  fetch('../tarot/_eco_ids.json', { cache: 'no-cache' })
    .then(r => r.json())
    .then(d => {
      const id = d.ids[slug];
      if (!id || !d._public_now.includes(slug)) return toArchive();
      const item = q.get('item');
      location.replace('https://recursive.eco/play?id=' + id +
        (item ? '&pane=one&node=' + encodeURIComponent(item) : '&pane=' + tag.pane));
    })
    .catch(toArchive);
})();
