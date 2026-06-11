<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Juego Raro - Geometry Dash</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #1a1a2e;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    font-family: monospace;
    overflow: hidden;
  }
  .game-container {
    position: relative;
    background: #0f0f23;
    border: 3px solid #e94560;
    border-radius: 8px;
    box-shadow: 0 0 40px rgba(233,69,96,0.3);
  }
  canvas {
    display: block;
  }
  #ui {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    padding: 10px 16px;
    color: #fff;
    font-size: 18px;
    font-weight: bold;
    pointer-events: none;
  }
  #score { color: #0ff; }
  #best { color: #ff0; }
  #message {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #fff;
    font-size: 28px;
    font-weight: bold;
    text-align: center;
    pointer-events: none;
    text-shadow: 0 0 20px rgba(233,69,96,0.8);
    transition: opacity 0.2s;
  }
  #message small {
    display: block;
    font-size: 14px;
    color: #aaa;
    margin-top: 12px;
    font-weight: normal;
  }
</style>
</head>
<body>
<div class="game-container">
  <canvas id="game"></canvas>
  <div id="ui">
    <span id="score">0</span>
    <span id="best">MEJOR: 0</span>
  </div>
  <div id="message">PRESIONA <span style="color:#e94560">ESPACIO</span><br><small>para empezar</small></div>
</div>
<script>
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const bestEl = document.getElementById('best');
const msgEl = document.getElementById('message');

const W = 800, H = 400;
canvas.width = W;
canvas.height = H;

// game state
const GRAVITY = 0.55;
const JUMP = -8;
const GROUND_Y = H - 60;
const PLAYER_SIZE = 28;
const SPIKE_W = 22;
const SPIKE_H = 28;
const MIN_GAP = 180;
const MAX_GAP = 280;
const SPEED_INIT = 4.5;
const SPIKE_INTERVAL = 80;

let player, spikes, score, best, speed, frame, gameOver, started;
let spikeTimer;

function reset() {
  player = { x: 100, y: GROUND_Y - PLAYER_SIZE, vy: 0, size: PLAYER_SIZE };
  spikes = [];
  score = 0;
  speed = SPEED_INIT;
  frame = 0;
  gameOver = false;
  spikeTimer = 0;
  scoreEl.textContent = '0';
}

function jump() {
  if (gameOver) {
    if (score > best) {
      best = score;
      bestEl.textContent = 'MEJOR: ' + best;
    }
    reset();
    started = false;
    msgEl.style.opacity = '1';
    msgEl.innerHTML = 'PRESIONA <span style="color:#e94560">ESPACIO</span><br><small>para empezar</small>';
    return;
  }
  if (!started) {
    started = true;
    msgEl.style.opacity = '0';
  }
  if (player.y >= GROUND_Y - PLAYER_SIZE - 1) {
    player.vy = JUMP;
  }
}

function spawnSpike() {
  const groundH = 2;
  spikes.push({
    x: W,
    w: SPIKE_W,
    h: SPIKE_H,
    groundH: groundH,
    passed: false
  });
}

function update() {
  if (!started || gameOver) return;
  frame++;

  // gravity
  player.vy += GRAVITY;
  player.y += player.vy;
  if (player.y > GROUND_Y - PLAYER_SIZE) {
    player.y = GROUND_Y - PLAYER_SIZE;
    player.vy = 0;
  }

  // speed up
  speed = SPEED_INIT + Math.floor(score / 15) * 0.3;

  // spawn spikes
  spikeTimer++;
  if (spikeTimer >= SPIKE_INTERVAL) {
    const offset = Math.min(20 + Math.floor(score / 10) * 3, 60);
    const interval = Math.max(MIN_GAP - offset, 140);
    spikeTimer = -Math.floor(Math.random() * interval * 0.6);
    spawnSpike();
  }

  // move spikes
  for (let i = spikes.length - 1; i >= 0; i--) {
    const s = spikes[i];
    s.x -= speed;
    if (!s.passed && s.x + s.w < player.x) {
      s.passed = true;
      score++;
      scoreEl.textContent = score;
    }
    if (s.x + s.w < 0) {
      spikes.splice(i, 1);
    }
  }

  // collision
  for (const s of spikes) {
    if (rectCollide(
      player.x, player.y, PLAYER_SIZE, PLAYER_SIZE,
      s.x, GROUND_Y - s.h, s.w, s.h
    )) {
      gameOver = true;
      msgEl.style.opacity = '1';
      msgEl.innerHTML = '💀 GAME OVER<br><small>Presiona ESPACIO para reintentar</small>';
      if (score > best) {
        best = score;
        bestEl.textContent = 'MEJOR: ' + best;
      }
      return;
    }
  }
}

