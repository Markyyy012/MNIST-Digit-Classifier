const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const BRUSH_SIZE = 18;

ctx.fillStyle = "#000";
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.strokeStyle = "#fff";
ctx.lineWidth = BRUSH_SIZE;
ctx.lineCap = "round";
ctx.lineJoin = "round";

let drawing = false;

function getPos(e) {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  return {
    x: (e.clientX - rect.left) * scaleX,
    y: (e.clientY - rect.top) * scaleY,
  };
}

function startDraw(e) {
  drawing = true;
  const pos = getPos(e);
  ctx.beginPath();
  ctx.moveTo(pos.x, pos.y);
}

function draw(e) {
  if (!drawing) return;
  const pos = getPos(e);
  ctx.lineTo(pos.x, pos.y);
  ctx.stroke();
}

function endDraw() {
  drawing = false;
}

canvas.addEventListener("mousedown", startDraw);
canvas.addEventListener("mousemove", draw);
window.addEventListener("mouseup", endDraw);

canvas.addEventListener("touchstart", (e) => {
  e.preventDefault();
  const touch = e.touches[0];
  startDraw(touch);
});
canvas.addEventListener("touchmove", (e) => {
  e.preventDefault();
  const touch = e.touches[0];
  draw(touch);
});
canvas.addEventListener("touchend", (e) => {
  e.preventDefault();
  endDraw();
});

function clearCanvas() {
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  resetResults();
}

function resetResults() {
  document.getElementById("prediction").textContent = "\u2013";
  document.getElementById("confidence").textContent = "\u2013";
  document.querySelectorAll(".bar-row").forEach((row) => {
    row.classList.remove("winner");
    row.querySelector(".bar-fill").style.width = "0%";
  });
  const thumb = document.getElementById("thumbnail");
  const tctx = thumb.getContext("2d");
  tctx.fillStyle = "#000";
  tctx.fillRect(0, 0, thumb.width, thumb.height);
  hideError();
}

function showError(msg) {
  const el = document.getElementById("error");
  el.textContent = msg;
  el.hidden = false;
}

function hideError() {
  document.getElementById("error").hidden = true;
}

function renderResults(data) {
  document.getElementById("prediction").textContent = data.prediction;
  document.getElementById("confidence").textContent =
    data.confidence.toFixed(2) + "%";

  data.probabilities.forEach((prob, digit) => {
    const row = document.querySelector(`.bar-row[data-digit="${digit}"]`);
    row.querySelector(".bar-fill").style.width = (prob * 100).toFixed(1) + "%";
    row.classList.toggle("winner", digit === data.prediction);
  });

  renderThumbnail(data.processed);
}

function renderThumbnail(processed) {
  const thumb = document.getElementById("thumbnail");
  const tctx = thumb.getContext("2d");
  const scale = thumb.width / 28;
  for (let y = 0; y < 28; y++) {
    for (let x = 0; x < 28; x++) {
      const v = Math.round(processed[y][x] * 255);
      tctx.fillStyle = `rgb(${v},${v},${v})`;
      tctx.fillRect(x * scale, y * scale, scale, scale);
    }
  }
}

async function predict() {
  hideError();

  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  let hasInk = false;
  for (let i = 0; i < imageData.data.length; i += 4) {
    if (imageData.data[i] > 0) {
      hasInk = true;
      break;
    }
  }
  if (!hasInk) {
    showError("Canvas is empty. Draw a digit first.");
    return;
  }

  const base64 = canvas.toDataURL("image/png").split(",")[1];

  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: base64 }),
    });

    const data = await res.json();

    if (!res.ok) {
      showError(data.error || "Prediction failed.");
      return;
    }

    renderResults(data);
  } catch (err) {
    showError("Network error: could not reach the server.");
  }
}

document.getElementById("predict-btn").addEventListener("click", predict);
document.getElementById("clear-btn").addEventListener("click", clearCanvas);

resetResults();
