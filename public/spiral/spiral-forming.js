// spiral-forming.js — the "still forming" logo (About page).
//
// It BEGINS as the exact recursive.eco hero spiral: a golden logarithmic spiral
// (growth ln(φ)/(π·½)) drawn from the centre at angle 0, in the hero purple — the
// same start, deterministically, every time. Where the hero would cap its radius
// and close into a circle, this one instead BREAKS at a random angle and keeps
// going in a new direction — wandering outward, then withdrawing to the same
// origin to set out again (a new wander each time, but always the same beginning).
// Honours prefers-reduced-motion (one static form).
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
  const GROWTH = Math.log(PHI) / (Math.PI / 2);   // exactly the hero spiral's growth rate
  const HUE = '#9333ea';                           // the hero purple
  const rand = (a, b) => a + Math.random() * (b - a);

  let path = [];   // ordered segments {x1,y1,x2,y2}
  function build() {
    path = [];
    const cx = W / 2, cy = H / 2, dth = 0.04;
    const breakR = Math.min(W, H) * 0.30;          // where the hero would cap & circle → we break instead
    // ── deterministic hero beginning: centre, angle 0, +turn, golden growth ──
    let th = 0, r = 1, dir = 1, g = GROWTH, c0x = cx, c0y = cy;
    let px = cx + r, py = cy;                        // first point at angle 0 (matches the hero)
    let broken = false, sinceBreak = 0;
    for (let i = 0; i < 3200; i++) {
      th += dth * dir; r *= Math.exp(g * dth); sinceBreak++;
      const nx = c0x + r * Math.cos(th), ny = c0y + r * Math.sin(th);
      if (nx < -30 || nx > W + 30 || ny < -30 || ny > H + 30) break;   // wandered off
      path.push({ x1: px, y1: py, x2: nx, y2: ny });
      px = nx; py = ny;
      if (!broken) {
        // FIRST break — exactly where the hero would stop spiralling and close a circle
        if (r > breakR) {
          broken = true;
          th += rand(-1, 1) * rand(0.6, 1.4);
          if (Math.random() < 0.4) dir = -dir;
          g = GROWTH * rand(0.5, 0.95);
          r *= rand(0.45, 0.7);                       // re-anchor: keep the point, veer off, don't close the ring
          c0x = px - r * Math.cos(th); c0y = py - r * Math.sin(th);
          sinceBreak = 0;
        }
      } else if (r > 7 && sinceBreak > (Math.PI * 2 / dth) * rand(0.55, 1.0)) {
        // subsequent wandering breaks
        th += rand(-1, 1) * rand(0.5, 1.5);
        if (Math.random() < 0.35) dir = -dir;
        g = GROWTH * rand(0.5, 0.95);
        r *= rand(0.5, 0.8);
        c0x = px - r * Math.cos(th); c0y = py - r * Math.sin(th);
        sinceBreak = 0;
      }
    }
  }

  function draw(progress) {
    ctx.clearRect(0, 0, W, H);
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.strokeStyle = HUE; ctx.lineWidth = 1.6; ctx.globalAlpha = 0.88;
    const n = Math.floor(progress * path.length);
    ctx.beginPath();
    for (let i = 0; i < n; i++) { const s = path[i]; ctx.moveTo(s.x1, s.y1); ctx.lineTo(s.x2, s.y2); }
    ctx.stroke();
    ctx.globalAlpha = 1;
  }

  window.addEventListener('resize', () => { resize(); build(); });

  const ease = t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  const T_GROW = 4600, T_HOLD = 1300, T_RET = 3200, T_REST = 550;
  let phase = 0, phaseStart = 0, built = false, raf = 0;

  function tick(now) {
    if (!built) { build(); built = true; phase = 0; phaseStart = now; }
    const el = now - phaseStart; let p;
    if (phase === 0) { p = ease(Math.min(1, el / T_GROW)); if (el >= T_GROW) { phase = 1; phaseStart = now; } }
    else if (phase === 1) { p = 1; if (el >= T_HOLD) { phase = 2; phaseStart = now; } }
    else if (phase === 2) { p = ease(1 - Math.min(1, el / T_RET)); if (el >= T_RET) { phase = 3; phaseStart = now; } }
    else { p = 0; if (el >= T_REST) built = false; }
    draw(p);
    raf = requestAnimationFrame(tick);
  }

  if (reduce) { requestAnimationFrame(() => { resize(); build(); draw(1); }); return; }
  raf = requestAnimationFrame(tick);
})();
