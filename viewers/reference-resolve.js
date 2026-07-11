/**
 * Shared repo-local reference resolver.
 *
 * The meta grammar (`tarot/all-decks-many-lenses/grammar.json`, "The Tarot — All Decks, Many
 * Lenses") wires every card item with `metadata.source_deck` (the source deck's repo slug) +
 * `metadata.source_item_id` (the card's id within that deck's own grammar.json) — see
 * `scripts/build_meta_grammar.py` and the cross-link pattern documented in CLAUDE.md. That's
 * the repo-native counterpart of the Supabase-imported copy's `ref_document_id`/`ref_item_id`
 * pointer (wired at import time by the private app's `scripts/import-historical-tarot.mjs`).
 *
 * This module resolves that pointer to the SOURCE card's own content (keywords + sections) by
 * fetching the source deck's grammar.json directly from the repo — no backend, no Supabase call
 * needed, since the source decks live right here in `tarot/<slug>/grammar.json`. Mirrors the
 * semantics of the private app's `apps/flow/src/lib/grammar/reference-resolve.ts` (the
 * `get_grammar_item_text` RPC + source-doc name lookup): resolve whenever the pointer is
 * present, cache per (deck, item), never treat "item already has its own content" as a reason
 * to skip resolution — the meta card's own "Origin" blurb and the resolved source content are
 * additive, not a replace-vs-keep choice.
 *
 * Used by viewers/cards.html (card detail modal), viewers/caster-studio.html (drawn-card detail
 * in a cast/reading), and viewers/tree-viewer.html (tree node detail).
 */
(function (global) {
  // slug -> Promise<grammarJson|null>, shared across every resolveSourceItem call on the page.
  const deckGrammarCache = {};

  function loadDeckGrammar(slug) {
    if (!deckGrammarCache[slug]) {
      deckGrammarCache[slug] = fetch('../tarot/' + encodeURIComponent(slug) + '/grammar.json')
        .then(function (r) { return r.ok ? r.json() : null; })
        .catch(function () { return null; });
    }
    return deckGrammarCache[slug];
  }

  /**
   * @param {string} srcDeck - source deck slug (metadata.source_deck)
   * @param {string} srcItemId - source item id within that deck (metadata.source_item_id)
   * @param {string} [deckLabelHint] - display name to prefer (e.g. metadata.deck), falls back
   *   to the source grammar's own `name`, then the slug — NEVER shows a bare id/uuid.
   * @returns {Promise<{status:'ok', item:object, deckLabel:string}|{status:'error', deckLabel:string|null}>}
   */
  async function resolveSourceItem(srcDeck, srcItemId, deckLabelHint) {
    if (!srcDeck || !srcItemId) {
      return { status: 'error', deckLabel: deckLabelHint || null };
    }
    const g = await loadDeckGrammar(srcDeck);
    const deckLabel = deckLabelHint || (g && g.name) || srcDeck;
    if (!g) return { status: 'error', deckLabel: deckLabelHint || null };
    const item = (g.items || []).find(function (it) { return it.id === srcItemId; });
    if (!item) return { status: 'error', deckLabel };
    return { status: 'ok', item: item, deckLabel: deckLabel };
  }

  global.RefResolve = { resolveSourceItem: resolveSourceItem, loadDeckGrammar: loadDeckGrammar };
})(window);