function rectCollide(x1,y1,w1,h1,x2,y2,w2,h2) {
  return x1 < x2 + w2 && x1 + w1 > x2 && y1 < y2 + h2 && y1 + h1 > y2;
}

function draw() {
  ctx.clearRect(0, 0, W, H);

  // background
  const grad = ctx.createLinearGradient(0, 0, 0, H);
  grad.addColorStop(0, '#0f0f23');
  grad.addColorStop(1, '#1a1a3e');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, W, H);

  // stars
  ctx.fillStyle = 'rgba(255,255,255,0.4)';
  for (let i = 0; i < 50; i++) {
    const sx = (i * 137 + i * i * 7) % W;
    const sy = (i * 89 + i * i * 3) % (GROUND_Y - 40);
    const size = 1 + (i % 3);
    ctx.fillRect(sx, sy, size, size);
  }

  // ground
  ctx.fillStyle = '#e94560';
  ctx.fillRect(0, GROUND_Y, W, 2);
  ctx.fillStyle = '#2d2d5e';
  ctx.fillRect(0, GROUND_Y + 2, W, H - GROUND_Y);

  // spikes
  for (const s of spikes) {
    ctx.fillStyle = '#e94560';
    ctx.beginPath();
    const cx = s.x + s.w / 2;
    const cy = GROUND_Y - s.h;
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx - s.w / 2, cy + s.h);
    ctx.lineTo(cx + s.w / 2, cy + s.h);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = '#ff6b81';
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  // player
  const p = player;
  ctx.fillStyle = gameOver ? '#ff4444' : '#0ff';
  ctx.shadowColor = '#0ff';
  ctx.shadowBlur = gameOver ? 5 : 15;
  const r = 4;
  ctx.beginPath();
  ctx.moveTo(p.x + r, p.y);
  ctx.lineTo(p.x + p.size - r, p.y);
  ctx.quadraticCurveTo(p.x + p.size, p.y, p.x + p.size, p.y + r);
  ctx.lineTo(p.x + p.size, p.y + p.size - r);
  ctx.quadraticCurveTo(p.x + p.size, p.y + p.size, p.x + p.size - r, p.y + p.size);
  ctx.lineTo(p.x + r, p.y + p.size);
  ctx.quadraticCurveTo(p.x, p.y + p.size, p.x, p.y + p.size - r);
  ctx.lineTo(p.x, p.y + r);
  ctx.quadraticCurveTo(p.x, p.y, p.x + r, p.y);
  ctx.closePath();
  ctx.fill();
  ctx.shadowBlur = 0;

  // eye
  ctx.fillStyle = '#fff';
  ctx.beginPath();
  ctx.arc(p.x + p.size - 10, p.y + 10, 5, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#111';
  ctx.beginPath();
  ctx.arc(p.x + p.size - 9, p.y + 10, 2.5, 0, Math.PI * 2);
  ctx.fill();
}

function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}

document.addEventListener('keydown', e => {
  if (e.key === ' ' || e.key === 'Space') {
    e.preventDefault();
    jump();
  }
});
canvas.addEventListener('click', jump);
canvas.addEventListener('touchstart', e => { e.preventDefault(); jump(); });

reset();
best = parseInt(localStorage.getItem('gdBest') || '0');
bestEl.textContent = 'MEJOR: ' + best;
loop();
</script>
</body>
</html>
