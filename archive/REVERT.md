# Putting an archived page back

The archive (Oct 20 2026) moved four pages and deleted nothing. Each old address holds a short stub
that forwards to the archive with its query and `#hash` kept, so every old link still works.

| Page | Now | Old address (the stub) |
|---|---|---|
| Cards | `archive/cards.html` | `viewers/cards.html` |
| Tree | `archive/tree-viewer.html` | `viewers/tree-viewer.html` |
| Course | retired Oct 23 2026 (deleted; restore from the history before that pull request) | none: courses read in recursive.eco Play |
| One deck | `archive/deck.html` | `deck.html` |

## Undo all of it

Revert the pull request's merge commit (on GitHub: the PR page → **Revert**, or
`git revert -m 1 <merge sha>`). The pages come back to their old addresses, the stubs and this folder go.

## Put one page back (example: Cards)

1. Delete the stub: `git rm viewers/cards.html`
2. Move the page back: `git mv archive/cards.html viewers/cards.html`
3. Undo its path edits (the only lines the move changed):
   - Cards and Tree: the helper scripts go back to bare names,
     `src="../viewers/reference-resolve.js?v=2"` → `src="reference-resolve.js?v=2"` (and the same for
     `grammar-loader.js`, `dimension-engine.js`, `deck-picker.js`).
   - Tree: its "Lay the cards" button, `../viewers/caster-studio.html` → `caster-studio.html`.
   - Course: `../viewers/course-embeds.css` and `../viewers/course-embeds.js` → bare names.
   - One deck: drop the `../` added to `theme.css`, `style.css`, `site-header.js`, `site-footer.js`,
     `assistant.js`, `loader.js`, `index.html`, and set `<site-footer base="">`. (`loader.js` now finds
     the grammar from its own address, so it works from either place; no change needed there.)
4. Point the navigation back: `site-header.js` (Views menu: Cards, Tree; Play menu: Bus Passengers),
   `view-switcher.js` (Cards, Course, Tree, Thumbnails), and `scripts/build_search_index.py`
   (then `python scripts/build_search_index.py`).
5. Take its card off `archive/index.html`.
6. Run `python scripts/check_all.py`, then open the old address with a `?src=` to see it load.
