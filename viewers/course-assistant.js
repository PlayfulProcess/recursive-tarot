/* Course reading companion — a self-contained, static-only assistant.
 *
 * Lives entirely in the tarot repo: it reads the course straight from the page
 * (no Supabase, no UUID, no webhook) and calls Claude directly from the browser
 * using a key the reader provides (stored only in their browser, never committed).
 * For the author's own read/edit use this is the whole "assistant flow" — no
 * recursive.eco involvement.
 *
 * Usage:  <script src="course-assistant.js?v=1"></script>  on any course page
 * that renders into #ctitle / #cintro / .content (grammar-course.html does).
 */
(function () {
  if (window.__rtCourseAssistant) return;
  window.__rtCourseAssistant = true;

  // --- config ---------------------------------------------------------------
  const API = 'https://api.anthropic.com/v1/messages';
  const LS_KEY = 'rt-claude-key';                 // localStorage key (browser only)
  const MODEL = 'claude-sonnet-4-6';              // cheap-but-good for Q&A.
  //   swap to 'claude-opus-4-8' (best) or 'claude-haiku-4-5' (cheapest).
  const MAX_TOKENS = 1024;
  const CONTEXT_CAP = 500000;                     // chars of course text (~125k tokens) — fits 1M ctx;
  //   the course prefix is prompt-cached, so follow-up questions in a session are ~0.1x the input cost.

  const md = (t) => (window.marked ? window.marked.parse(t) : t.replace(/</g, '&lt;'));
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  // Pull the course straight from the rendered page.
  function courseText() {
    const title = (document.getElementById('ctitle') || {}).textContent || document.title || '';
    const intro = (document.getElementById('cintro') || {}).textContent || '';
    const body = ((document.querySelector('.content') || document.body) || {}).innerText || '';
    let t = `# ${title}\n\n${intro}\n\n${body}`.trim();
    if (t.length > CONTEXT_CAP) t = t.slice(0, CONTEXT_CAP) + '\n\n[…course truncated for length…]';
    return t;
  }

  const SYSTEM_PREFIX =
    'You are a warm, precise reading companion embedded inside a course, part of ' +
    "recursive.eco's Recursive Tarot. Answer the reader's questions using ONLY the " +
    'course text below. If the answer is not in the course, say so plainly and do not ' +
    'invent history, dates, or sources. Be concise; when it helps, point to the relevant ' +
    'section by its heading. This project reads the cards as a mirror, never as a ' +
    'prediction — never tell the reader their fate or treat a card as something to obey.';

  const convo = []; // {role:'user'|'assistant', content:string}

  // --- UI (shadow DOM so the page CSS can't fight it) -----------------------
  const host = document.createElement('div');
  document.body.appendChild(host);
  const sr = host.attachShadow({ mode: 'open' });
  sr.innerHTML = `
    <style>
      :host{ all:initial }
      .fab{ position:fixed; right:18px; bottom:18px; z-index:9998; font-family:Inter,system-ui,sans-serif;
        background:#9a7322; color:#fff; border:none; border-radius:999px; padding:12px 18px; font-size:14px;
        font-weight:600; cursor:pointer; box-shadow:0 10px 28px -10px rgba(60,45,20,.6) }
      .fab:hover{ background:#7c5b18 }
      .panel{ position:fixed; right:18px; bottom:18px; z-index:9999; width:min(420px,calc(100vw - 24px));
        height:min(560px,calc(100vh - 24px)); background:#fbf9f3; border:1px solid #d8d2c6; border-radius:14px;
        display:none; flex-direction:column; overflow:hidden; box-shadow:0 24px 60px -20px rgba(60,45,20,.55);
        font-family:Inter,system-ui,sans-serif; color:#221f1a }
      .panel.open{ display:flex }
      .hd{ display:flex; align-items:center; gap:8px; padding:11px 13px; border-bottom:1px solid #e7e1d5; background:#fff }
      .hd b{ font-size:13.5px } .hd .sp{ flex:1 }
      .hd button{ background:none; border:none; cursor:pointer; color:#6b6457; font-size:13px; padding:4px 6px; border-radius:6px }
      .hd button:hover{ background:#f1ece1; color:#221f1a }
      .log{ flex:1; overflow:auto; padding:13px; display:flex; flex-direction:column; gap:11px }
      .msg{ font-size:13.5px; line-height:1.55; max-width:90% }
      .msg.u{ align-self:flex-end; background:#9a7322; color:#fff; padding:8px 11px; border-radius:12px 12px 3px 12px }
      .msg.a{ align-self:flex-start; color:#221f1a }
      .msg.a :first-child{ margin-top:0 } .msg.a :last-child{ margin-bottom:0 }
      .msg.a p{ margin:.4em 0 } .msg.a a{ color:#8a6414 }
      .msg.sys{ align-self:center; color:#6b6457; font-size:12px; text-align:center; max-width:100% }
      .msg.err{ align-self:flex-start; color:#a3402d; font-size:12.5px }
      .ft{ border-top:1px solid #e7e1d5; padding:10px; background:#fff }
      .ft form{ display:flex; gap:7px }
      .ft input,.ft textarea{ font-family:inherit; font-size:13.5px }
      .ft textarea{ flex:1; resize:none; height:38px; padding:8px 10px; border:1px solid #d8d2c6; border-radius:8px; background:#fbf9f3 }
      .ft .send{ background:#9a7322; color:#fff; border:none; border-radius:8px; padding:0 14px; font-weight:600; cursor:pointer }
      .ft .send:disabled{ background:#d8d2c6; cursor:default }
      .keyrow{ display:flex; gap:7px; margin-bottom:8px }
      .keyrow input{ flex:1; padding:8px 10px; border:1px solid #d8d2c6; border-radius:8px; background:#fbf9f3 }
      .keynote{ font-size:11px; color:#6b6457; margin:0 0 8px; line-height:1.45 }
      .keynote a{ color:#8a6414 }
    </style>
    <button class="fab" id="fab">✦ Ask about this course</button>
    <section class="panel" id="panel" aria-label="Course assistant">
      <div class="hd"><b>Reading companion</b><span class="sp"></span>
        <button id="reset" title="Clear conversation">Clear</button>
        <button id="close" title="Close">✕</button></div>
      <div class="log" id="log"></div>
      <div class="ft" id="ft"></div>
    </section>`;

  const $ = (id) => sr.getElementById(id);
  const panel = $('panel'), log = $('log'), ft = $('ft');

  function add(role, html) {
    const d = document.createElement('div');
    d.className = 'msg ' + role;
    d.innerHTML = html;
    log.appendChild(d);
    log.scrollTop = log.scrollHeight;
    return d;
  }

  function renderFooter() {
    const hasKey = !!localStorage.getItem(LS_KEY);
    if (!hasKey) {
      ft.innerHTML =
        `<p class="keynote">Paste an <b>Anthropic API key</b> to chat. It is stored only in this browser
         (localStorage), sent directly to Anthropic, and never committed. Use a key with a low budget.
         <a href="https://console.anthropic.com/settings/keys" target="_blank" rel="noopener">Get a key →</a></p>
         <div class="keyrow"><input id="key" type="password" placeholder="sk-ant-…" autocomplete="off">
         <button class="send" id="savekey">Save</button></div>`;
      $('savekey').onclick = () => {
        const v = $('key').value.trim();
        if (v) { localStorage.setItem(LS_KEY, v); renderFooter(); $('q') && $('q').focus(); }
      };
      $('key').addEventListener('keydown', e => { if (e.key === 'Enter') $('savekey').click(); });
      return;
    }
    ft.innerHTML =
      `<form id="form"><textarea id="q" placeholder="Ask anything about the course…" rows="1"></textarea>
       <button class="send" id="send" type="submit">Send</button></form>`;
    const form = $('form'), q = $('q');
    form.onsubmit = (e) => { e.preventDefault(); send(q.value); };
    q.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(q.value); } });
    q.focus();
  }

  async function send(text) {
    text = (text || '').trim();
    if (!text) return;
    const key = localStorage.getItem(LS_KEY);
    if (!key) return renderFooter();
    $('q') && ($('q').value = '');
    $('send') && ($('send').disabled = true);
    add('u', esc(text));
    convo.push({ role: 'user', content: text });
    const thinking = add('a', '<em style="color:#6b6457">thinking…</em>');
    try {
      const res = await fetch(API, {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'x-api-key': key,
          'anthropic-version': '2023-06-01',
          'anthropic-dangerous-direct-browser-access': 'true'
        },
        body: JSON.stringify({
          model: MODEL,
          max_tokens: MAX_TOKENS,
          // System as a cacheable block: the (large, stable) course text is prompt-cached,
          // so each follow-up question in a ~5-min window pays ~0.1x for it.
          system: [{
            type: 'text',
            text: SYSTEM_PREFIX + '\n\n=== COURSE TEXT ===\n' + courseText(),
            cache_control: { type: 'ephemeral' }
          }],
          messages: convo
        })
      });
      const data = await res.json();
      if (data.error) {
        thinking.className = 'msg err';
        thinking.textContent = data.error.message || 'Request failed.';
        if (res.status === 401) { localStorage.removeItem(LS_KEY); renderFooter(); }
        convo.pop();
      } else {
        const out = (data.content || []).filter(b => b.type === 'text').map(b => b.text).join('').trim();
        thinking.className = 'msg a';
        thinking.innerHTML = md(out || '(no answer)');
        convo.push({ role: 'assistant', content: out });
      }
    } catch (err) {
      thinking.className = 'msg err';
      thinking.textContent = 'Network error: ' + (err && err.message || err);
      convo.pop();
    } finally {
      $('send') && ($('send').disabled = false);
      log.scrollTop = log.scrollHeight;
    }
  }

  $('fab').onclick = () => {
    panel.classList.add('open');
    $('fab').style.display = 'none';
    if (!log.children.length) {
      add('sys', 'Ask about anything in this course — I read only from the page in front of you.');
    }
    renderFooter();
  };
  $('close').onclick = () => { panel.classList.remove('open'); $('fab').style.display = ''; };
  $('reset').onclick = () => { convo.length = 0; log.innerHTML = ''; add('sys', 'Conversation cleared.'); };
})();
