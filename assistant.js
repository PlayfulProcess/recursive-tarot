/* The Recursive Tarot — the ONE recursive.eco assistant sidebar.
   <script src="assistant.js" defer></script>   (../assistant.js from pages/ or viewers/)

   NOT a copy of the assistant: this only loads the shared shell,
   https://recursive.eco/js/assistant-launcher.js, which iframes the flow app's
   /assistant embed — the exact same star FAB and tabbed sidebar (Chat · Tarot ·
   I Ching · Astro · Story, same icon bars) every recursive.eco page mounts.
   When the pattern changes in the app, this site follows automatically —
   nothing here to keep in sync. Auth carries too: tarot.recursive.eco is a
   .recursive.eco subdomain, so the signed-in session flows into the iframe.
   This file IS the pattern source for the family: recursive-astrology's own
   assistant.js is modeled on this one (its header comment says so). Keep the
   two in sync by hand when the pattern evolves — there's no shared package. */
(function () {
  // Never render inside an embed: some viewer pages iframe other viewer pages
  // (e.g. pages/course-viewer.html embeds viewers/genealogy-tree.html and
  // viewers/timeline.html with ?embed=1), and a few viewers already carry their
  // own purpose-built assistant iframe (viewers/cards.html, viewers/tree-viewer.html,
  // pages/course-viewer.html) — this guard is what keeps the shared shell from
  // double-mounting on top of those. Same rule site-header.js / site-footer.js apply.
  if (window.self !== window.top) return;
  if (new URLSearchParams(location.search).get('embed') === '1') return;

  var s = document.createElement('script');
  s.src = 'https://recursive.eco/js/assistant-launcher.js';
  s.defer = true;
  s.onload = function () {
    if (!window.RecursiveAssistant) return;
    window.RecursiveAssistant.init({
      buildSrc: function () {
        var params = new URLSearchParams(location.search);
        var grammarId = params.get('grammar_id') || params.get('id') || '';
        var qs = new URLSearchParams();
        if (grammarId) {
          // A grammar is on the page: the assistant grounds "this grammar" on it.
          qs.set('grammar_id', grammarId);
          qs.set('context', 'tarot');
        } else {
          // No grammar: pass page context so "what is this page?" just works.
          qs.set('page_title', document.title || 'The Recursive Tarot');
          qs.set('page_url', location.href);
        }
        return window.RecursiveAssistant.flowBaseUrl() + '/assistant?' + qs.toString();
      }
    });
  };
  document.head.appendChild(s);

  // Jul 9 2026 fix, carried over from recursive-astrology's assistant.js —
  // header-over-assistant overlap. Root cause, confirmed by reading the shared
  // launcher's actual source (recursive-eco/apps/landing/js/assistant-launcher.js):
  // `.rec-assistant-shell` is z-index:45, LOWER than this site's own sticky
  // <site-header> (site-header.js, z-index:50). Both are position:fixed/sticky
  // elements competing directly at the document root, so whichever has the
  // bigger number paints on top — no stacking-context trap involved.
  // site-header.js also auto-hides on scroll-down and *reveals* on scroll-up (a
  // normal reading gesture), which re-plants the header at top:0 while the
  // assistant panel (position:fixed, unaffected by page scroll) is open — at
  // that moment the header's opaque background paints over the assistant's
  // top ~129px, covering the first lines of whatever response is scrolled to
  // the top. recursive-tarot's site-header.js has the identical sticky/
  // z-index:50/auto-hide-reveal pattern (confirmed by reading it), so the same
  // bug applies here too.
  //
  // The correct long-term fix is bumping z-index in the shared launcher itself
  // (it's meant to be the topmost layer on every recursive.eco family site) —
  // that lives in a different, private repo and needs its own session/approval.
  // Until then, force it here so this site is never affected regardless of the
  // shared file's current value or load order.
  var zfix = document.createElement('style');
  zfix.textContent = '.rec-assistant-shell{z-index:2147483000!important}';
  document.head.appendChild(zfix);
})();
