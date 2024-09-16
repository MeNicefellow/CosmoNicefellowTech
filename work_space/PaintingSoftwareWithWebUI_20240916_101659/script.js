const canvas = document.getElementById('paintingCanvas');
const ctx = canvas.getContext('2d');
const brushColorInput = document.getElementById('brushColor');
const brushSizeInput = document.getElementById('brushSize');
const eraserButton = document.getElementById('eraserButton');
let isDrawing = false;
let brushColor = '#000000';
let brushSize = 5;
let isEraserActive = false;

canvas.width = window.innerWidth - 50;
canvas.height = window.innerHeight - 200;

function startDrawing(event) {
    isDrawing = true;
    draw(event);
}

function endDrawing() {
    isDrawing = false;
    ctx.beginPath();
}

function draw(event) {
    if (!isDrawing) return;
    ctx.lineWidth = isEraserActive ? 50 : brushSize;
    ctx.lineCap = 'round';
    ctx.strokeStyle = isEraserActive ? '#FFFFFF' : brushColor;
    ctx.lineTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
}

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', endDrawing);
canvas.addEventListener('mousemove', draw);

brushColorInput.addEventListener('input', (event) => {
    brushColor = event.target.value;
});

brushSizeInput.addEventListener('input', (event) => {
    brushSize = event.target.value;
});

eraserButton.addEventListener('click', () => {
    isEraserActive = !isEraserActive;
    eraserButton.innerText = isEraserActive ? 'Brush' : 'Eraser';
});