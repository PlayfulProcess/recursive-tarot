/* Shared-identity widget for the Recursive Tarot static site (rung L1 of the
 * tree↔fruit integration ladder, plan/FRUITS-INTEGRATION.md).
 *
 * Reads the SAME Supabase session the recursive.eco app sets: the auth cookie is
 * scoped to `.recursive.eco` (NEXT_PUBLIC_AUTH_COOKIE_DOMAIN), so any subdomain
 * — tarot.recursive.eco included — can see it. This file only ever READS the
 * session; sign-in/out lives on the tree (recursive.eco). Uses the public anon
 * key (browser-safe by design — it ships in every recursive.eco page); RLS and
 * the credits wallet do the real gating server-side.
 *
 * Renders <recursive-auth> (Shadow DOM):  signed-out → "Sign in ↗" linking to
 * recursive.eco · signed-in → green dot + display name linking to /account.
 * Exposes window.recursiveAuth = { client, getUser() } for other fruit features
 * (course tutor, caster readings) to reuse the session + call recursive.eco AI
 * routes with credentials.
 *
 * Off-domain (localhost, GitHub Pages mirrors): the cookie simply isn't there,
 * the widget shows signed-out — the fruit works fully without it.
 */
(function () {
  if (customElements.get('recursive-auth')) return;

  const SUPABASE_URL = 'https://xtviwcznhbrsvkitepvm.supabase.co';
  const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh0dml3Y3puaGJyc3ZraXRlcHZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc1NDA1MDMsImV4cCI6MjA4MzExNjUwM30.eBXM6NTe3Sz3SfdtI0pTHQyJzd6PXJl5ZvpNg7yFSII';
  const TREE = 'https://recursive.eco';
  const FLOW = 'https://flow.recursive.eco';
  // Sign-in deep link: opens the tree's auth modal in a NEW TAB (so work on the
  // fruit is never lost) and tells it where the visitor came from, so after
  // sign-in the tree can offer "return to the tarot site".
  const signInUrl = () => FLOW + '/?signin=1&next=' + encodeURIComponent(location.href);

  const clientPromise = import('https://esm.sh/@supabase/ssr@0.5.2')
    .then(({ createBrowserClient }) => createBrowserClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
      auth: { persistSession: true, autoRefreshToken: false, detectSessionInUrl: false,
              storageKey: 'recursive-eco-auth' },
      cookieOptions: { domain: '.recursive.eco', path: '/', sameSite: 'lax', secure: true },
    }))
    .catch(() => null);

  window.recursiveAuth = {
    client: clientPromise,
    async getUser() {
      const c = await clientPromise; if (!c) return null;
      try { return (await c.auth.getUser()).data.user; } catch { return null; }
    },
  };

  class RecursiveAuth extends HTMLElement {
    async connectedCallback() {
      const root = this.attachShadow({ mode: 'open' });
      root.innerHTML = `
        <style>
          a{ display:inline-flex; align-items:center; gap:6px; text-decoration:none;
             font-size:12.5px; padding:5px 11px; border-radius:999px; white-space:nowrap;
             font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
             color:#a99fc6; border:1px solid #3a3450; transition:.15s }
          a:hover{ color:#ece8f5; border-color:#d4af37 }
          .dot{ width:7px; height:7px; border-radius:50%; background:#81b29a }
          .in{ color:#9ad0b5; border-color:rgba(129,178,154,.45) }
          .in:hover{ color:#bfe8d2 }
        </style>
        <a href="${signInUrl()}" target="_blank" rel="noopener" title="Sign in at recursive.eco — the session carries over to this site">Sign in ↗</a>`;
      const user = await window.recursiveAuth.getUser();
      if (user) {
        const name = (user.user_metadata && (user.user_metadata.username || user.user_metadata.full_name))
                     || (user.email || '').split('@')[0] || 'account';
        const a = root.querySelector('a');
        a.className = 'in';
        a.href = FLOW + '/account';
        a.title = 'Signed in as ' + (user.email || name) + ' — manage at recursive.eco';
        a.innerHTML = '<span class="dot"></span>' + name.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
      }
    }
  }
  customElements.define('recursive-auth', RecursiveAuth);
})();
