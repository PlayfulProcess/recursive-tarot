/* recursive-tarot — the ONE recursive.eco assistant sidebar.
   <script src="assistant.js" defer></script>   (../assistant.js from pages/ and viewers/)

   NOT a copy of the assistant: this only loads the shared shell,
   https://recursive.eco/js/assistant-launcher.js, which iframes the flow app's
   /assistant embed — the exact same star FAB and tabbed sidebar (Chat · Tarot ·
   I Ching · Astro · Story, same icon bars) every recursive.eco page mounts.
   When the pattern changes in the app, this site follows automatically —
   nothing here to keep in sync. Auth carries too: tarot.recursive.eco is a
   .recursive.eco subdomain, so the signed-in session flows into the iframe.
   Same file as recursive-astrology/assistant.js (Jul 7 2026). */
(function () {
  // Never render inside an embed: the flow app iframes these viewers (it has its
  // own assistant), and ?embed=1 marks other framed uses.
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
})();
