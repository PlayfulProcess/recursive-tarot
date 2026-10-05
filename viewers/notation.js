/* notation.js — the card-table notation: parse it, write it back, name its cards.
 *
 * A card table is a grid of areas (rows) by columns (default: less · keep · more), with one or
 * more cards in each cell. The notation is how a table is written by hand or typed:
 *
 *   deck: golden-dawn-book-t-tarot
 *   columns: less | keep | more
 *   [Goals]                         <- a row in brackets is a heading over the rows below it
 *   Work    | 4C     | 3W     | (XVIII)
 *   Health  | 7C↓    | 8C 3P  | QS
 *   > cards = possibilities         <- a free note
 *   Golden Dawn: (6C) QS 11         <- a mini-row: a label, a colon, cards (another deck/oracle)
 *
 * Cards:  majors in Roman numerals 0–XXI (0 = the Fool) · minors as rank + suit
 *         ranks A (or 1), 2–10, P page, Kn knight, Q queen, K king
 *         suits W wands, C cups, S swords, P pentacles; also ♥/♡ cups, ⛤/☆ pentacles,
 *               + or † swords (a handwritten sword can read as "+")
 *         ↓ (or r) after a card = reversed; ↑ = upright (optional) · (card) = circled, the message
 *         two cards in one cell: separated by a space · "-" or nothing = an empty cell
 *
 * Pure functions, no DOM: works in the browser (window.CardNotation) and in node (require).
 * Errors never throw; they come back per line: { line, text, message }.
 */
