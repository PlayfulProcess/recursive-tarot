// Tests for notation.js. Run: node viewers/notation.test.js
'use strict';
const assert = require('assert');
const N = require('./notation.js');

let passed = 0;
function t(name, fn) { fn(); passed++; }

t('majors in Roman numerals, 0 is the Fool', () => {
  const c = N.parseCard('XVIII');
  assert.deepStrictEqual([c.major, c.number, c.reversed, c.circled], [true, 18, false, false]);
  assert.strictEqual(N.parseCard('0').number, 0);
  assert.strictEqual(N.cardName(N.parseCard('XXI')), 'XXI The World');
});

t('minors: ranks and suits', () => {
  const c = N.parseCard('4C');
  assert.deepStrictEqual([c.major, c.rank, c.suit], [false, 4, 'C']);
  assert.strictEqual(N.parseCard('AW').rank, 1);
  assert.strictEqual(N.parseCard('1W').rank, 1);
  assert.strictEqual(N.parseCard('10S').rank, 10);
  assert.strictEqual(N.parseCard('PW').rank, 11);
  assert.strictEqual(N.parseCard('KnP').rank, 12);
  assert.strictEqual(N.parseCard('QS').rank, 13);
  assert.strictEqual(N.parseCard('KC').rank, 14);
  assert.strictEqual(N.parseCard('PP').suit, 'P');      // page of pentacles
  assert.strictEqual(N.cardName(N.parseCard('KnP')), 'Knight of Pentacles');
});

t('reversed with ↓ (her mark) or r; ↑ is optional upright', () => {
  assert.strictEqual(N.parseCard('7C↓').reversed, true);
  assert.strictEqual(N.parseCard('6Wr').reversed, true);
  assert.strictEqual(N.parseCard('XIIr').reversed, true);
  const up = N.parseCard('4C↑');
  assert.deepStrictEqual([up.reversed, up.rank, up.suit], [false, 4, 'C']);
});

t('circled = parentheses, with or without orientation', () => {
  assert.strictEqual(N.parseCard('(XVIII)').circled, true);
  const a = N.parseCard('(4C↓)'); assert.deepStrictEqual([a.circled, a.reversed], [true, true]);
  const b = N.parseCard('(4C)↓'); assert.deepStrictEqual([b.circled, b.reversed], [true, true]);
});

t('her glyphs: ♥ cups, ⛤ pentacles, + or † swords', () => {
  assert.strictEqual(N.parseCard('3♥').suit, 'C');
  assert.strictEqual(N.parseCard('QP').suit, 'P');
  assert.strictEqual(N.parseCard('Q⛤').suit, 'P');
  assert.strictEqual(N.parseCard('8+').suit, 'S');
  assert.strictEqual(N.parseCard('8†').suit, 'S');
});

t('bad cards come back as errors, never throw', () => {
  for (const bad of ['9X', 'XXII', '11C', 'Z', '()', '', 'KnZ']) {
    assert.ok(N.parseCard(bad).error, `expected an error for "${bad}"`);
  }
});

t('codes round-trip', () => {
  for (const s of ['XVIII', '0', '4C', '(XVIII)', '7C↓', '(KnP↓)', 'AW', '10S', 'QP']) {
    assert.strictEqual(N.cardCode(N.parseCard(s)), s);
  }
  assert.strictEqual(N.cardCode(N.parseCard('6Wr')), '6W↓');   // r is written back as ↓
  assert.strictEqual(N.cardCode(N.parseCard('8+')), '8S');      // glyphs become letters
});

const EXAMPLE = `deck: golden-dawn-book-t-tarot
columns: less | keep | more

[Goals]
Work      | 4C ↑      | 3W        | (XVIII)
Health    | 7C        | 8C 3P     | QS
Writing   | (XVII)    | AS        | 6W↓
Family    | KnP       | (VIII)    | IV

> cards = possibilities
Golden Dawn: (6C) QS XI
`;

t('the plan example parses: rows, heading, notes, strip', () => {
  const tb = N.parseTable(EXAMPLE);
  assert.strictEqual(tb.deck, 'golden-dawn-book-t-tarot');
  assert.deepStrictEqual(tb.columns, ['less', 'keep', 'more']);
  assert.strictEqual(tb.rows.length, 5);
  assert.deepStrictEqual(tb.rows[0], { label: 'Goals', heading: true });
  const health = tb.rows[2];
  assert.strictEqual(health.label, 'Health');
  assert.strictEqual(health.cells[1].length, 2);           // two cards in one cell
  assert.strictEqual(tb.rows[3].cells[2][0].reversed, true);
  assert.deepStrictEqual(tb.notes, ['cards = possibilities']);
  assert.strictEqual(tb.strips[0].label, 'Golden Dawn');
  assert.strictEqual(tb.strips[0].cards.length, 3);
  // "4C ↑": a lone arrow joins the card before it
  assert.strictEqual(tb.rows[1].cells[0].length, 1);
  assert.strictEqual(tb.rows[1].cells[0][0].rank, 4);
  assert.strictEqual(N.parseTable('Work | 7C ↓').rows[0].cells[0][0].reversed, true);
  assert.deepStrictEqual(tb.errors, []);
});

t('errors carry the line number', () => {
  const tb = N.parseTable('Work | 9X | 3W | -\nwhat is this');
  assert.strictEqual(tb.errors.length, 2);
  assert.strictEqual(tb.errors[0].line, 1);
  assert.strictEqual(tb.errors[1].line, 2);
  assert.strictEqual(tb.rows[0].cells[0].length, 0);       // the bad card is skipped
  assert.strictEqual(tb.rows[0].cells[2].length, 0);       // "-" is an empty cell
});

t('serialize then parse gives the same table', () => {
  const a = N.parseTable(EXAMPLE);
  const b = N.parseTable(N.serializeTable(a));
  const strip = x => JSON.parse(JSON.stringify(x, (k, v) => (k === 'raw' || k === 'errors') ? undefined : v));
  assert.deepStrictEqual(strip(b), strip(a));
});

t('short rows are padded; columns default to less | keep | more', () => {
  const tb = N.parseTable('Work | 4C');
  assert.deepStrictEqual(tb.columns, ['less', 'keep', 'more']);
  assert.strictEqual(tb.rows[0].cells.length, 3);
});

console.log(`notation: ${passed} tests passed`);
