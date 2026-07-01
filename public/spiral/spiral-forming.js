// spiral-forming.js — the "still forming" logo for the About page.
//
// A TREE OF SPIRALS from one fixed origin (the centre). Golden logarithmic arms
// (growth ln(φ)/(π·½), as in spiral.js) grow out from the same point, branching into
// a tree as they go — a crowd of small lilac marks with gold accents (echoes
// spiral-v2.svg). It reveals from the origin outward (spreading), holds, then
// withdraws back toward the origin (returning), and re-emerges — always from the
// same centre, never jumping elsewhere. Honours prefers-reduced-motion.
(function () {
  const canvas = document.getElementById('logoCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  let W, H, DPR;
  function resize() {
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    const b = canvas.getBoundingClientRect();
    W = b.width || 220; H = b.height || 220;
    canvas.width = Math.round(W * DPR); canvas.height = Math.round(H * DPR);
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  }
  resize();

  const PHI = (1 + Math.sqrt(5)) / 2;
  const GROWTH = Math.log(PHI) / (Math.PI / 2);
  const rand = (a, b) => a + Math.random() * (b - a);
  const LILAC = ['#c9a8f0', '#c6a3ef', '#bd97ea', '#b085e0', '#a97fdc'];
  const GOLD = ['#b8902f', '#9a7322'];
  const hue = () => (Math.random() < 0.2 ? GOLD : LILAC)[(Math.random() * (Math.random() < 0.2 ? 2 : 5)) | 0];

  let segs = [];
  function build() {
    segs = [];
    const cx = W / 2, cy = H / 2, maxR = Math.min(W, H) * 0.43, dth = 0.09;
    function grow(x, y, th, r, dir, g, depth, col) {
      const c0x = x - r * Math.cos(th), c0y = y - r * Math.sin(th);   // this arm's spiral centre
      let px = x, py = y, rr = r, t = th;
      const steps = Math.round(rand(1.2, 2.6) * 2 * Math.PI / dth);
      for (let i = 0; i < steps; i++) {
        t += dth * dir; rr *= Math.exp(g * dth);
        const nx = c0x + rr * Math.cos(t), ny = c0y + rr * Math.sin(t);
        if (rr > maxR) break;
        const dx = nx - cx, dy = ny - cy;
        segs.push({ x1: px, y1: py, x2: nx, y2: ny, hue: col, dist: Math.sqrt(dx * dx + dy * dy), a: rand(0.5, 0.9) });
        px = nx; py = ny;
        if (depth < 3 && i > steps * 0.25 && Math.random() < 0.02) {          // branch → a tree
          const n = Math.random() < 0.4 ? 2 : 1;
          for (let k = 0; k < n; k++)
            grow(nx, ny, t + rand(-1, 1) * 0.9, Math.max(2, rr * 0.15),
              Math.random() < 0.5 ? dir : -dir, GROWTH * rand(0.55, 1.0), depth + 1,
              Math.random() < 0.7 ? col : hue());
        }
      }
    }
    const arms = 2 + ((Math.random() * 2) | 0);                                 // 2–3 primary arms, one origin
    const base = rand(0, Math.PI * 2);
    for (let a = 0; a < arms; a++)
      grow(cx, cy, base + a * (2 * Math.PI / arms) + rand(-0.3, 0.3), rand(1.5, 3),
        Math.random() < 0.5 ? 1 : -1, GROWTH * rand(0.6, 1.0), 0, hue());
    segs.sort((p, q) => p.dist - q.dist);                                       // reveal from origin outward
  }

  function draw(progress) {
    ctx.clearRect(0, 0, W, H);
    ctx.lineCap = 'round';
    const n = Math.floor(progress * segs.length);
    for (let i = 0; i < n; i++) {
      const s = segs[i];
      ctx.strokeStyle = s.hue; ctx.globalAlpha = s.a;
      ctx.lineWidth = 1.0 + s.dist * 0.012;
      ctx.beginPath(); ctx.moveTo(s.x1, s.y1); ctx.lineTo(s.x2, s.y2); ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  window.addEventListener('resize', () => { resize(); build(); });

  const ease = t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  const T_GROW = 4200, T_HOLD = 1200, T_RET = 3200, T_REST = 550;
  let phase = 0, phaseStart = 0, built = false, raf = 0;

  function tick(now) {
    if (!built) { build(); built = true; phase = 0; phaseStart = now; }
    const el = now - phaseStart; let p;
    if (phase === 0) { p = ease(Math.min(1, el / T_GROW)); if (el >= T_GROW) { phase = 1; phaseStart = now; } }
    else if (phase === 1) { p = 1; if (el >= T_HOLD) { phase = 2; phaseStart = now; } }
    else if (phase === 2) { p = ease(1 - Math.min(1, el / T_RET)); if (el >= T_RET) { phase = 3; phaseStart = now; } }
    else { p = 0; if (el >= T_REST) built = false; }                            // re-emerge from the SAME origin
    draw(p);
    raf = requestAnimationFrame(tick);
  }

  // reduced motion: draw one full static tree (deferred a frame so layout is ready)
  if (reduce) { requestAnimationFrame(() => { resize(); build(); draw(1); }); return; }

  // Otherwise animate. rAF is throttled by the browser when the tab is hidden, so no
  // visibility bookkeeping is needed — keeping it simple avoids the start/resume races.
  raf = requestAnimationFrame(tick);
})();
