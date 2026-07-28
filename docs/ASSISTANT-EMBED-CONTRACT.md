# Assistant embed contract — "Interpret with AI"

**Status (Jul 28 2026): the host side (this repo) is shipped. The flow side (the `/assistant`
embed in `recursive-eco`) does NOT implement this yet — it's queued for the flow-side agent.**
This doc is the pinned contract that implementation must match exactly, so the handshake works
the moment both sides ship it.

## Why this exists

The Spread Caster (`viewers/caster-studio.html`) used to send a finished reading to recursive.eco
by **redirecting** the browser to `flow.recursive.eco/?d=<base64 reading>` (the "Send to
recursive.eco oracle" link). The builder reported this "is not really working." The replacement
keeps the person on the Caster page: it opens the **embedded** assistant sidebar (the same
`.rec-assistant-shell` iframe every recursive-tarot page mounts via `assistant.js` →
`https://recursive.eco/js/assistant-launcher.js` → `flow.recursive.eco/assistant`) and hands the
reading to it with `postMessage`, instead of a full-page navigation.

## Who initiates

The **host page** (any recursive-tarot page that has cast a reading — today, only
`viewers/caster-studio.html`) initiates. The **embed** (`flow.recursive.eco/assistant` or
`dev.flow.recursive.eco/assistant`, running inside the `.rec-assistant-shell iframe`) receives and
acknowledges.

## Step 1 — host opens the sidebar

```js
window.RecursiveAssistant.open();   // exposed by assistant-launcher.js; grows the shell to the pinned sidebar
```

`RecursiveAssistant` is only defined after `assistant-launcher.js` has loaded and called
`init()` — the host must poll for `document.querySelector('.rec-assistant-shell iframe')` before
calling `open()` or posting a message (see `ensureAssistantReady()` in caster-studio.html; ~10s
timeout, then falls back — see Step 4).

## Step 2 — host posts the reading

```js
const iframe = document.querySelector('.rec-assistant-shell iframe');
const targetOrigin = new URL(iframe.src).origin;   // e.g. https://flow.recursive.eco or https://dev.flow.recursive.eco — READ from the live iframe, never hardcoded, never '*'

iframe.contentWindow.postMessage({
  type: 'recursive:interpret-reading',
  reading: { /* ReadingV1 — see schema below */ },
}, targetOrigin);
```

**Origin rule:** the host must derive `targetOrigin` from the iframe's actual `src` at call time
(`new URL(iframe.src).origin`), never hardcode `flow.recursive.eco` or use `'*'`. The iframe's
origin already varies by environment (`assistant-launcher.js`'s `flowBaseUrl()`: `dev.flow.recursive.eco`
when the **host page** is on a `dev.`/`localhost` hostname, `flow.recursive.eco` otherwise) — deriving
from `iframe.src` handles both automatically and never leaks the reading to an unintended origin.

## Step 3 — embed acknowledges

The embed, on receiving a `recursive:interpret-reading` message it accepts, must reply
**immediately** (well under the host's ~1s wait — see Step 4) with:

```js
event.source.postMessage({ type: 'recursive:interpret-ack' }, event.origin);
```

`event.source` is the host window (the iframe's parent); `event.origin` is the host page's own
origin (e.g. `https://tarot.recursive.eco`), which is exactly the right `targetOrigin` for the
reply — it's the origin the incoming message actually arrived from, not a hardcoded value.

The embed should validate the incoming message before acting on it:
- `event.data.type === 'recursive:interpret-reading'`
- `event.data.reading` is an object matching the schema below (tolerate unknown extra fields;
  reject/ignore if `reading.positions` isn't an array)
- `event.origin` is an allowed host — recursive-tarot embeds this same shell pattern is shared
  across the `*.recursive.eco` family (see `assistant-launcher.js` header comment: "recursive-astrology's
  own assistant.js is modeled on this one"), so allow-list known family sites
  (`tarot.recursive.eco`, `astro.recursive.eco`, their `dev.` counterparts, and `localhost` during
  development) rather than a single fixed origin.

After acking, the embed should ground the assistant on the reading — e.g. pre-fill/send a chat
message summarizing the spread and cards and prompting for an interpretation, using the same
system-prompt-context mechanism the embed already uses for `page_title`/`page_url`/`grammar_id`
(see `apps/landing/js/assistant-launcher.js`'s `page-context` handshake in `recursive-eco` for the
existing precedent — this is the same shape of "host hands the embed something to ground on").

## Step 4 — host's ack timeout + fallback

The host waits **~1000ms** for the `recursive:interpret-ack` reply. If it doesn't arrive in time
(embed not yet updated, message rejected, network hiccup):

1. The sidebar is left open regardless (it was already opened in Step 1) — the person can see and
   use the assistant even if the handoff didn't land.
2. The host copies a compact one-line summary of the reading to the clipboard
   (`navigator.clipboard.writeText`), so the person can paste it into the chat themselves.
3. The host shows a small toast:
   - *"Reading copied — paste it into the chat and ask about it. It will send automatically once
     recursive.eco updates."* (clipboard write succeeded), or
   - *"Open the chat and ask about this reading — it will be sent automatically once the app
     updates."* (clipboard denied/unavailable).

See `showInterpretFallbackToast()` / `interpretWithAI()` in `viewers/caster-studio.html` for the
reference implementation.

## Message shapes

**Host → embed:**

```json
{
  "type": "recursive:interpret-reading",
  "reading": { "...": "ReadingV1, see below" }
}
```

**Embed → host (ack):**

```json
{ "type": "recursive:interpret-ack" }
```

No payload on the ack — it only signals "message received and understood," so the host can stop
its fallback timer. If the embed later wants to report ingestion failure, add a new
`ok: false, reason: string` field to this same message rather than inventing a new type — keep the
minimum viable ack contract until there's a real need for more.

## Reading schema — `ReadingV1`

```ts
interface ReadingV1 {
  v: 1;
  spread: string;                 // the working spread's display name (resolveSpreadName()) — the
                                   // one authoritative name, same string shown in #spreadName
  question: string | null;        // the caster's free-text question, or null
  positions: Array<{
    n: number;                    // 1-based position index (board order)
    label: string;                // position label, e.g. "The Root", "Structures · Perceiver"
    meaning: string | null;       // the position's prompt/meaning text, or null
    card: {
      name: string;               // card name, e.g. "The Fool", "Three of Cups"
      deck: string | null;        // deck label, e.g. "Rider-Waite-Smith", "Visconti-Sforza"
      reversed: boolean;          // true if drawn reversed
      arcana: string | null;      // "major" | "minor" | null (unclassified)
      number: number | null;      // rank/trump number when known, else null
    } | null;                     // null when this position hasn't been cast yet
  }>;
  cast_at: string;                 // ISO 8601 timestamp of the cast (Date.toISOString())
  source: string;                  // "https://tarot.recursive.eco/viewers/caster-studio.html"
}
```

Notes for the flow-side implementer:
- `positions[].card` can be `null` — the host currently guards against opening the assistant with
  no cards cast at all (`interpretWithAI()` no-ops with an alert if nothing has been cast), but an
  individual position can still be empty in a partially-cast spread. Handle gracefully.
- This is a **new, independent** message type — it does not reuse or replace the existing
  `eco-spread` message (embed → host, AI-built spread layouts loading into the Caster board) or the
  `?d=<base64>` deep-link format the old redirect link used. Those keep working as-is.
- Field names and casing are pinned. If the schema needs to evolve, bump to `v: 2` and keep `v: 1`
  readable for one deprecation window — same spirit as the Caster's own spread contract
  (`viewers/caster-studio.html`'s `b64urlEncode`/`currentSpreadContract` comments).

## Reference implementation (host side, shipped)

`viewers/caster-studio.html`:
- `getAssistantIframe()`, `ensureAssistantReady()` — locate/wait for the mounted iframe
- `buildReadingForAssistant()` — builds `ReadingV1` from the live `positions` array + `lastCast`
- `buildCompactReadingSummary()` — the one-line fallback-clipboard text
- `interpretWithAI()` — the full flow: open → derive origin → post → wait for ack → fallback
- Wired to the "✦ Interpret with AI" button (`#interpretAI`) in the `.export` panel, which is only
  visible once a cast exists.
