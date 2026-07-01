// spiral-forming.js — the "still forming" logo (About page).
//
// A single spiral in the recursive.eco hero purple, golden growth (ln(φ)/(π·½)),
// drawn from ONE origin as a crowd of small marks. Where a loop would close back
// into a circle, it instead BREAKS at a random angle and keeps going in a new
// direction — so it never quite closes; it wanders outward from the centre, then
// withdraws to that same origin and sets out again, differently. Honours
// prefers-reduced-motion (one static form).
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
  const PURPLE = ['#9333ea', '#a855f7', '#8b5cf6', '#7c3aed', '#b083f0'];   // the hero purple family
  const GOLD = ['#b8902f', '#9a7322'];
  const hue = () => (Math.random() < 0.15 ? GOLD : PURPLE)[(Math.random() * (Math.random() < 0.15 ? 2 : 5)) | 0];

  let path = [];   // ordered segments {x1,y1,x2,y2,hue,a}
  function build() {
    path = [];
    const cx = W / 2, cy = H / 2, dth = 0.085;
    let x = cx, y = cy, th = rand(0, Math.PI * 2), r = rand(1.5, 3), dir = Math.random() < 0.5 ? 1 : -1;
    let g = GROWTH * rand(0.6, 1.0);
    let c0x = x - r * Math.cos(th), c0y = y - r * Math.sin(th);   // this arc's spiral centre
    let sinceBreak = 0, col = hue();
    for (let i = 0; i < 2200; i++) {
      th += dth * dir; r *= Math.exp(g * dth); sinceBreak++;
      const nx = c0x + r * Math.cos(th), ny = c0y + r * Math.sin(th);
      if (nx < -30 || nx > W + 30 || ny < -30 || ny > H + 30) break;   // wandered off — stop
      path.push({ x1: x, y1: y, x2: nx, y2: ny, hue: col, a: rand(0.5, 0.9) });
      x = nx; y = ny;
      // where about a full loop has gone by (it would close into a circle), BREAK to a
      // random new heading and re-anchor — so it opens off in a new direction, not a circle.
      if (r > 7 && sinceBreak > (Math.PI * 2 / dth) * rand(0.6, 1.1)) {
        th += rand(-1, 1) * rand(0.5, 1.6);
        if (Math.random() < 0.35) dir = -dir;
        g = GROWTH * rand(0.5, 0.95);
        c0x = x - r * Math.cos(th); c0y = y - r * Math.sin(th);
        if (Math.random() < 0.4) col = hue();
        sinceBreak = 0;
      }
    }
  }

  function draw(progress) {
    ctx.clearRect(0, 0, W, H);
    ctx.lineCap = 'round';
    const n = Math.floor(progress * path.length);
    for (let i = 0; i < n; i++) {
      const s = path[i];
      ctx.strokeStyle = s.hue; ctx.globalAlpha = s.a;
      ctx.lineWidth = 1.0 + (i / Math.max(1, path.length)) * 1.6;   // thin at the origin, fuller as it wanders out
      ctx.beginPath(); ctx.moveTo(s.x1, s.y1); ctx.lineTo(s.x2, s.y2); ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  window.addEventListener('resize', () => { resize(); build(); });

  const ease = t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  const T_GROW = 4600, T_HOLD = 1200, T_RET = 3200, T_REST = 550;
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
