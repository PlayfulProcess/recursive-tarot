/* The Recursive Tarot — tiny static loader.
   Loads grammar JSON from a local repo path (?file=), or from a GitHub branch
   (?path=tarot/<slug>&ref=<branch>). No dependencies. */
(function (g) {
  'use strict';

  var OWNER = 'PlayfulProcess', REPO = 'recursive-tarot';

  function qs(name) {
    return new URLSearchParams(location.search).get(name);
  }

  // Resolve where to fetch a grammar from, based on URL params.
  function grammarUrl() {
    var file = qs('file');                 // e.g. tarot/visconti-sforza-tarot/grammar.json
    if (file) return rel(file);
    var path = qs('path'), ref = qs('ref'); // e.g. path=tarot/<slug> ref=my-branch
    if (path) {
      if (!/grammar\.json$/.test(path)) path = path.replace(/\/$/, '') + '/grammar.json';
      return 'https://raw.githubusercontent.com/' + OWNER + '/' + REPO + '/' +
             (ref || 'main') + '/' + path;
    }
    return null;
  }

  // The viewer pages live at the repo root, alongside the tarot/ data folder,
  // so a repo-relative path is used as-is.
  function rel(p) {
    return p;
  }

  function collectionUrl() {
    var ref = qs('ref');
    if (ref) return 'https://raw.githubusercontent.com/' + OWNER + '/' + REPO + '/' + ref + '/tarot/_collection.json';
    return rel('tarot/_collection.json');
  }

  async function fetchJson(url) {
    var r = await fetch(url, { cache: 'no-cache' });
    if (!r.ok) throw new Error('Could not load ' + url + ' (' + r.status + ')');
    return r.json();
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // Turn bare http(s) URLs into anchors. Runs FIRST, on already-escaped plain text, and only
  // matches a URL at the start of the string or after whitespace — so a markdown link's target
  // (preceded by "(") is left alone for the [text](url) rule below, and nothing inside an
  // attribute or an already-built anchor can be matched twice. Trailing sentence punctuation
  // and a closing bracket are pushed back out of the href.
  var URL_RE = /(^|\s)(https?:\/\/[^\s<>"']+)/g;
  function linkify(escaped) {
    return String(escaped).replace(URL_RE, function (m, pre, url) {
      var tail = '';
      var t = url.match(/[).,;:!?]+$/);
      if (t) { tail = t[0]; url = url.slice(0, -tail.length); }
      return pre + '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + url + '</a>' + tail;
    });
  }

  // Render markdown-ish: **bold**, *italic*, `code`, [text](url) links, bare URLs, and #/##
  // headings. Inline images are dropped (they're shown separately). Links are real anchors —
  // section prose across the grammars carries markdown links (research dossiers, Wikipedia,
  // full-text sources) and used to render as literal "[label](https://…)" text here.
  function md(s) {
    s = esc(s);
    s = linkify(s);
    s = s.replace(/!\[[^\]]*\]\(([^)]+)\)/g, '');           // drop inline images (shown separately)
    // [text](url) — the target may already have been wrapped by linkify(); unwrap it first.
    s = s.replace(/\[([^\]]+)\]\(\s*(?:<a href="([^"]+)"[^>]*>[^<]*<\/a>|([^)\s]+))\s*\)/g,
      function (m, text, wrapped, plain) {
        var href = wrapped || plain || '';
        var ext = /^https?:\/\//i.test(href);
        return '<a href="' + href + '"' + (ext ? ' target="_blank" rel="noopener noreferrer"' : '') + '>' + text + '</a>';
      });
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
    s = s.replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
    s = s.replace(/\*([^*]+)\*/g, '<i>$1</i>');
    // Headings: markdown "#"/"##" lines used to render as literal hashes in long descriptions.
    s = s.replace(/(^|\n)#{1,6}\s+([^\n]+)/g, '$1<b class="mdh">$2</b>');
    s = s.replace(/\n/g, '<br>');
    return s;
  }

  function deckHref(slug) {
    var ref = qs('ref');
    return 'deck.html?file=tarot/' + slug + '/grammar.json' + (ref ? '&ref=' + encodeURIComponent(ref) : '');
  }

  g.RT = { qs: qs, grammarUrl: grammarUrl, collectionUrl: collectionUrl, fetchJson: fetchJson,
           esc: esc, md: md, linkify: linkify, deckHref: deckHref, rel: rel };
})(window);