(function (global) {
  'use strict';

  const ROMAN = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
    'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI'];
  const MAJOR_NAMES = ['The Fool', 'The Magician', 'The High Priestess', 'The Empress', 'The Emperor',
    'The Hierophant', 'The Lovers', 'The Chariot', 'Strength', 'The Hermit', 'Wheel of Fortune',
    'Justice', 'The Hanged Man', 'Death', 'Temperance', 'The Devil', 'The Tower', 'The Star',
    'The Moon', 'The Sun', 'Judgement', 'The World'];
  // suit symbol -> canonical letter
  const SUIT_ALIASES = { W: 'W', C: 'C', S: 'S', P: 'P', '♥': 'C', '♡': 'C', '⛤': 'P', '☆': 'P', '+': 'S', '†': 'S' };
  const SUIT_NAMES = { W: 'Wands', C: 'Cups', S: 'Swords', P: 'Pentacles' };
  // rank token -> number (1..14)
  const RANKS = { A: 1, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    P: 11, KN: 12, Q: 13, K: 14 };
  const RANK_CODE = { 1: 'A', 11: 'P', 12: 'Kn', 13: 'Q', 14: 'K' };
  const RANK_NAMES = { 1: 'Ace', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven',
    8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Page', 12: 'Knight', 13: 'Queen', 14: 'King' };
  const DEFAULT_COLUMNS = ['less', 'keep', 'more'];
  const KEYWORDS = new Set(['deck', 'columns', 'title']);

  /** Parse one card token. Returns a card object, or { error }. */
  function parseCard(raw) {
    let t = String(raw || '').trim();
    if (!t) return { error: 'empty card' };
    let circled = false, reversed = false;
    if (t[0] === '(' && t[t.length - 1] === ')') { circled = true; t = t.slice(1, -1).trim(); }
    // orientation suffix: ↓ / r = reversed, ↑ = upright
    if (/[↓]$/.test(t)) { reversed = true; t = t.slice(0, -1); }
    else if (/[↑]$/.test(t)) { t = t.slice(0, -1); }
    else if (t.length > 1 && /r$/.test(t) && !/^\d+r$/i.test(t)) { reversed = true; t = t.slice(0, -1); }
    // the circle may also sit inside the orientation: (XVIII)↓ handled above; "(4C↓)" too
    if (!circled && t[0] === '(' && t[t.length - 1] === ')') { circled = true; t = t.slice(1, -1).trim(); }
    if (!t) return { error: `"${raw}" has no card` };

    const up = t.toUpperCase();
    const mi = ROMAN.indexOf(up);
    if (mi >= 0) {
      return { raw: String(raw).trim(), major: true, number: mi, rank: null, suit: null, reversed, circled };
    }
    const suitChar = t.slice(-1);
    const suit = SUIT_ALIASES[suitChar.toUpperCase()] || SUIT_ALIASES[suitChar];
    const rankTok = t.slice(0, -1).toUpperCase();
    if (!suit || !(rankTok in RANKS)) {
      return { error: `"${raw}" isn't a card (majors: 0–XXI; minors: rank A,2–10,P,Kn,Q,K + suit W,C,S,P)` };
    }
    return { raw: String(raw).trim(), major: false, number: null, rank: RANKS[rankTok], suit, reversed, circled };
  }

  /** The canonical code for a card: XVIII, 4C↓, (KnP). */
  function cardCode(c, opts) {
    if (!c) return '';
    const o = opts || {};
    let s = c.major ? ROMAN[c.number] : (RANK_CODE[c.rank] || String(c.rank)) + c.suit;
    if (c.reversed) s += '↓';
    if (c.circled && !o.noCircle) s = '(' + s + ')';
    return s;
  }

  /** A plain-language name: "XVIII The Moon", "Four of Cups". */
  function cardName(c) {
    if (!c) return '';
    if (c.major) return ROMAN[c.number] + ' ' + MAJOR_NAMES[c.number];
    return RANK_NAMES[c.rank] + ' of ' + SUIT_NAMES[c.suit];
  }

  function splitCards(cellText) {
    const t = String(cellText || '').trim();
    if (!t || t === '-' || t === '—') return [];
    // keep "( 4C )" together: tokens are runs of non-space, but a lone "(" or ")" joins its neighbour
    // a lone arrow ("4C ↑", "7C ↓") belongs to the card before it, as in handwriting
    const toks = t.replace(/\(\s+/g, '(').replace(/\s+\)/g, ')').split(/\s+/);
    const out = [];
    toks.forEach(tok => { if (/^[↑↓]$/.test(tok) && out.length) out[out.length - 1] += tok; else out.push(tok); });
    return out;
  }

  /** Parse a whole table. Returns { title, deck, columns, rows, notes, strips, errors }.
   *  rows: [{ label, heading:false, cells:[[card...]] } | { label, heading:true }] */
  function parseTable(text) {
    const out = { title: '', deck: '', columns: DEFAULT_COLUMNS.slice(), rows: [], notes: [], strips: [], errors: [] };
    const lines = String(text || '').split(/\r?\n/);
    lines.forEach((rawLine, idx) => {
      const n = idx + 1;
      const line = rawLine.trim();
      if (!line || line.startsWith('#') || line.startsWith('//')) return;
      if (line.startsWith('>')) { out.notes.push(line.replace(/^>\s?/, '')); return; }
      const kw = line.match(/^([A-Za-z]+)\s*:\s*(.*)$/);
      const kwKey = kw ? kw[1].toLowerCase() : '';
      if (kw && KEYWORDS.has(kwKey) && (kwKey === 'columns' || line.indexOf('|') < 0)) {
        const key = kw[1].toLowerCase(), val = kw[2].trim();
        if (key === 'deck') out.deck = val;
        else if (key === 'title') out.title = val;
        else if (key === 'columns') {
          const cols = val.split('|').map(s => s.trim()).filter(Boolean);
          if (cols.length) out.columns = cols;
          else out.errors.push({ line: n, text: rawLine, message: 'columns: needs at least one name, separated by |' });
        }
        return;
      }
      const head = line.match(/^\[(.+)\]$/);
      if (head) { out.rows.push({ label: head[1].trim(), heading: true }); return; }
      if (line.indexOf('|') >= 0) {
        const parts = line.split('|').map(s => s.trim());
        const label = parts.shift();
        const cells = parts.map((cellText, ci) => {
          const cards = [];
          splitCards(cellText).forEach(tok => {
            const c = parseCard(tok);
            if (c.error) out.errors.push({ line: n, text: rawLine, message: `column ${ci + 1}: ${c.error}` });
            else cards.push(c);
          });
          return cards;
        });
        out.rows.push({ label, heading: false, cells });
        return;
      }
      const strip = line.match(/^([^:]+):\s*(.*)$/);
      if (strip) {
        const cards = [];
        splitCards(strip[2]).forEach(tok => {
          const c = parseCard(tok);
          if (c.error) out.errors.push({ line: n, text: rawLine, message: c.error });
          else cards.push(c);
        });
        out.strips.push({ label: strip[1].trim(), cards });
        return;
      }
      out.errors.push({ line: n, text: rawLine, message: 'not a row (use "Label | cards | cards | cards"), a [heading], a "> note" or "Label: cards"' });
    });
    // rows narrower than the columns get empty cells; wider rows widen the table (unnamed columns)
    const width = Math.max(out.columns.length, ...out.rows.filter(r => !r.heading).map(r => r.cells.length), 0);
    while (out.columns.length < width) out.columns.push('');
    out.rows.forEach(r => { if (!r.heading) while (r.cells.length < width) r.cells.push([]); });
    return out;
  }

  /** Write a table back to notation (the inverse of parseTable, up to spacing). */
  function serializeTable(t) {
    const lines = [];
    if (t.title) lines.push('title: ' + t.title);
    if (t.deck) lines.push('deck: ' + t.deck);
    lines.push('columns: ' + (t.columns || DEFAULT_COLUMNS).join(' | '));
    lines.push('');
    (t.rows || []).forEach(r => {
      if (r.heading) { lines.push('[' + r.label + ']'); return; }
      const cells = (r.cells || []).map(cards => cards.length ? cards.map(c => cardCode(c)).join(' ') : '-');
      lines.push([r.label || '?'].concat(cells).join(' | '));
    });
    if ((t.notes || []).length || (t.strips || []).length) lines.push('');
    (t.notes || []).forEach(nt => lines.push('> ' + nt));
    (t.strips || []).forEach(s => lines.push(s.label + ': ' + s.cards.map(c => cardCode(c)).join(' ')));
    return lines.join('\n') + '\n';
  }

  const api = { parseCard, parseTable, serializeTable, cardCode, cardName, ROMAN, MAJOR_NAMES, SUIT_NAMES, RANK_NAMES, DEFAULT_COLUMNS };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else global.CardNotation = api;
})(typeof window !== 'undefined' ? window : globalThis);
