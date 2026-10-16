import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    page_title="Fruit Ninja 2",
    page_icon="🍉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit default UI
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {margin: 0; padding: 0;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    iframe {border: none; width: 100vw; height: 100vh;}
    </style>
    """,
    unsafe_allow_html=True,
)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>Fruit Ninja 2</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  html, body {
    width: 100%; height: 100%;
    overflow: hidden;
    background: #0a1f0a;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    touch-action: none;
    user-select: none;
    -webkit-user-select: none;
  }
  #game-container {
    position: relative;
    width: 100%;
    height: 100%;
    max-width: 480px;
    margin: 0 auto;
    background: linear-gradient(180deg, #87CEEB 0%, #98D8C8 40%, #7CB342 70%, #558B2F 100%);
    overflow: hidden;
  }
  canvas {
    display: block;
    width: 100%;
    height: 100%;
    touch-action: none;
  }
  .ui-overlay {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 10;
  }
  .hud {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 12px 16px;
    color: #fff;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    font-weight: 700;
    font-size: 18px;
  }
  .score-box, .lives-box, .timer-box {
    background: rgba(0,0,0,0.35);
    border-radius: 12px;
    padding: 6px 14px;
    backdrop-filter: blur(4px);
  }
  .lives-box span { color: #ff5252; margin-left: 4px; }
  #pause-btn {
    pointer-events: auto;
    background: rgba(0,0,0,0.4);
    border: none;
    color: #fff;
    width: 40px; height: 40px;
    border-radius: 50%;
    font-size: 18px;
    cursor: pointer;
  }
  .screen {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(180deg, rgba(10,40,20,0.92) 0%, rgba(20,60,30,0.95) 100%);
    z-index: 20;
    pointer-events: auto;
    padding: 20px;
    text-align: center;
  }
  .screen.hidden { display: none; }
  .logo {
    font-size: 42px;
    font-weight: 900;
    background: linear-gradient(90deg, #ff1744, #ff9100, #ffea00, #00e676, #2979ff, #d500f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
    letter-spacing: 1px;
    text-shadow: none;
  }
  .logo span { font-size: 28px; display: block; color: #fff; -webkit-text-fill-color: #fff; margin-top: 4px; }
  .btn {
    background: linear-gradient(180deg, #ff6b00, #e65100);
    border: none;
    color: #fff;
    font-size: 20px;
    font-weight: 700;
    padding: 14px 48px;
    border-radius: 50px;
    margin: 10px 0;
    cursor: pointer;
    box-shadow: 0 6px 0 #bf360c, 0 8px 16px rgba(0,0,0,0.3);
    transition: transform 0.1s, box-shadow 0.1s;
    min-width: 220px;
  }
  .btn:active { transform: translateY(4px); box-shadow: 0 2px 0 #bf360c; }
  .btn.secondary {
    background: linear-gradient(180deg, #546e7a, #37474f);
    box-shadow: 0 6px 0 #263238, 0 8px 16px rgba(0,0,0,0.3);
  }
  .btn.green {
    background: linear-gradient(180deg, #43a047, #2e7d32);
    box-shadow: 0 6px 0 #1b5e20, 0 8px 16px rgba(0,0,0,0.3);
  }
  .mode-select { margin: 16px 0; }
  .mode-select label {
    display: inline-block;
    margin: 6px;
    padding: 10px 18px;
    background: rgba(255,255,255,0.15);
    border-radius: 20px;
    color: #fff;
    cursor: pointer;
    font-size: 15px;
  }
  .mode-select input { display: none; }
  .mode-select input:checked + label {
    background: #ff6b00;
    box-shadow: 0 0 12px rgba(255,107,0,0.6);
  }
  .highscore {
    color: #ffd740;
    font-size: 16px;
    margin: 12px 0;
  }
  .instructions {
    color: #b0bec5;
    font-size: 14px;
    max-width: 320px;
    line-height: 1.5;
    margin-top: 12px;
  }
  .gameover-score {
    font-size: 48px;
    color: #ffd740;
    font-weight: 900;
    margin: 12px 0;
  }
  .combo-text {
    position: absolute;
    font-size: 28px;
    font-weight: 900;
    color: #ffea00;
    text-shadow: 0 0 10px #ff6b00, 0 2px 4px #000;
    pointer-events: none;
    z-index: 15;
    animation: comboPop 0.8s ease-out forwards;
  }
  @keyframes comboPop {
    0% { transform: scale(0.5); opacity: 1; }
    70% { transform: scale(1.3); opacity: 1; }
    100% { transform: scale(1.5); opacity: 0; }
  }
  .sound-toggle {
    position: absolute;
    top: 12px; right: 16px;
    background: rgba(0,0,0,0.4);
    border: none;
    color: #fff;
    width: 40px; height: 40px;
    border-radius: 50%;
    font-size: 18px;
    cursor: pointer;
    z-index: 25;
    pointer-events: auto;
  }
  .settings-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 260px;
    margin: 10px 0;
    color: #fff;
    font-size: 16px;
  }
  .settings-row input[type=range] { width: 120px; }
</style>
</head>
<body>
<div id="game-container">
  <canvas id="gameCanvas"></canvas>
  <div class="ui-overlay">
    <div class="hud" id="hud" style="display:none;">
      <div class="score-box">🍉 <span id="score">0</span></div>
      <div class="timer-box" id="timer-box" style="display:none;">⏱ <span id="timer">60</span></div>
      <div class="lives-box" id="lives-box">❤ <span id="lives">3</span></div>
      <button id="pause-btn">⏸</button>
    </div>
  </div>

  <!-- Start Screen -->
  <div class="screen" id="start-screen">
    <div class="logo">FRUIT NINJA<span>2</span></div>
    <div class="highscore">High Score: <span id="high-score">0</span></div>
    <div class="mode-select">
      <input type="radio" name="mode" id="mode-classic" value="classic" checked>
      <label for="mode-classic">Classic</label>
      <input type="radio" name="mode" id="mode-arcade" value="arcade">
      <label for="mode-arcade">Arcade</label>
      <input type="radio" name="mode" id="mode-zen" value="zen">
      <label for="mode-zen">Zen</label>
    </div>
    <button class="btn" id="play-btn">PLAY</button>
    <button class="btn secondary" id="settings-btn">SETTINGS</button>
    <p class="instructions">
      Swipe to slice fruits • Avoid bombs<br>
      Miss fruits = lose life • Combo for bonus
    </p>
  </div>

  <!-- Settings Screen -->
  <div class="screen hidden" id="settings-screen">
    <div class="logo" style="font-size:28px;">SETTINGS</div>
    <div class="settings-row">
      <span>Sound</span>
      <button class="btn secondary" id="sound-toggle-settings" style="min-width:80px;padding:8px 16px;font-size:14px;">ON</button>
    </div>
    <div class="settings-row">
      <span>Volume</span>
      <input type="range" id="volume-slider" min="0" max="100" value="70">
    </div>
    <button class="btn green" id="back-btn">BACK</button>
  </div>

  <!-- Pause Screen -->
  <div class="screen hidden" id="pause-screen">
    <div class="logo" style="font-size:32px;">PAUSED</div>
    <button class="btn" id="resume-btn">RESUME</button>
    <button class="btn secondary" id="restart-btn">RESTART</button>
    <button class="btn secondary" id="menu-btn">MENU</button>
  </div>

  <!-- Game Over Screen -->
  <div class="screen hidden" id="gameover-screen">
    <div class="logo" style="font-size:32px;">GAME OVER</div>
    <div class="gameover-score" id="final-score">0</div>
    <div class="highscore">Best: <span id="final-high">0</span></div>
    <button class="btn" id="again-btn">PLAY AGAIN</button>
    <button class="btn secondary" id="menu2-btn">MENU</button>
  </div>

  <button class="sound-toggle" id="sound-btn" style="display:none;">🔊</button>
</div>

<script>
(function() {
  // ========== CONFIG ==========
  const FRUIT_TYPES = [
    { name: 'watermelon', color: '#e53935', halfColor: '#c62828', radius: 32, points: 10, juice: '#ff5252' },
    { name: 'apple', color: '#f44336', halfColor: '#d32f2f', radius: 22, points: 8, juice: '#ff8a80' },
    { name: 'orange', color: '#ff9800', halfColor: '#f57c00', radius: 24, points: 8, juice: '#ffcc80' },
    { name: 'banana', color: '#ffeb3b', halfColor: '#fdd835', radius: 20, points: 6, juice: '#fff59d' },
    { name: 'pineapple', color: '#ffc107', halfColor: '#ffa000', radius: 26, points: 12, juice: '#ffe082' },
    { name: 'kiwi', color: '#8bc34a', halfColor: '#689f38', radius: 18, points: 7, juice: '#c5e1a5' },
    { name: 'strawberry', color: '#e91e63', halfColor: '#c2185b', radius: 16, points: 9, juice: '#f48fb1' },
  ];

  // ========== STATE ==========
  let canvas, ctx;
  let W = 0, H = 0;
  let fruits = [];
  let particles = [];
  let blades = [];
  let score = 0;
  let lives = 3;
  let highScore = 0;
  let gameMode = 'classic';
  let isPlaying = false;
  let isPaused = false;
  let soundOn = true;
  let volume = 0.7;
  let lastTime = 0;
  let spawnTimer = 0;
  let difficulty = 1;
  let timer = 60;
  let combo = 0;
  let comboTimer = 0;
  let slicePoints = [];
  let isSlicing = false;
  let audioCtx = null;
  let animId = null;

  // ========== AUDIO ==========
  function initAudio() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
  }

  function playTone(freq, duration, type = 'sine', vol = 0.3) {
    if (!soundOn || !audioCtx) return;
    try {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      gain.gain.setValueAtTime(vol * volume, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + duration);
    } catch(e) {}
  }

  function playSlice() {
    playTone(800 + Math.random()*400, 0.08, 'square', 0.2);
    playTone(400 + Math.random()*200, 0.12, 'sawtooth', 0.15);
  }

  function playBomb() {
    playTone(80, 0.4, 'sawtooth', 0.4);
    playTone(40, 0.5, 'square', 0.3);
  }

  function playMiss() {
    playTone(150, 0.2, 'triangle', 0.25);
  }

  function playCombo() {
    playTone(600, 0.1, 'sine', 0.3);
    setTimeout(() => playTone(900, 0.15, 'sine', 0.3), 80);
  }

  // ========== UTILS ==========
  function rand(min, max) { return Math.random() * (max - min) + min; }
  function dist(x1,y1,x2,y2) { return Math.hypot(x2-x1, y2-y1); }

  function lineCircleIntersect(x1,y1,x2,y2, cx,cy,r) {
    const dx = x2 - x1;
    const dy = y2 - y1;
    const len = Math.hypot(dx, dy);
    if (len < 1) return dist(x1,y1,cx,cy) < r;
    const t = Math.max(0, Math.min(1, ((cx-x1)*dx + (cy-y1)*dy) / (len*len)));
    const px = x1 + t * dx;
    const py = y1 + t * dy;
    return dist(px,py,cx,cy) < r;
  }

  // ========== ENTITIES ==========
  function createFruit(isBomb = false) {
    const type = isBomb ? null : FRUIT_TYPES[Math.floor(Math.random() * FRUIT_TYPES.length)];
    const fromLeft = Math.random() < 0.5;
    const x = fromLeft ? rand(-40, W*0.3) : rand(W*0.7, W+40);
    const y = H + 40;
    const speed = rand(8, 14) * (0.8 + difficulty * 0.15);
    const angle = fromLeft ? rand(-Math.PI*0.7, -Math.PI*0.3) : rand(-Math.PI*0.7, -Math.PI*0.3);
    return {
      x, y,
      vx: Math.cos(angle) * speed * (fromLeft ? 1 : -1) * rand(0.6, 1.2),
      vy: -Math.abs(Math.sin(angle) * speed) - rand(4, 9),
      radius: isBomb ? 26 : type.radius,
      type: isBomb ? 'bomb' : type.name,
      color: isBomb ? '#333' : type.color,
      halfColor: isBomb ? '#111' : type.halfColor,
      juice: isBomb ? '#ff1744' : type.juice,
      points: isBomb ? 0 : type.points,
      rotation: rand(0, Math.PI*2),
      rotSpeed: rand(-0.15, 0.15),
      sliced: false,
      halves: null,
      life: 1,
      isBomb
    };
  }

  function createParticles(x, y, color, count = 12) {
    for (let i = 0; i < count; i++) {
      particles.push({
        x, y,
        vx: rand(-6, 6),
        vy: rand(-8, 2),
        life: 1,
        decay: rand(0.02, 0.05),
        color,
        size: rand(3, 8)
      });
    }
  }

  function createBlade(points) {
    if (points.length < 2) return;
    blades.push({
      points: points.map(p => ({...p})),
      life: 1,
      decay: 0.08
    });
  }

  // ========== DRAWING ==========
  function drawBackground() {
    // Sky gradient already in CSS, draw ground details
    ctx.save();
    // Soft hills
    ctx.fillStyle = 'rgba(76, 175, 80, 0.3)';
    ctx.beginPath();
    ctx.moveTo(0, H * 0.75);
    for (let x = 0; x <= W; x += 40) {
      ctx.quadraticCurveTo(x + 20, H * 0.75 - 30 + Math.sin(x*0.02)*20, x + 40, H * 0.75);
    }
    ctx.lineTo(W, H);
    ctx.lineTo(0, H);
    ctx.fill();

    // Simple pagoda silhouettes
    ctx.fillStyle = 'rgba(60, 40, 20, 0.25)';
    drawPagoda(W * 0.15, H * 0.55, 0.6);
    drawPagoda(W * 0.85, H * 0.5, 0.7);
    ctx.restore();
  }

  function drawPagoda(x, y, scale) {
    ctx.save();
    ctx.translate(x, y);
    ctx.scale(scale, scale);
    // Base
    ctx.fillRect(-25, 0, 50, 40);
    // Roof layers
    for (let i = 0; i < 3; i++) {
      const w = 40 - i * 8;
      const h = -20 - i * 18;
      ctx.beginPath();
      ctx.moveTo(-w/2 - 8, h + 15);
      ctx.lineTo(0, h);
      ctx.lineTo(w/2 + 8, h + 15);
      ctx.closePath();
      ctx.fill();
      ctx.fillRect(-w/2, h + 15, w, 12);
    }
    ctx.restore();
  }

  function drawFruit(f) {
    if (f.sliced && f.halves) {
      f.halves.forEach(h => drawHalf(h, f));
      return;
    }
    ctx.save();
    ctx.translate(f.x, f.y);
    ctx.rotate(f.rotation);

    if (f.isBomb) {
      // Bomb body
      ctx.beginPath();
      ctx.arc(0, 0, f.radius, 0, Math.PI * 2);
      ctx.fillStyle = '#222';
      ctx.fill();
      ctx.strokeStyle = '#555';
      ctx.lineWidth = 3;
      ctx.stroke();
      // Fuse
      ctx.beginPath();
      ctx.moveTo(0, -f.radius);
      ctx.quadraticCurveTo(8, -f.radius - 12, 4, -f.radius - 20);
      ctx.strokeStyle = '#8d6e63';
      ctx.lineWidth = 3;
      ctx.stroke();
      // Spark
      ctx.beginPath();
      ctx.arc(4, -f.radius - 20, 4, 0, Math.PI*2);
      ctx.fillStyle = '#ffeb3b';
      ctx.fill();
      // Face
      ctx.fillStyle = '#fff';
      ctx.beginPath();
      ctx.arc(-8, -4, 4, 0, Math.PI*2);
      ctx.arc(8, -4, 4, 0, Math.PI*2);
      ctx.fill();
      ctx.fillStyle = '#000';
      ctx.beginPath();
      ctx.arc(-8, -4, 2, 0, Math.PI*2);
      ctx.arc(8, -4, 2, 0, Math.PI*2);
      ctx.fill();
    } else {
      // Fruit body
      ctx.beginPath();
      ctx.arc(0, 0, f.radius, 0, Math.PI * 2);
      const grad = ctx.createRadialGradient(-f.radius*0.3, -f.radius*0.3, 0, 0, 0, f.radius);
      grad.addColorStop(0, lighten(f.color, 40));
      grad.addColorStop(1, f.color);
      ctx.fillStyle = grad;
      ctx.fill();
      ctx.strokeStyle = 'rgba(0,0,0,0.2)';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Stem / leaf for some
      if (f.type === 'apple' || f.type === 'watermelon') {
        ctx.fillStyle = '#4caf50';
        ctx.beginPath();
        ctx.ellipse(0, -f.radius + 2, 4, 8, 0, 0, Math.PI*2);
        ctx.fill();
      }
      if (f.type === 'pineapple') {
        ctx.fillStyle = '#558b2f';
        for (let i = -2; i <= 2; i++) {
          ctx.beginPath();
          ctx.moveTo(i*5, -f.radius);
          ctx.lineTo(i*5 - 3, -f.radius - 12);
          ctx.lineTo(i*5 + 3, -f.radius - 12);
          ctx.fill();
        }
      }
    }
    ctx.restore();
  }

  function drawHalf(h, f) {
    ctx.save();
    ctx.translate(h.x, h.y);
    ctx.rotate(h.rotation);
    ctx.beginPath();
    ctx.arc(0, 0, f.radius, h.startAngle, h.endAngle);
    ctx.lineTo(0, 0);
    ctx.closePath();
    ctx.fillStyle = f.halfColor;
    ctx.fill();
    ctx.strokeStyle = 'rgba(0,0,0,0.15)';
    ctx.lineWidth = 1;
    ctx.stroke();
    // Juice edge
    ctx.beginPath();
    ctx.arc(0, 0, f.radius * 0.7, h.startAngle, h.endAngle);
    ctx.strokeStyle = f.juice;
    ctx.lineWidth = 3;
    ctx.stroke();
    ctx.restore();
  }

  function lighten(hex, percent) {
    const num = parseInt(hex.slice(1), 16);
    const r = Math.min(255, (num >> 16) + percent);
    const g = Math.min(255, ((num >> 8) & 0x00FF) + percent);
    const b = Math.min(255, (num & 0x0000FF) + percent);
    return `rgb(${r},${g},${b})`;
  }

  function drawParticles() {
    particles.forEach(p => {
      ctx.globalAlpha = p.life;
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI*2);
      ctx.fill();
    });
    ctx.globalAlpha = 1;
  }

  function drawBlades() {
    blades.forEach(b => {
      if (b.points.length < 2) return;
      ctx.save();
      ctx.globalAlpha = b.life;
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 4;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.shadowColor = '#ffea00';
      ctx.shadowBlur = 12;
      ctx.beginPath();
      ctx.moveTo(b.points[0].x, b.points[0].y);
      for (let i = 1; i < b.points.length; i++) {
        ctx.lineTo(b.points[i].x, b.points[i].y);
      }
      ctx.stroke();
      // Glow core
      ctx.strokeStyle = '#ffea00';
      ctx.lineWidth = 2;
      ctx.shadowBlur = 0;
      ctx.stroke();
      ctx.restore();
    });
  }

  // ========== GAME LOGIC ==========
  function spawnFruits(dt) {
    spawnTimer -= dt;
    if (spawnTimer <= 0) {
      const count = Math.min(1 + Math.floor(difficulty / 2), 4);
      for (let i = 0; i < count; i++) {
        const bombChance = gameMode === 'zen' ? 0 : (0.08 + difficulty * 0.02);
        fruits.push(createFruit(Math.random() < bombChance));
      }
      spawnTimer = rand(0.6, 1.4) / (0.7 + difficulty * 0.2);
    }
  }

  function update(dt) {
    if (!isPlaying || isPaused) return;

    // Difficulty ramp
    difficulty += dt * 0.015;

    // Timer for Arcade
    if (gameMode === 'arcade') {
      timer -= dt;
      document.getElementById('timer').textContent = Math.max(0, Math.ceil(timer));
      if (timer <= 0) {
        endGame();
        return;
      }
    }

    // Combo decay
    comboTimer -= dt;
    if (comboTimer <= 0) combo = 0;

    spawnFruits(dt);

    // Update fruits
    for (let i = fruits.length - 1; i >= 0; i--) {
      const f = fruits[i];
      if (f.sliced && f.halves) {
        f.halves.forEach(h => {
          h.x += h.vx * dt * 60;
          h.y += h.vy * dt * 60;
          h.vy += 0.4 * dt * 60;
          h.rotation += h.rotSpeed;
          h.life -= dt * 1.5;
        });
        if (f.halves[0].life <= 0) fruits.splice(i, 1);
        continue;
      }

      f.x += f.vx * dt * 60;
      f.y += f.vy * dt * 60;
      f.vy += 0.25 * dt * 60; // gravity
      f.rotation += f.rotSpeed;

      // Missed fruit
      if (f.y > H + 60 && !f.sliced) {
        if (!f.isBomb && gameMode !== 'zen') {
          lives--;
          updateHUD();
          playMiss();
          if (lives <= 0) {
            endGame();
            return;
          }
        }
        fruits.splice(i, 1);
      }
    }

    // Particles
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.2;
      p.life -= p.decay;
      if (p.life <= 0) particles.splice(i, 1);
    }

    // Blades
    for (let i = blades.length - 1; i >= 0; i--) {
      blades[i].life -= blades[i].decay;
      if (blades[i].life <= 0) blades.splice(i, 1);
    }
  }

  function trySlice(x1, y1, x2, y2) {
    let slicedAny = false;
    for (let i = fruits.length - 1; i >= 0; i--) {
      const f = fruits[i];
      if (f.sliced) continue;
      if (lineCircleIntersect(x1, y1, x2, y2, f.x, f.y, f.radius + 8)) {
        f.sliced = true;
        slicedAny = true;

        if (f.isBomb) {
          // Bomb hit
          createParticles(f.x, f.y, '#ff1744', 25);
          createParticles(f.x, f.y, '#ffeb3b', 15);
          playBomb();
          if (navigator.vibrate) navigator.vibrate(200);
          if (gameMode === 'classic' || gameMode === 'arcade') {
            lives = 0;
            updateHUD();
            endGame();
            return;
          }
          fruits.splice(i, 1);
        } else {
          // Slice fruit
          const angle = Math.atan2(y2 - y1, x2 - x1);
          f.halves = [
            { x: f.x, y: f.y, vx: Math.cos(angle + 0.8) * 4, vy: Math.sin(angle + 0.8) * 3 - 2,
              rotation: f.rotation, rotSpeed: -0.2, life: 1, startAngle: angle, endAngle: angle + Math.PI },
            { x: f.x, y: f.y, vx: Math.cos(angle - 0.8) * 4, vy: Math.sin(angle - 0.8) * 3 - 2,
              rotation: f.rotation, rotSpeed: 0.2, life: 1, startAngle: angle + Math.PI, endAngle: angle + Math.PI * 2 }
          ];
          createParticles(f.x, f.y, f.juice, 14);
          playSlice();
          if (navigator.vibrate) navigator.vibrate(30);

          combo++;
          comboTimer = 1.2;
          let pts = f.points;
          if (combo >= 3) {
            pts = Math.floor(pts * (1 + combo * 0.3));
            showCombo(f.x, f.y, combo);
            playCombo();
          }
          score += pts;
          updateHUD();
        }
      }
    }
    return slicedAny;
  }

  function showCombo(x, y, n) {
    const el = document.createElement('div');
    el.className = 'combo-text';
    el.textContent = n + 'x COMBO!';
    el.style.left = (x - 40) + 'px';
    el.style.top = (y - 40) + 'px';
    document.getElementById('game-container').appendChild(el);
    setTimeout(() => el.remove(), 800);
  }

  function updateHUD() {
    document.getElementById('score').textContent = score;
    document.getElementById('lives').textContent = lives;
  }

  // ========== RENDER ==========
  function render() {
    ctx.clearRect(0, 0, W, H);
    drawBackground();
    fruits.forEach(drawFruit);
    drawParticles();
    drawBlades();

    // Active slice trail
    if (isSlicing && slicePoints.length > 1) {
      ctx.save();
      ctx.strokeStyle = 'rgba(255,255,255,0.9)';
      ctx.lineWidth = 5;
      ctx.lineCap = 'round';
      ctx.shadowColor = '#ffea00';
      ctx.shadowBlur = 15;
      ctx.beginPath();
      ctx.moveTo(slicePoints[0].x, slicePoints[0].y);
      for (let i = 1; i < slicePoints.length; i++) {
        ctx.lineTo(slicePoints[i].x, slicePoints[i].y);
      }
      ctx.stroke();
      ctx.restore();
    }
  }

  function loop(timestamp) {
    const dt = Math.min((timestamp - lastTime) / 1000, 0.05);
    lastTime = timestamp;
    update(dt);
    render();
    animId = requestAnimationFrame(loop);
  }

  // ========== INPUT ==========
  function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    let clientX, clientY;
    if (e.touches && e.touches.length) {
      clientX = e.touches[0].clientX;
      clientY = e.touches[0].clientY;
    } else {
      clientX = e.clientX;
      clientY = e.clientY;
    }
    return {
      x: (clientX - rect.left) * scaleX,
      y: (clientY - rect.top) * scaleY
    };
  }

  function onStart(e) {
    if (!isPlaying || isPaused) return;
    e.preventDefault();
    initAudio();
    isSlicing = true;
    slicePoints = [getPos(e)];
  }

  function onMove(e) {
    if (!isSlicing || !isPlaying || isPaused) return;
    e.preventDefault();
    const p = getPos(e);
    const last = slicePoints[slicePoints.length - 1];
    if (dist(last.x, last.y, p.x, p.y) > 8) {
      slicePoints.push(p);
      if (slicePoints.length > 20) slicePoints.shift();
      // Check slice between last two points
      trySlice(last.x, last.y, p.x, p.y);
    }
  }

  function onEnd(e) {
    if (!isSlicing) return;
    e.preventDefault();
    if (slicePoints.length > 1) {
      createBlade(slicePoints);
    }
    isSlicing = false;
    slicePoints = [];
  }

  // ========== SCREENS & CONTROLS ==========
  function showScreen(id) {
    ['start-screen', 'settings-screen', 'pause-screen', 'gameover-screen'].forEach(s => {
      document.getElementById(s).classList.toggle('hidden', s !== id);
    });
    document.getElementById('hud').style.display = (id === null) ? 'flex' : 'none';
    document.getElementById('sound-btn').style.display = (id === null) ? 'block' : 'none';
  }

  function startGame() {
    initAudio();
    if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();

    gameMode = document.querySelector('input[name="mode"]:checked').value;
    score = 0;
    lives = gameMode === 'zen' ? 99 : 3;
    difficulty = 1;
    timer = 60;
    combo = 0;
    fruits = [];
    particles = [];
    blades = [];
    isPlaying = true;
    isPaused = false;
    spawnTimer = 0.5;

    document.getElementById('lives-box').style.display = gameMode === 'zen' ? 'none' : 'block';
    document.getElementById('timer-box').style.display = gameMode === 'arcade' ? 'block' : 'none';
    updateHUD();
    showScreen(null);
    lastTime = performance.now();
  }

  function endGame() {
    isPlaying = false;
    if (score > highScore) {
      highScore = score;
      localStorage.setItem('fn2_highscore', highScore);
    }
    document.getElementById('final-score').textContent = score;
    document.getElementById('final-high').textContent = highScore;
    document.getElementById('high-score').textContent = highScore;
    showScreen('gameover-screen');
  }

  function pauseGame() {
    if (!isPlaying) return;
    isPaused = true;
    showScreen('pause-screen');
  }

  function resumeGame() {
    isPaused = false;
    showScreen(null);
    lastTime = performance.now();
  }

  // ========== INIT ==========
  function resize() {
    const container = document.getElementById('game-container');
    const rect = container.getBoundingClientRect();
    W = Math.floor(rect.width * (window.devicePixelRatio || 1));
    H = Math.floor(rect.height * (window.devicePixelRatio || 1));
    // Cap for performance on mobile
    const maxDim = 900;
    if (W > maxDim || H > maxDim) {
      const scale = maxDim / Math.max(W, H);
      W = Math.floor(W * scale);
      H = Math.floor(H * scale);
    }
    canvas.width = W;
    canvas.height = H;
    canvas.style.width = rect.width + 'px';
    canvas.style.height = rect.height + 'px';
  }

  function init() {
    canvas = document.getElementById('gameCanvas');
    ctx = canvas.getContext('2d');
    highScore = parseInt(localStorage.getItem('fn2_highscore') || '0', 10);
    document.getElementById('high-score').textContent = highScore;

    resize();
    window.addEventListener('resize', resize);
    window.addEventListener('orientationchange', () => setTimeout(resize, 200));

    // Input
    canvas.addEventListener('mousedown', onStart);
    canvas.addEventListener('mousemove', onMove);
    canvas.addEventListener('mouseup', onEnd);
    canvas.addEventListener('mouseleave', onEnd);
    canvas.addEventListener('touchstart', onStart, {passive: false});
    canvas.addEventListener('touchmove', onMove, {passive: false});
    canvas.addEventListener('touchend', onEnd, {passive: false});
    canvas.addEventListener('touchcancel', onEnd, {passive: false});

    // Buttons
    document.getElementById('play-btn').onclick = startGame;
    document.getElementById('settings-btn').onclick = () => showScreen('settings-screen');
    document.getElementById('back-btn').onclick = () => showScreen('start-screen');
    document.getElementById('pause-btn').onclick = pauseGame;
    document.getElementById('resume-btn').onclick = resumeGame;
    document.getElementById('restart-btn').onclick = () => { isPaused = false; startGame(); };
    document.getElementById('menu-btn').onclick = () => { isPlaying = false; isPaused = false; showScreen('start-screen'); };
    document.getElementById('again-btn').onclick = startGame;
    document.getElementById('menu2-btn').onclick = () => showScreen('start-screen');

    const soundBtn = document.getElementById('sound-btn');
    const soundSettings = document.getElementById('sound-toggle-settings');
    function toggleSound() {
      soundOn = !soundOn;
      soundBtn.textContent = soundOn ? '🔊' : '🔇';
      soundSettings.textContent = soundOn ? 'ON' : 'OFF';
    }
    soundBtn.onclick = toggleSound;
    soundSettings.onclick = toggleSound;

    document.getElementById('volume-slider').oninput = (e) => {
      volume = e.target.value / 100;
    };

    // Start render loop
    lastTime = performance.now();
    animId = requestAnimationFrame(loop);
  }

  // Prevent scroll / bounce on iOS
  document.body.addEventListener('touchmove', e => {
    if (e.target === canvas || e.target.closest('#game-container')) {
      e.preventDefault();
    }
  }, {passive: false});

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
</body>
</html>
"""

# Embed the game at full viewport height
html(GAME_HTML, height=800, scrolling=False)
