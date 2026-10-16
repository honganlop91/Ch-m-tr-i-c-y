import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    page_title="Fruit Ninja 2",
    page_icon="🍉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {margin: 0; padding: 0; background: #0a1f0a;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    iframe {border: none !important; width: 100vw !important; height: 100vh !important;}
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
    font-family: 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
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
    overflow: hidden;
    background: #1a3a2a;
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
    padding: 12px 12px;
    color: #fff;
    text-shadow: 0 2px 6px rgba(0,0,0,0.6);
    font-weight: 800;
    font-size: 15px;
    gap: 6px;
    flex-wrap: wrap;
  }
  .score-box, .lives-box, .timer-box, .coins-box, .power-box {
    background: linear-gradient(135deg, rgba(0,0,0,0.45), rgba(0,0,0,0.25));
    border-radius: 12px;
    padding: 6px 11px;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
  }
  .lives-box span { color: #ff5252; margin-left: 2px; }
  .coins-box { color: #ffd740; }
  .power-box { color: #80d8ff; font-size: 13px; }
  #pause-btn {
    pointer-events: auto;
    background: linear-gradient(135deg, rgba(0,0,0,0.5), rgba(0,0,0,0.3));
    border: 1px solid rgba(255,255,255,0.15);
    color: #fff;
    width: 40px; height: 40px;
    border-radius: 50%;
    font-size: 17px;
    cursor: pointer;
    backdrop-filter: blur(8px);
  }
  .screen {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(165deg, rgba(8,30,18,0.95) 0%, rgba(15,50,28,0.97) 50%, rgba(10,35,20,0.98) 100%);
    z-index: 20;
    pointer-events: auto;
    padding: 20px;
    text-align: center;
    overflow-y: auto;
  }
  .screen.hidden { display: none; }
  .logo {
    font-size: 42px;
    font-weight: 900;
    background: linear-gradient(90deg, #ff1744, #ff6d00, #ffea00, #00e676, #00b0ff, #d500f9);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
    letter-spacing: 1px;
    animation: logoShine 4s linear infinite;
    filter: drop-shadow(0 4px 12px rgba(0,0,0,0.4));
  }
  @keyframes logoShine { to { background-position: 200% center; } }
  .logo span {
    font-size: 26px;
    display: block;
    color: #fff;
    -webkit-text-fill-color: #fff;
    margin-top: 2px;
    letter-spacing: 5px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.5);
  }
  .btn {
    background: linear-gradient(180deg, #ff8a00 0%, #e65100 100%);
    border: none;
    color: #fff;
    font-size: 18px;
    font-weight: 800;
    padding: 13px 44px;
    border-radius: 50px;
    margin: 7px 0;
    cursor: pointer;
    box-shadow: 0 6px 0 #bf360c, 0 8px 16px rgba(0,0,0,0.35);
    transition: transform 0.08s, box-shadow 0.08s;
    min-width: 200px;
    letter-spacing: 1px;
    text-shadow: 0 1px 2px rgba(0,0,0,0.3);
  }
  .btn:active { transform: translateY(4px); box-shadow: 0 2px 0 #bf360c; }
  .btn.secondary {
    background: linear-gradient(180deg, #607d8b, #455a64);
    box-shadow: 0 6px 0 #263238, 0 8px 16px rgba(0,0,0,0.35);
  }
  .btn.green {
    background: linear-gradient(180deg, #66bb6a, #2e7d32);
    box-shadow: 0 6px 0 #1b5e20, 0 8px 16px rgba(0,0,0,0.35);
  }
  .btn.purple {
    background: linear-gradient(180deg, #ab47bc, #7b1fa2);
    box-shadow: 0 6px 0 #4a148c, 0 8px 16px rgba(0,0,0,0.35);
  }
  .btn.small {
    min-width: 90px;
    padding: 8px 16px;
    font-size: 13px;
    margin: 4px;
  }
  .btn:disabled {
    opacity: 0.45;
    cursor: not-allowed;
    transform: none !important;
  }
  .mode-select { margin: 14px 0 8px; }
  .mode-select label {
    display: inline-block;
    margin: 4px;
    padding: 9px 16px;
    background: rgba(255,255,255,0.1);
    border-radius: 22px;
    color: #e0e0e0;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.12);
    transition: all 0.2s;
  }
  .mode-select input { display: none; }
  .mode-select input:checked + label {
    background: linear-gradient(135deg, #ff6b00, #ff8f00);
    color: #fff;
    box-shadow: 0 0 16px rgba(255,107,0,0.55);
    border-color: transparent;
  }
  .highscore, .coin-display {
    color: #ffd740;
    font-size: 15px;
    margin: 8px 0;
    font-weight: 600;
    text-shadow: 0 2px 6px rgba(0,0,0,0.4);
  }
  .instructions {
    color: #90a4ae;
    font-size: 13px;
    max-width: 300px;
    line-height: 1.5;
    margin-top: 10px;
  }
  .gameover-score {
    font-size: 52px;
    color: #ffd740;
    font-weight: 900;
    margin: 8px 0;
    text-shadow: 0 0 20px rgba(255,215,64,0.4), 0 4px 8px rgba(0,0,0,0.4);
  }
  .combo-text {
    position: absolute;
    font-size: 28px;
    font-weight: 900;
    color: #ffea00;
    text-shadow: 0 0 14px #ff6b00, 0 0 28px #ff1744, 0 3px 6px #000;
    pointer-events: none;
    z-index: 15;
    animation: comboPop 0.85s cubic-bezier(0.18, 0.89, 0.32, 1.28) forwards;
  }
  @keyframes comboPop {
    0% { transform: scale(0.3) rotate(-8deg); opacity: 0; }
    40% { transform: scale(1.35) rotate(3deg); opacity: 1; }
    100% { transform: scale(1.6) translateY(-30px); opacity: 0; }
  }
  .sound-toggle {
    position: absolute;
    top: 12px; right: 14px;
    background: linear-gradient(135deg, rgba(0,0,0,0.5), rgba(0,0,0,0.3));
    border: 1px solid rgba(255,255,255,0.12);
    color: #fff;
    width: 40px; height: 40px;
    border-radius: 50%;
    font-size: 17px;
    cursor: pointer;
    z-index: 25;
    pointer-events: auto;
    backdrop-filter: blur(8px);
  }
  .settings-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 260px;
    margin: 10px 0;
    color: #e0e0e0;
    font-size: 15px;
    font-weight: 600;
  }
  .settings-row input[type=range] { width: 120px; accent-color: #ff6b00; }

  .shop-grid {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
    max-width: 340px;
    margin: 12px 0;
    max-height: 48vh;
    overflow-y: auto;
    padding: 4px;
  }
  .shop-item {
    display: flex;
    align-items: center;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 12px;
    gap: 12px;
    text-align: left;
  }
  .shop-item.owned {
    border-color: #66bb6a;
    background: rgba(102,187,106,0.12);
  }
  .shop-item.active {
    border-color: #ffd740;
    background: rgba(255,215,64,0.12);
    box-shadow: 0 0 12px rgba(255,215,64,0.25);
  }
  .shop-icon {
    font-size: 28px;
    width: 42px;
    text-align: center;
    flex-shrink: 0;
  }
  .shop-info { flex: 1; min-width: 0; }
  .shop-name {
    color: #fff;
    font-weight: 700;
    font-size: 14px;
  }
  .shop-desc {
    color: #90a4ae;
    font-size: 11.5px;
    margin-top: 2px;
    line-height: 1.3;
  }
  .shop-price {
    color: #ffd740;
    font-weight: 700;
    font-size: 13px;
    white-space: nowrap;
  }
  .active-powers {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    justify-content: center;
    margin: 8px 0;
  }
  .power-tag {
    background: rgba(128,216,255,0.2);
    border: 1px solid rgba(128,216,255,0.4);
    color: #80d8ff;
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 20px;
    font-weight: 600;
  }
</style>
</head>
<body>
<div id="game-container">
  <canvas id="gameCanvas"></canvas>
  <div class="ui-overlay">
    <div class="hud" id="hud" style="display:none;">
      <div class="score-box">🍉 <span id="score">0</span></div>
      <div class="coins-box">🪙 <span id="hud-coins">0</span></div>
      <div class="timer-box" id="timer-box" style="display:none;">⏱ <span id="timer">60</span></div>
      <div class="lives-box" id="lives-box">❤ <span id="lives">3</span></div>
      <div class="power-box" id="power-hud" style="display:none;"></div>
      <button id="pause-btn">⏸</button>
    </div>
  </div>

  <div class="screen" id="start-screen">
    <div class="logo">FRUIT NINJA<span>2</span></div>
    <div class="highscore">🏆 High Score: <span id="high-score">0</span></div>
    <div class="coin-display">🪙 Coins: <span id="menu-coins">0</span></div>
    <div class="mode-select">
      <input type="radio" name="mode" id="mode-classic" value="classic" checked>
      <label for="mode-classic">Classic</label>
      <input type="radio" name="mode" id="mode-arcade" value="arcade">
      <label for="mode-arcade">Arcade</label>
      <input type="radio" name="mode" id="mode-zen" value="zen">
      <label for="mode-zen">Zen</label>
    </div>
    <div class="active-powers" id="active-powers-preview"></div>
    <button class="btn" id="play-btn">PLAY</button>
    <button class="btn purple" id="shop-btn">🛒 SHOP</button>
    <button class="btn secondary" id="settings-btn">SETTINGS</button>
    <p class="instructions">
      Swipe to slice • Avoid bombs<br>
      Earn coins → buy skills in Shop
    </p>
  </div>

  <div class="screen hidden" id="shop-screen">
    <div class="logo" style="font-size:28px;">🛒 SHOP</div>
    <div class="coin-display">🪙 <span id="shop-coins">0</span> coins</div>
    <div class="shop-grid" id="shop-grid"></div>
    <button class="btn green" id="shop-back-btn">BACK</button>
  </div>

  <div class="screen hidden" id="settings-screen">
    <div class="logo" style="font-size:28px;">SETTINGS</div>
    <div class="settings-row">
      <span>Sound</span>
      <button class="btn secondary small" id="sound-toggle-settings">ON</button>
    </div>
    <div class="settings-row">
      <span>Volume</span>
      <input type="range" id="volume-slider" min="0" max="100" value="70">
    </div>
    <button class="btn green" id="back-btn">BACK</button>
  </div>

  <div class="screen hidden" id="pause-screen">
    <div class="logo" style="font-size:32px;">PAUSED</div>
    <button class="btn" id="resume-btn">RESUME</button>
    <button class="btn secondary" id="restart-btn">RESTART</button>
    <button class="btn secondary" id="menu-btn">MENU</button>
  </div>

  <div class="screen hidden" id="gameover-screen">
    <div class="logo" style="font-size:32px;">GAME OVER</div>
    <div class="gameover-score" id="final-score">0</div>
    <div class="highscore">Best: <span id="final-high">0</span></div>
    <div class="coin-display">+🪙 <span id="earned-coins">0</span> coins</div>
    <button class="btn" id="again-btn">PLAY AGAIN</button>
    <button class="btn purple" id="go-shop-btn">🛒 SHOP</button>
    <button class="btn secondary" id="menu2-btn">MENU</button>
  </div>

  <button class="sound-toggle" id="sound-btn" style="display:none;">🔊</button>
</div>

<script>
(function() {
  const SHOP_ITEMS = [
    { id: 'double_score', name: 'Double Score', icon: '✖️2️⃣', desc: 'x2 points for the whole next game', cost: 60, type: 'consumable' },
    { id: 'extra_life', name: 'Extra Life', icon: '❤️', desc: '+1 life at the start of next game', cost: 80, type: 'consumable' },
    { id: 'slow_mo', name: 'Slow Motion', icon: '🐢', desc: 'Fruits move 40% slower next game', cost: 70, type: 'consumable' },
    { id: 'big_blade', name: 'Big Blade', icon: '⚔️', desc: 'Larger slice hitbox next game', cost: 65, type: 'consumable' },
    { id: 'bomb_shield', name: 'Bomb Shield', icon: '🛡️', desc: 'Survive 1 bomb hit next game', cost: 100, type: 'consumable' },
    { id: 'fruit_rain', name: 'Fruit Rain', icon: '🌧️', desc: 'More fruits spawn next game', cost: 55, type: 'consumable' },
    { id: 'lucky', name: 'Lucky Charm', icon: '🍀', desc: 'Fewer bombs appear next game', cost: 75, type: 'consumable' },
    { id: 'critical', name: 'Critical Slice', icon: '💥', desc: '20% chance x3 points per fruit', cost: 90, type: 'consumable' },
    { id: 'max_life', name: 'Max Life +1', icon: '💖', desc: 'Permanently start with +1 life', cost: 250, type: 'permanent' }
  ];

  const FRUIT_TYPES = [
    { name: 'watermelon', radius: 48, points: 12, juice: '#ff1744', rind: '#2e7d32', flesh: '#e53935' },
    { name: 'apple', radius: 34, points: 9, juice: '#ff5252', rind: '#c62828', flesh: '#ef5350' },
    { name: 'orange', radius: 36, points: 8, juice: '#ffab40', rind: '#ef6c00', flesh: '#ff9800' },
    { name: 'banana', radius: 32, points: 7, juice: '#fff59d', rind: '#f9a825', flesh: '#ffee58' },
    { name: 'pineapple', radius: 40, points: 14, juice: '#ffe082', rind: '#f9a825', flesh: '#ffc107' },
    { name: 'kiwi', radius: 30, points: 8, juice: '#c5e1a5', rind: '#6d4c41', flesh: '#8bc34a' },
    { name: 'strawberry', radius: 28, points: 10, juice: '#f48fb1', rind: '#c2185b', flesh: '#e91e63' },
  ];

  let canvas, ctx, W = 0, H = 0;
  let fruits = [], particles = [], blades = [], clouds = [], sparkles = [];
  let score = 0, lives = 3, highScore = 0, coins = 0, sessionCoins = 0;
  let gameMode = 'classic';
  let isPlaying = false, isPaused = false, soundOn = true, volume = 0.7;
  let lastTime = 0, spawnTimer = 0, difficulty = 1, timer = 60;
  let combo = 0, comboTimer = 0;
  let slicePoints = [], isSlicing = false;
  let audioCtx = null, animId = null, bgTime = 0;
  let ownedPerm = {}, equipped = {}, activePowers = {};
  let bombShieldLeft = 0, scoreMult = 1, speedMult = 1, bladeBonus = 0;
  let spawnBonus = 0, bombReduce = 0, critChance = 0;

  function initAudio() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  function playTone(freq, dur, type='sine', vol=0.3) {
    if (!soundOn || !audioCtx) return;
    try {
      const o = audioCtx.createOscillator(), g = audioCtx.createGain();
      o.type = type; o.frequency.setValueAtTime(freq, audioCtx.currentTime);
      g.gain.setValueAtTime(vol * volume, audioCtx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + dur);
      o.connect(g); g.connect(audioCtx.destination);
      o.start(); o.stop(audioCtx.currentTime + dur);
    } catch(e) {}
  }
  function playSlice() {
    playTone(900 + Math.random()*500, 0.07, 'square', 0.18);
    playTone(350 + Math.random()*200, 0.11, 'sawtooth', 0.12);
  }
  function playBomb() {
    playTone(70, 0.45, 'sawtooth', 0.4);
    playTone(35, 0.55, 'square', 0.28);
  }
  function playMiss() { playTone(140, 0.22, 'triangle', 0.22); }
  function playCombo() {
    playTone(620, 0.09, 'sine', 0.28);
    setTimeout(() => playTone(980, 0.14, 'sine', 0.28), 70);
  }
  function playBuy() {
    playTone(520, 0.08, 'sine', 0.25);
    setTimeout(() => playTone(780, 0.12, 'sine', 0.25), 60);
  }

  const rand = (a,b) => Math.random()*(b-a)+a;
  const dist = (x1,y1,x2,y2) => Math.hypot(x2-x1, y2-y1);
  function lineCircle(x1,y1,x2,y2,cx,cy,r) {
    const dx=x2-x1, dy=y2-y1, len=Math.hypot(dx,dy);
    if (len<1) return dist(x1,y1,cx,cy)<r;
    const t=Math.max(0,Math.min(1,((cx-x1)*dx+(cy-y1)*dy)/(len*len)));
    return dist(x1+t*dx, y1+t*dy, cx,cy) < r;
  }
  function lighten(hex, p) {
    const n = parseInt(hex.slice(1),16);
    return `rgb(${Math.min(255,(n>>16)+p)},${Math.min(255,((n>>8)&255)+p)},${Math.min(255,(n&255)+p)})`;
  }

  function loadData() {
    highScore = parseInt(localStorage.getItem('fn2_highscore') || '0', 10);
    coins = parseInt(localStorage.getItem('fn2_coins') || '0', 10);
    try {
      ownedPerm = JSON.parse(localStorage.getItem('fn2_perm') || '{}');
      equipped = JSON.parse(localStorage.getItem('fn2_equipped') || '{}');
    } catch(e) { ownedPerm = {}; equipped = {}; }
  }
  function saveData() {
    localStorage.setItem('fn2_highscore', highScore);
    localStorage.setItem('fn2_coins', coins);
    localStorage.setItem('fn2_perm', JSON.stringify(ownedPerm));
    localStorage.setItem('fn2_equipped', JSON.stringify(equipped));
  }

  function renderShop() {
    const grid = document.getElementById('shop-grid');
    grid.innerHTML = '';
    document.getElementById('shop-coins').textContent = coins;
    SHOP_ITEMS.forEach(item => {
      const isPermOwned = item.type === 'permanent' && ownedPerm[item.id];
      const isEquipped = !!equipped[item.id];
      const canBuy = coins >= item.cost && !isPermOwned;
      const el = document.createElement('div');
      el.className = 'shop-item' + (isPermOwned || isEquipped ? ' owned' : '') + (isEquipped ? ' active' : '');
      el.innerHTML = `
        <div class="shop-icon">${item.icon}</div>
        <div class="shop-info">
          <div class="shop-name">${item.name}</div>
          <div class="shop-desc">${item.desc}</div>
        </div>
        <div>
          ${isPermOwned
            ? '<span class="shop-price" style="color:#66bb6a">OWNED</span>'
            : isEquipped
              ? `<button class="btn small secondary" data-unequip="${item.id}">UNEQUIP</button>`
              : `<button class="btn small" data-buy="${item.id}" ${canBuy ? '' : 'disabled'}>🪙 ${item.cost}</button>`
          }
        </div>`;
      grid.appendChild(el);
    });
    grid.querySelectorAll('[data-buy]').forEach(btn => {
      btn.onclick = () => {
        const id = btn.getAttribute('data-buy');
        const item = SHOP_ITEMS.find(i => i.id === id);
        if (!item || coins < item.cost) return;
        if (item.type === 'permanent' && ownedPerm[id]) return;
        coins -= item.cost;
        if (item.type === 'permanent') ownedPerm[id] = true;
        else equipped[id] = true;
        saveData(); playBuy(); updateCoinDisplays(); renderShop(); updateActivePreview();
      };
    });
    grid.querySelectorAll('[data-unequip]').forEach(btn => {
      btn.onclick = () => {
        delete equipped[btn.getAttribute('data-unequip')];
        saveData(); renderShop(); updateActivePreview();
      };
    });
  }

  function updateActivePreview() {
    const box = document.getElementById('active-powers-preview');
    box.innerHTML = '';
    Object.keys(equipped).forEach(id => {
      const item = SHOP_ITEMS.find(i => i.id === id);
      if (item) {
        const tag = document.createElement('span');
        tag.className = 'power-tag';
        tag.textContent = item.icon + ' ' + item.name;
        box.appendChild(tag);
      }
    });
    if (ownedPerm['max_life']) {
      const tag = document.createElement('span');
      tag.className = 'power-tag';
      tag.textContent = '💖 Max Life +1';
      box.appendChild(tag);
    }
  }

  function updateCoinDisplays() {
    document.getElementById('menu-coins').textContent = coins;
    document.getElementById('shop-coins').textContent = coins;
    document.getElementById('hud-coins').textContent = coins + sessionCoins;
  }

  function applyEquippedPowers() {
    scoreMult = 1; speedMult = 1; bladeBonus = 0; spawnBonus = 0;
    bombReduce = 0; critChance = 0; bombShieldLeft = 0; activePowers = {};
    if (equipped['double_score']) { scoreMult = 2; activePowers['double_score'] = true; }
    if (equipped['slow_mo']) { speedMult = 0.6; activePowers['slow_mo'] = true; }
    if (equipped['big_blade']) { bladeBonus = 18; activePowers['big_blade'] = true; }
    if (equipped['fruit_rain']) { spawnBonus = 0.45; activePowers['fruit_rain'] = true; }
    if (equipped['lucky']) { bombReduce = 0.6; activePowers['lucky'] = true; }
    if (equipped['critical']) { critChance = 0.2; activePowers['critical'] = true; }
    if (equipped['bomb_shield']) { bombShieldLeft = 1; activePowers['bomb_shield'] = true; }
    if (equipped['extra_life']) { activePowers['extra_life'] = true; }
    equipped = {};
    saveData();
  }

  function updatePowerHUD() {
    const el = document.getElementById('power-hud');
    const names = [];
    if (scoreMult > 1) names.push('x2');
    if (speedMult < 1) names.push('🐢');
    if (bladeBonus > 0) names.push('⚔️');
    if (bombShieldLeft > 0) names.push('🛡️');
    if (critChance > 0) names.push('💥');
    if (spawnBonus > 0) names.push('🌧️');
    if (names.length) { el.style.display = 'block'; el.textContent = names.join(' '); }
    else el.style.display = 'none';
  }

  function createFruit(isBomb=false) {
    const t = isBomb ? null : FRUIT_TYPES[Math.floor(Math.random()*FRUIT_TYPES.length)];
    const fromLeft = Math.random() < 0.5;
    const x = fromLeft ? rand(-50, W*0.28) : rand(W*0.72, W+50);
    const baseSpeed = rand(9, 15) * (0.75 + difficulty*0.14) * speedMult;
    const ang = rand(-Math.PI*0.72, -Math.PI*0.28);
    return {
      x, y: H + 50,
      vx: Math.cos(ang)*baseSpeed*(fromLeft?1:-1)*rand(0.55,1.15),
      vy: -Math.abs(Math.sin(ang)*baseSpeed) - rand(5,10)*speedMult,
      radius: isBomb ? 40 : t.radius,
      type: isBomb ? 'bomb' : t.name,
      juice: isBomb ? '#ff1744' : t.juice,
      rind: isBomb ? '#222' : t.rind,
      flesh: isBomb ? '#111' : t.flesh,
      points: isBomb ? 0 : t.points,
      rotation: rand(0, Math.PI*2), rotSpeed: rand(-0.12, 0.12),
      sliced: false, halves: null, isBomb, fuse: 0
    };
  }

  function createParticles(x, y, color, count=14, speed=7) {
    for (let i=0; i<count; i++) {
      particles.push({
        x, y, vx: rand(-speed, speed), vy: rand(-speed*1.2, speed*0.3),
        life: 1, decay: rand(0.018, 0.04), color, size: rand(2.5, 7),
        shape: Math.random() < 0.3 ? 'drop' : 'circle'
      });
    }
  }
  function createSparkles(x, y, count=8) {
    for (let i=0; i<count; i++) {
      sparkles.push({ x: x+rand(-20,20), y: y+rand(-20,20), life: 1, decay: rand(0.03,0.06), size: rand(2,5) });
    }
  }
  function createBlade(pts) {
    if (pts.length < 2) return;
    blades.push({ points: pts.map(p=>({...p})), life: 1, decay: 0.07 });
  }

  function drawBackground(t) {
    const sky = ctx.createLinearGradient(0, 0, 0, H);
    sky.addColorStop(0, '#4fc3f7'); sky.addColorStop(0.35, '#81d4fa');
    sky.addColorStop(0.55, '#a5d6a7'); sky.addColorStop(0.75, '#81c784'); sky.addColorStop(1, '#558b2f');
    ctx.fillStyle = sky; ctx.fillRect(0, 0, W, H);
    const sunGrad = ctx.createRadialGradient(W*0.75, H*0.18, 0, W*0.75, H*0.18, W*0.35);
    sunGrad.addColorStop(0, 'rgba(255,248,200,0.45)'); sunGrad.addColorStop(1, 'rgba(255,236,160,0)');
    ctx.fillStyle = sunGrad; ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = 'rgba(255,255,255,0.55)';
    clouds.forEach(c => {
      const x = c.x + Math.sin(t*0.15 + c.phase)*8, y = c.y, s = c.scale;
      ctx.beginPath();
      ctx.arc(x,y,18*s,0,Math.PI*2); ctx.arc(x+22*s,y-6*s,22*s,0,Math.PI*2);
      ctx.arc(x+48*s,y,16*s,0,Math.PI*2); ctx.arc(x+28*s,y+8*s,14*s,0,Math.PI*2);
      ctx.fill();
    });
    ctx.fillStyle = 'rgba(55,90,60,0.35)';
    ctx.beginPath(); ctx.moveTo(0, H*0.52);
    ctx.quadraticCurveTo(W*0.2, H*0.38, W*0.4, H*0.48);
    ctx.quadraticCurveTo(W*0.55, H*0.55, W*0.7, H*0.42);
    ctx.quadraticCurveTo(W*0.85, H*0.35, W, H*0.48);
    ctx.lineTo(W, H); ctx.lineTo(0, H); ctx.fill();
    ctx.fillStyle = 'rgba(70,120,55,0.4)';
    ctx.beginPath(); ctx.moveTo(0, H*0.62);
    for (let x=0; x<=W; x+=30) ctx.lineTo(x, H*0.62 - 25 + Math.sin(x*0.025 + t*0.1)*12);
    ctx.lineTo(W, H); ctx.lineTo(0, H); ctx.fill();
    ctx.fillStyle = 'rgba(76,140,50,0.55)';
    ctx.beginPath(); ctx.moveTo(0, H*0.78);
    for (let x=0; x<=W; x+=25) ctx.lineTo(x, H*0.78 - 18 + Math.sin(x*0.04)*10);
    ctx.lineTo(W, H); ctx.lineTo(0, H); ctx.fill();
  }

  function drawFruit(f) {
    if (f.sliced && f.halves) { f.halves.forEach(h => drawHalf(h, f)); return; }
    ctx.save(); ctx.globalAlpha = 0.18; ctx.fillStyle = '#000';
    ctx.beginPath(); ctx.ellipse(f.x, f.y + f.radius*0.85, f.radius*0.75, f.radius*0.22, 0, 0, Math.PI*2); ctx.fill();
    ctx.restore();
    ctx.save(); ctx.translate(f.x, f.y); ctx.rotate(f.rotation);
    if (f.isBomb) drawBomb(f);
    else {
      const r = f.radius;
      if (f.type === 'watermelon') {
        const g = ctx.createRadialGradient(-r*0.25,-r*0.25,0,0,0,r);
        g.addColorStop(0,'#66bb6a'); g.addColorStop(1,'#2e7d32');
        ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.fillStyle=g; ctx.fill();
        ctx.strokeStyle='rgba(27,94,32,0.55)'; ctx.lineWidth=3.5;
        for (let i=-3;i<=3;i++) { ctx.beginPath(); ctx.ellipse(0,0,r*0.92,r*0.35,i*0.35,0,Math.PI*2); ctx.stroke(); }
      } else if (f.type === 'banana') {
        ctx.beginPath();
        ctx.moveTo(-r*0.9,-r*0.15);
        ctx.quadraticCurveTo(-r*0.3,-r*0.9,r*0.2,-r*0.7);
        ctx.quadraticCurveTo(r*0.9,-r*0.3,r*0.85,r*0.2);
        ctx.quadraticCurveTo(r*0.5,r*0.7,-r*0.2,r*0.55);
        ctx.quadraticCurveTo(-r*0.9,r*0.3,-r*0.9,-r*0.15);
        const g = ctx.createLinearGradient(-r,0,r,0);
        g.addColorStop(0,'#fbc02d'); g.addColorStop(0.5,'#ffee58'); g.addColorStop(1,'#f9a825');
        ctx.fillStyle=g; ctx.fill();
      } else if (f.type === 'strawberry') {
        ctx.beginPath();
        ctx.moveTo(0,-r);
        ctx.bezierCurveTo(r*1.1,-r*0.6,r*1.0,r*0.5,0,r);
        ctx.bezierCurveTo(-r*1.0,r*0.5,-r*1.1,-r*0.6,0,-r);
        const g = ctx.createRadialGradient(-r*0.2,-r*0.2,0,0,0,r);
        g.addColorStop(0,'#f06292'); g.addColorStop(1,'#c2185b');
        ctx.fillStyle=g; ctx.fill();
        ctx.fillStyle='#43a047';
        for (let i=-2;i<=2;i++) { ctx.beginPath(); ctx.ellipse(i*5,-r*0.85,5,7,i*0.4,0,Math.PI*2); ctx.fill(); }
      } else {
        const g = ctx.createRadialGradient(-r*0.3,-r*0.3,0,0,0,r);
        g.addColorStop(0, lighten(f.rind,40)); g.addColorStop(1, f.rind);
        ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.fillStyle=g; ctx.fill();
      }
    }
    ctx.restore();
  }

  function drawBomb(f) {
    const r = f.radius; f.fuse += 0.15;
    const g = ctx.createRadialGradient(-r*0.3,-r*0.3,0,0,0,r);
    g.addColorStop(0,'#555'); g.addColorStop(1,'#1a1a1a');
    ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.fillStyle=g; ctx.fill();
    ctx.strokeStyle='#8d6e63'; ctx.lineWidth=3;
    ctx.beginPath(); ctx.moveTo(0,-r); ctx.quadraticCurveTo(10,-r-10,6,-r-22); ctx.stroke();
    const flicker = 0.6 + Math.sin(f.fuse*8)*0.4;
    ctx.fillStyle=`rgba(255,235,59,${flicker})`;
    ctx.beginPath(); ctx.arc(6,-r-22,5,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#fff';
    ctx.beginPath(); ctx.arc(-8,-5,5,0,Math.PI*2); ctx.arc(8,-5,5,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#f44336';
    ctx.beginPath(); ctx.arc(-8,-4,2.5,0,Math.PI*2); ctx.arc(8,-4,2.5,0,Math.PI*2); ctx.fill();
  }

  function drawHalf(h, f) {
    ctx.save(); ctx.translate(h.x,h.y); ctx.rotate(h.rotation); ctx.globalAlpha=Math.max(0,h.life);
    ctx.beginPath(); ctx.arc(0,0,f.radius,h.startAngle,h.endAngle); ctx.lineTo(0,0); ctx.closePath();
    const g = ctx.createRadialGradient(0,0,0,0,0,f.radius);
    g.addColorStop(0,lighten(f.flesh,30)); g.addColorStop(1,f.flesh);
    ctx.fillStyle=g; ctx.fill();
    ctx.strokeStyle=f.juice; ctx.lineWidth=3; ctx.globalAlpha=h.life*0.7;
    ctx.beginPath(); ctx.arc(0,0,f.radius*0.92,h.startAngle,h.endAngle); ctx.stroke();
    ctx.restore();
  }

  function drawParticles() {
    particles.forEach(p => {
      ctx.globalAlpha=p.life; ctx.fillStyle=p.color;
      ctx.beginPath();
      if (p.shape==='drop') ctx.ellipse(p.x,p.y,p.size*0.5*p.life,p.size*p.life,0,0,Math.PI*2);
      else ctx.arc(p.x,p.y,p.size*p.life,0,Math.PI*2);
      ctx.fill();
    });
    sparkles.forEach(s => {
      ctx.globalAlpha=s.life; ctx.strokeStyle='#fff'; ctx.lineWidth=1.5;
      const sz=s.size*s.life;
      ctx.beginPath(); ctx.moveTo(s.x-sz,s.y); ctx.lineTo(s.x+sz,s.y);
      ctx.moveTo(s.x,s.y-sz); ctx.lineTo(s.x,s.y+sz); ctx.stroke();
    });
    ctx.globalAlpha=1;
  }

  function drawBlades() {
    blades.forEach(b => {
      if (b.points.length<2) return;
      ctx.save(); ctx.globalAlpha=b.life; ctx.lineCap='round'; ctx.lineJoin='round';
      ctx.strokeStyle='rgba(255,100,0,0.4)'; ctx.lineWidth=14; ctx.shadowColor='#ff6b00'; ctx.shadowBlur=20;
      ctx.beginPath(); ctx.moveTo(b.points[0].x,b.points[0].y);
      for (let i=1;i<b.points.length;i++) ctx.lineTo(b.points[i].x,b.points[i].y);
      ctx.stroke();
      ctx.strokeStyle='rgba(255,234,0,0.7)'; ctx.lineWidth=7; ctx.shadowColor='#ffea00'; ctx.shadowBlur=12; ctx.stroke();
      ctx.strokeStyle='#fff'; ctx.lineWidth=2.5; ctx.shadowBlur=0; ctx.stroke();
      ctx.restore();
    });
  }

  function spawnFruits(dt) {
    spawnTimer -= dt;
    if (spawnTimer <= 0) {
      let count = Math.min(1 + Math.floor(difficulty/2), 4);
      if (spawnBonus > 0) count = Math.min(count + 1, 5);
      for (let i=0; i<count; i++) {
        let bombChance = gameMode==='zen' ? 0 : (0.07 + difficulty*0.02);
        bombChance *= (1 - bombReduce);
        fruits.push(createFruit(Math.random() < bombChance));
      }
      spawnTimer = rand(0.55, 1.35) / (0.65 + difficulty*0.22) * (spawnBonus > 0 ? 0.7 : 1);
    }
  }

  function update(dt) {
    if (!isPlaying || isPaused) return;
    bgTime += dt; difficulty += dt * 0.015;
    if (gameMode === 'arcade') {
      timer -= dt;
      document.getElementById('timer').textContent = Math.max(0, Math.ceil(timer));
      if (timer <= 0) { endGame(); return; }
    }
    comboTimer -= dt; if (comboTimer <= 0) combo = 0;
    spawnFruits(dt);
    for (let i = fruits.length-1; i >= 0; i--) {
      const f = fruits[i];
      if (f.sliced && f.halves) {
        f.halves.forEach(h => {
          h.x += h.vx*dt*60; h.y += h.vy*dt*60; h.vy += 0.42*dt*60;
          h.rotation += h.rotSpeed; h.life -= dt*1.4;
        });
        if (f.halves[0].life <= 0) fruits.splice(i, 1);
        continue;
      }
      f.x += f.vx*dt*60; f.y += f.vy*dt*60; f.vy += 0.26*dt*60*speedMult; f.rotation += f.rotSpeed;
      if (f.y > H+70 && !f.sliced) {
        if (!f.isBomb && gameMode !== 'zen') {
          lives--; updateHUD(); playMiss();
          if (lives <= 0) { endGame(); return; }
        }
        fruits.splice(i, 1);
      }
    }
    for (let i=particles.length-1;i>=0;i--) {
      const p=particles[i]; p.x+=p.vx; p.y+=p.vy; p.vy+=0.22; p.life-=p.decay;
      if (p.life<=0) particles.splice(i,1);
    }
    for (let i=sparkles.length-1;i>=0;i--) {
      sparkles[i].life-=sparkles[i].decay;
      if (sparkles[i].life<=0) sparkles.splice(i,1);
    }
    for (let i=blades.length-1;i>=0;i--) {
      blades[i].life-=blades[i].decay;
      if (blades[i].life<=0) blades.splice(i,1);
    }
  }

  function trySlice(x1,y1,x2,y2) {
    const hitR = 10 + bladeBonus;
    for (let i = fruits.length-1; i >= 0; i--) {
      const f = fruits[i];
      if (f.sliced) continue;
      if (lineCircle(x1,y1,x2,y2, f.x,f.y, f.radius+hitR)) {
        f.sliced = true;
        if (f.isBomb) {
          createParticles(f.x,f.y,'#ff1744',30,10);
          createParticles(f.x,f.y,'#ffeb3b',18,8);
          createSparkles(f.x,f.y,12); playBomb();
          if (navigator.vibrate) navigator.vibrate(200);
          if (bombShieldLeft > 0) {
            bombShieldLeft--; createSparkles(f.x,f.y,15); updatePowerHUD(); fruits.splice(i,1);
          } else if (gameMode !== 'zen') {
            lives=0; updateHUD(); endGame(); return;
          } else fruits.splice(i,1);
        } else {
          const ang = Math.atan2(y2-y1,x2-x1);
          f.halves = [
            {x:f.x,y:f.y,vx:Math.cos(ang+0.9)*5,vy:Math.sin(ang+0.9)*3.5-2.5,rotation:f.rotation,rotSpeed:-0.25,life:1,startAngle:ang,endAngle:ang+Math.PI},
            {x:f.x,y:f.y,vx:Math.cos(ang-0.9)*5,vy:Math.sin(ang-0.9)*3.5-2.5,rotation:f.rotation,rotSpeed:0.25,life:1,startAngle:ang+Math.PI,endAngle:ang+Math.PI*2}
          ];
          createParticles(f.x,f.y,f.juice,16,8); createSparkles(f.x,f.y,6);
          playSlice(); if (navigator.vibrate) navigator.vibrate(25);
          combo++; comboTimer=1.25;
          let pts = f.points;
          if (critChance>0 && Math.random()<critChance) { pts*=3; showCombo(f.x,f.y-30,'CRIT x3!'); }
          if (combo>=3) { pts=Math.floor(pts*(1+combo*0.35)); showCombo(f.x,f.y,combo+'x'); playCombo(); }
          pts=Math.floor(pts*scoreMult); score+=pts;
          sessionCoins+=Math.max(1,Math.floor(f.points/3));
          updateHUD(); updateCoinDisplays();
        }
      }
    }
  }

  function showCombo(x,y,text) {
    const el=document.createElement('div'); el.className='combo-text';
    el.textContent=(typeof text==='number'?text+'x COMBO!':text);
    el.style.left=Math.max(10,Math.min(W-100,x-50))+'px';
    el.style.top=Math.max(10,y-50)+'px';
    document.getElementById('game-container').appendChild(el);
    setTimeout(()=>el.remove(),850);
  }

  function updateHUD() {
    document.getElementById('score').textContent=score;
    document.getElementById('lives').textContent=lives;
    document.getElementById('hud-coins').textContent=coins+sessionCoins;
  }

  function render() {
    ctx.clearRect(0,0,W,H);
    drawBackground(bgTime);
    fruits.forEach(drawFruit);
    drawParticles(); drawBlades();
    if (isSlicing && slicePoints.length>1) {
      ctx.save(); ctx.lineCap='round'; ctx.lineJoin='round';
      ctx.strokeStyle='rgba(255,120,0,0.5)'; ctx.lineWidth=12; ctx.shadowColor='#ff6b00'; ctx.shadowBlur=18;
      ctx.beginPath(); ctx.moveTo(slicePoints[0].x,slicePoints[0].y);
      for (let i=1;i<slicePoints.length;i++) ctx.lineTo(slicePoints[i].x,slicePoints[i].y);
      ctx.stroke();
      ctx.strokeStyle='#fff'; ctx.lineWidth=3; ctx.shadowBlur=0; ctx.stroke();
      ctx.restore();
    }
  }

  function loop(ts) {
    const dt=Math.min((ts-lastTime)/1000,0.05); lastTime=ts;
    update(dt); render();
    animId=requestAnimationFrame(loop);
  }

  function getPos(e) {
    const rect=canvas.getBoundingClientRect();
    const sx=canvas.width/rect.width, sy=canvas.height/rect.height;
    const cx=(e.touches&&e.touches.length)?e.touches[0].clientX:e.clientX;
    const cy=(e.touches&&e.touches.length)?e.touches[0].clientY:e.clientY;
    return {x:(cx-rect.left)*sx, y:(cy-rect.top)*sy};
  }
  function onStart(e) {
    if (!isPlaying||isPaused) return;
    e.preventDefault(); initAudio(); isSlicing=true; slicePoints=[getPos(e)];
  }
  function onMove(e) {
    if (!isSlicing||!isPlaying||isPaused) return;
    e.preventDefault();
    const p=getPos(e), last=slicePoints[slicePoints.length-1];
    if (dist(last.x,last.y,p.x,p.y)>6) {
      slicePoints.push(p); if (slicePoints.length>24) slicePoints.shift();
      trySlice(last.x,last.y,p.x,p.y);
    }
  }
  function onEnd(e) {
    if (!isSlicing) return;
    e.preventDefault();
    if (slicePoints.length>1) createBlade(slicePoints);
    isSlicing=false; slicePoints=[];
  }

  function showScreen(id) {
    ['start-screen','shop-screen','settings-screen','pause-screen','gameover-screen'].forEach(s=>{
      document.getElementById(s).classList.toggle('hidden', s!==id);
    });
    document.getElementById('hud').style.display=(id===null)?'flex':'none';
    document.getElementById('sound-btn').style.display=(id===null)?'block':'none';
  }

  function startGame() {
    initAudio();
    if (audioCtx&&audioCtx.state==='suspended') audioCtx.resume();
    gameMode=document.querySelector('input[name="mode"]:checked').value;
    score=0; sessionCoins=0; difficulty=1; timer=60; combo=0;
    fruits=[]; particles=[]; blades=[]; sparkles=[];
    isPlaying=true; isPaused=false; spawnTimer=0.4;
    applyEquippedPowers();
    let baseLives=gameMode==='zen'?99:3;
    if (ownedPerm['max_life']) baseLives+=1;
    if (activePowers['extra_life']) baseLives+=1;
    lives=baseLives;
    document.getElementById('lives-box').style.display=gameMode==='zen'?'none':'block';
    document.getElementById('timer-box').style.display=gameMode==='arcade'?'block':'none';
    updateHUD(); updatePowerHUD(); updateActivePreview();
    showScreen(null); lastTime=performance.now();
  }

  function endGame() {
    isPlaying=false;
    coins+=sessionCoins;
    if (score>highScore) highScore=score;
    saveData();
    document.getElementById('final-score').textContent=score;
    document.getElementById('final-high').textContent=highScore;
    document.getElementById('high-score').textContent=highScore;
    document.getElementById('earned-coins').textContent=sessionCoins;
    updateCoinDisplays();
    showScreen('gameover-screen');
  }

  function pauseGame() { if (!isPlaying) return; isPaused=true; showScreen('pause-screen'); }
  function resumeGame() { isPaused=false; showScreen(null); lastTime=performance.now(); }

  function resize() {
    const container=document.getElementById('game-container');
    const rect=container.getBoundingClientRect();
    let w=Math.floor(rect.width*(window.devicePixelRatio||1));
    let h=Math.floor(rect.height*(window.devicePixelRatio||1));
    const maxD=960;
    if (w>maxD||h>maxD) { const s=maxD/Math.max(w,h); w=Math.floor(w*s); h=Math.floor(h*s); }
    W=w; H=h; canvas.width=W; canvas.height=H;
    canvas.style.width=rect.width+'px'; canvas.style.height=rect.height+'px';
  }

  function init() {
    canvas=document.getElementById('gameCanvas');
    ctx=canvas.getContext('2d');
    loadData(); updateCoinDisplays();
    document.getElementById('high-score').textContent=highScore;
    updateActivePreview();
    for (let i=0;i<5;i++) clouds.push({x:rand(0,400),y:rand(30,120),scale:rand(0.6,1.3),phase:rand(0,10)});
    resize();
    window.addEventListener('resize',resize);
    window.addEventListener('orientationchange',()=>setTimeout(resize,200));
    canvas.addEventListener('mousedown',onStart);
    canvas.addEventListener('mousemove',onMove);
    canvas.addEventListener('mouseup',onEnd);
    canvas.addEventListener('mouseleave',onEnd);
    canvas.addEventListener('touchstart',onStart,{passive:false});
    canvas.addEventListener('touchmove',onMove,{passive:false});
    canvas.addEventListener('touchend',onEnd,{passive:false});
    canvas.addEventListener('touchcancel',onEnd,{passive:false});
    document.getElementById('play-btn').onclick=startGame;
    document.getElementById('shop-btn').onclick=()=>{renderShop();showScreen('shop-screen');};
    document.getElementById('shop-back-btn').onclick=()=>showScreen('start-screen');
    document.getElementById('settings-btn').onclick=()=>showScreen('settings-screen');
    document.getElementById('back-btn').onclick=()=>showScreen('start-screen');
    document.getElementById('pause-btn').onclick=pauseGame;
    document.getElementById('resume-btn').onclick=resumeGame;
    document.getElementById('restart-btn').onclick=()=>{isPaused=false;startGame();};
    document.getElementById('menu-btn').onclick=()=>{isPlaying=false;isPaused=false;showScreen('start-screen');};
    document.getElementById('again-btn').onclick=startGame;
    document.getElementById('go-shop-btn').onclick=()=>{renderShop();showScreen('shop-screen');};
    document.getElementById('menu2-btn').onclick=()=>showScreen('start-screen');
    const soundBtn=document.getElementById('sound-btn');
    const soundSettings=document.getElementById('sound-toggle-settings');
    function toggleSound() {
      soundOn=!soundOn;
      soundBtn.textContent=soundOn?'🔊':'🔇';
      soundSettings.textContent=soundOn?'ON':'OFF';
    }
    soundBtn.onclick=toggleSound; soundSettings.onclick=toggleSound;
    document.getElementById('volume-slider').oninput=e=>{volume=e.target.value/100;};
    document.body.addEventListener('touchmove',e=>{
      if (e.target===canvas||e.target.closest('#game-container')) e.preventDefault();
    },{passive:false});
    lastTime=performance.now();
    animId=requestAnimationFrame(loop);
  }

  if (document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
  else init();
})();
</script>
</body>
</html>
"""

html(GAME_HTML, height=820, scrolling=False)
