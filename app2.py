import threading
import subprocess
import time
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Tiempo Pro</title>

<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&display=swap" rel="stylesheet">

<style>

*, *::before, *::after{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

:root{

    --bg:#0a0a0a;
    --surface:#141414;
    --border:#2a2a2a;

    --accent:#ffffff;
    --accent-dim:rgba(255,255,255,.08);
    --accent-glow:rgba(255,255,255,.18);
    --accent-b:rgba(255,255,255,.25);

    --blue:#e0e0e0;
    --blue-dim:rgba(224,224,224,.08);
    --blue-glow:rgba(224,224,224,.15);
    --blue-b:rgba(224,224,224,.25);

    --orange:#b0b0b0;
    --orange-dim:rgba(176,176,176,.08);
    --orange-b:rgba(176,176,176,.25);

    --red:#707070;
    --red-dim:rgba(112,112,112,.1);
    --red-b:rgba(112,112,112,.3);

    --text:#f5f5f5;
    --muted:#7a7a7a;
}

html{
    scroll-behavior:smooth;
}

body{

    font-family:'DM Mono', monospace;

    background:var(--bg);
    color:var(--text);

    min-height:100vh;

    display:flex;
    flex-direction:column;
    align-items:center;

    padding:20px 14px 34px;

    gap:18px;

    background-image:
        radial-gradient(ellipse at 10% 20%, rgba(255,255,255,.03) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 70%, rgba(255,255,255,.03) 0%, transparent 50%);
}

.page-title{

    font-family:'Syne', sans-serif;

    font-size:11px;
    font-weight:700;

    letter-spacing:.3em;
    text-transform:uppercase;

    color:var(--muted);

    width:100%;
    max-width:1080px;

    text-align:center;

    padding-bottom:6px;

    border-bottom:1px solid var(--border);
}

/* ==================================================
   GRID
================================================== */

.columns{

    width:100%;
    max-width:1080px;

    display:grid;

    grid-template-columns:
        repeat(auto-fit, minmax(420px, 1fr));

    gap:18px;
}

@media (max-width:920px){

    .columns{
        grid-template-columns:1fr;
    }
}

/* ==================================================
   CARD
================================================== */

.card{

    width:100%;
    min-width:0;

    background:var(--surface);

    border:1px solid var(--border);

    border-radius:20px;

    padding:26px 22px;

    display:flex;
    flex-direction:column;

    box-shadow:
        0 0 0 1px rgba(255,255,255,.025),
        0 8px 50px rgba(0,0,0,.5),
        inset 0 1px 0 rgba(255,255,255,.04);

    animation:up .45s cubic-bezier(.22,.68,0,1.15) both;
}

.card:nth-child(2){
    animation-delay:.07s;
}

@keyframes up{

    from{
        opacity:0;
        transform:translateY(16px) scale(.98);
    }

    to{
        opacity:1;
        transform:translateY(0) scale(1);
    }
}

.card-header{
    text-align:center;
    margin-bottom:22px;
}

.badge{

    display:inline-flex;
    align-items:center;

    gap:5px;

    padding:4px 12px;

    border-radius:999px;

    margin-bottom:10px;

    font-size:9px;

    letter-spacing:.22em;
    text-transform:uppercase;
}

.badge.green{

    color:var(--accent);
    background:var(--accent-dim);

    border:1px solid var(--accent-b);
}

.badge.blue{

    color:var(--blue);
    background:var(--blue-dim);

    border:1px solid var(--blue-b);
}

.card-header h2{

    font-family:'Syne', sans-serif;

    font-size:clamp(18px, 1.8vw, 24px);

    font-weight:700;

    letter-spacing:0px;
}

.lbl{

    display:block;

    font-size:9px;

    letter-spacing:.18em;
    text-transform:uppercase;

    color:var(--muted);

    margin-bottom:8px;
}

/* ==================================================
   INPUTS
================================================== */

.time-row,
.cd-input-row{

    display:grid;

    grid-template-columns:1fr 1fr 1fr;

    gap:8px;

    margin-bottom:16px;
}

.field{

    display:flex;
    flex-direction:column;

    gap:4px;
}

.field span{

    font-size:9px;

    letter-spacing:.1em;
    text-transform:uppercase;

    color:var(--muted);

    text-align:center;
}

input[type="number"]{

    width:100%;

    padding:10px 4px;

    background:var(--bg);

    border:1px solid var(--border);

    border-radius:10px;

    color:var(--text);

    font-family:'DM Mono', monospace;

    font-size:clamp(16px, 1.6vw, 20px);

    text-align:center;

    transition:.18s;

    -moz-appearance:textfield;
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button{
    -webkit-appearance:none;
}

input[type="number"]:focus{

    outline:none;

    border-color:var(--accent);

    box-shadow:0 0 0 3px rgba(255,255,255,.08);
}

/* ==================================================
   DIVIDER
================================================== */

.hdiv{

    display:flex;
    align-items:center;

    gap:8px;

    margin:4px 0 16px;
}

.hdiv::before,
.hdiv::after{

    content:'';

    flex:1;

    height:1px;

    background:var(--border);
}

.hdiv span{
    color:var(--muted);
}

/* ==================================================
   BUTTONS
================================================== */

.op-row,
.crono-tabs{

    display:grid;

    grid-template-columns:1fr 1fr;

    gap:8px;

    margin-bottom:16px;
}

.crono-btns{

    display:grid;

    grid-template-columns:1fr 1fr 1fr;

    gap:8px;

    margin-bottom:14px;
}

.op-btn,
.tab-btn,
.crono-btn{

    min-height:44px;

    border-radius:10px;

    border:1px solid var(--border);

    background:var(--bg);

    color:var(--muted);

    cursor:pointer;

    transition:.18s;

    font-family:'Syne', sans-serif;

    font-size:11px;

    font-weight:700;

    letter-spacing:.05em;
    text-transform:uppercase;
}

.op-btn:hover,
.op-btn.active{

    border-color:var(--accent-b);

    color:var(--accent);

    background:var(--accent-dim);
}

.tab-btn.active{

    border-color:var(--blue-b);

    color:var(--blue);

    background:var(--blue-dim);
}

.btn-primary{

    width:100%;

    min-height:48px;

    margin-top:auto;

    border:none;

    border-radius:12px;

    background:var(--accent);

    color:#000;

    cursor:pointer;

    font-family:'Syne', sans-serif;

    font-size:12px;

    font-weight:800;

    letter-spacing:.12em;
    text-transform:uppercase;

    box-shadow:0 4px 22px var(--accent-glow);

    transition:.18s;
}

.btn-primary:hover{
    opacity:.9;
}

/* ==================================================
   RESULT
================================================== */

.result-box{

    margin-top:14px;

    padding:16px 12px;

    border-radius:12px;

    text-align:center;

    animation:up .3s ease both;
}

.result-box.ok{

    background:var(--accent-dim);

    border:1px solid var(--accent-b);
}

.rlbl{

    font-size:9px;

    letter-spacing:.18em;
    text-transform:uppercase;

    color:var(--muted);

    margin-bottom:5px;
}

.rval{

    font-family:'DM Mono', monospace;

    font-size:clamp(28px, 3.5vw, 40px);

    font-weight:500;

    color:var(--accent);

    letter-spacing:1px;

    line-height:1;
}

/* ==================================================
   CRONO
================================================== */

.crono-panel{
    display:none;
    flex-direction:column;
    flex:1;
}

.crono-panel.visible{
    display:flex;
}

.crono-face{

    text-align:center;

    margin-bottom:20px;
}

.crono-ring{

    display:inline-flex;

    flex-direction:column;

    align-items:center;
    justify-content:center;

    width:min(44vw, 200px);
    height:min(44vw, 200px);

    min-width:170px;
    min-height:170px;

    border-radius:50%;

    border:2px solid var(--border);

    background:var(--bg);

    box-shadow:
        0 0 0 5px var(--surface),
        0 0 0 6px var(--border),
        inset 0 0 30px rgba(0,0,0,.4);

    transition:.35s;
}

.crono-ring.running{

    border-color:var(--blue-b);

    box-shadow:
        0 0 0 5px var(--surface),
        0 0 0 6px var(--blue-b),
        0 0 28px var(--blue-glow),
        inset 0 0 30px rgba(0,0,0,.4);
}

.crono-ring.countdown-run{

    border-color:var(--orange-b);

    box-shadow:
        0 0 0 5px var(--surface),
        0 0 0 6px var(--orange-b),
        0 0 28px rgba(176,176,176,.15),
        inset 0 0 30px rgba(0,0,0,.4);
}

.crono-ring.countdown-done{

    border-color:var(--red-b);

    box-shadow:
        0 0 0 5px var(--surface),
        0 0 0 6px var(--red-b),
        0 0 32px rgba(112,112,112,.3),
        inset 0 0 30px rgba(0,0,0,.4);
}

.crono-hms{

    font-family:'DM Mono', monospace;

    font-size:clamp(24px, 2.8vw, 34px);

    font-weight:500;

    letter-spacing:0px;

    line-height:1;

    color:var(--blue);
}

.crono-ring.running .crono-hms{
    color:var(--accent);
}

.crono-ring.countdown-run .crono-hms{
    color:var(--orange);
}

.crono-ring.countdown-done .crono-hms{
    color:var(--red);
}

.crono-mil{

    margin-top:4px;

    font-size:13px;

    color:var(--muted);

    letter-spacing:2px;
}

.crono-status{

    margin-top:10px;

    font-size:9px;

    letter-spacing:.2em;
    text-transform:uppercase;

    color:var(--muted);
}

/* buttons */

.cbtn-start-sw{

    color:var(--blue);

    background:var(--blue-dim);

    border-color:var(--blue-b);

    box-shadow:0 3px 16px var(--blue-glow);
}

.cbtn-start-sw.paused{

    color:var(--accent);

    background:var(--accent-dim);

    border-color:var(--accent-b);
}

.cbtn-start-sw.running-s{

    color:var(--red);

    background:var(--red-dim);

    border-color:var(--red-b);
}

.cbtn-start-cd{

    color:var(--orange);

    background:var(--orange-dim);

    border-color:var(--orange-b);
}

.cbtn-start-cd.running-c{

    color:var(--red);

    background:var(--red-dim);

    border-color:var(--red-b);
}

#btn-lap:hover{

    border-color:var(--accent-b);

    color:var(--accent);

    background:var(--accent-dim);
}

#btn-reset-sw:hover,
#btn-reset-cd:hover{

    border-color:var(--red-b);

    color:var(--red);

    background:var(--red-dim);
}

/* laps */

.laps-list{

    max-height:150px;

    overflow-y:auto;

    display:flex;
    flex-direction:column;

    gap:5px;
}

.lap-row{

    display:flex;
    justify-content:space-between;
    align-items:center;

    padding:7px 12px;

    background:var(--bg);

    border:1px solid var(--border);

    border-radius:9px;

    font-size:12px;
}

.lap-row .ln{

    color:var(--muted);

    font-size:9px;

    letter-spacing:.1em;
}

.lap-row .lt{

    color:var(--text);

    font-weight:500;

    letter-spacing:1px;
}

.lap-row.best{
    border-color:var(--accent-b);
}

.lap-row.best .lt{
    color:var(--accent);
}

.lap-row.worst{
    border-color:var(--red-b);
}

.lap-row.worst .lt{
    color:var(--red);
}

/* ==================================================
   EXIT
================================================== */

.exit-btn{

    width:100%;
    max-width:1080px;

    min-height:52px;

    border-radius:14px;

    border:1px solid var(--red-b);

    background:transparent;

    color:var(--red);

    cursor:pointer;

    font-family:'Syne', sans-serif;

    font-size:12px;

    font-weight:800;

    letter-spacing:.12em;
    text-transform:uppercase;

    transition:.18s;
}

.exit-btn:hover{

    background:var(--red-dim);

    box-shadow:0 4px 22px rgba(112,112,112,.18);
}

/* ==================================================
   MOBILE
================================================== */

@media (max-width:768px){

    body{
        padding:14px 10px 28px;
    }

    .card{
        padding:20px 16px;
        border-radius:18px;
    }

    .columns{
        gap:14px;
    }

    .crono-ring{

        width:min(65vw, 190px);
        height:min(65vw, 190px);
    }
}

</style>
</head>

<body>

<p class="page-title">⏱ TIEMPO PRO</p>

<div class="columns">

<!-- ==================================================
     CALCULADORA
================================================== -->

<div class="card">

    <div class="card-header">

        <div class="badge green">
            ⬤ Calculadora
        </div>

        <h2>Calculadora de Tiempo</h2>

    </div>

    <form onsubmit="return calcular(event)">

        <span class="lbl">Hora inicial</span>

        <div class="time-row">

            <div class="field">
                <span>Horas</span>
                <input type="number" id="h1" min="0" max="23" value="0" placeholder="0"
                       onblur="if(this.value=='' || isNaN(Number(this.value))) this.value='0';">
            </div>

            <div class="field">
                <span>Minutos</span>
                <input type="number" id="m1" min="0" max="59" value="0" placeholder="0"
                       onblur="if(this.value=='' || isNaN(Number(this.value))) this.value='0';">
            </div>

            <div class="field">
                <span>Segundos</span>
                <input type="number" id="s1" min="0" max="59" value="0" placeholder="0"
                       onblur="if(this.value=='' || isNaN(Number(this.value))) this.value='0';">
            </div>

        </div>

        <div class="hdiv">
            <span>⇅</span>
        </div>

        <span class="lbl">Operación</span>

        <div class="op-row">

            <button type="button"
                    class="op-btn active"
                    onclick="setOp('resta', this)">
                − Restar
            </button>

            <button type="button"
                    class="op-btn"
                    onclick="setOp('suma', this)">
                ＋ Sumar
            </button>

        </div>

        <span class="lbl" id="op-label">
            Tiempo a restar
        </span>

        <div class="time-row">

            <div class="field">
                <span>Horas</span>
                <input type="number" id="h2" min="0" value="0" placeholder="0"
                       onblur="if(this.value=='' || isNaN(Number(this.value))) this.value='0';">
            </div>

            <div class="field">
                <span>Minutos</span>
                <input type="number" id="m2" min="0" value="0" placeholder="0"
                       onblur="if(this.value=='' || isNaN(Number(this.value))) this.value='0';">
            </div>

            <div class="field">
                <span>Segundos</span>
                <input type="number" id="s2" min="0" value="0" placeholder="0"
                       onblur="if(this.value=='' || isNaN(Number(this.value))) this.value='0';">
            </div>

        </div>

        <button type="submit" class="btn-primary">
            Calcular
        </button>

    </form>

    <div id="calc-result"
         style="display:none"
         class="result-box ok">

        <div class="rlbl">Resultado</div>

        <div class="rval" id="calc-rval">
            00:00:00
        </div>

    </div>

</div>

<!-- ==================================================
     CRONOMETRO
================================================== -->

<div class="card">

    <div class="card-header">

        <div class="badge blue">
            ⬤ Cronómetro
        </div>

        <h2>Cronómetro</h2>

    </div>

    <!-- tabs -->

    <div class="crono-tabs">

        <button class="tab-btn active"
                onclick="showTab('sw', this)">
            ⏱ Cronómetro
        </button>

        <button class="tab-btn"
                onclick="showTab('cd', this)">
            ⏳ Cuenta Regresiva
        </button>

    </div>

    <!-- STOPWATCH -->

    <div class="crono-panel visible" id="panel-sw">

        <div class="crono-face">

            <div class="crono-ring" id="ring-sw">

                <div class="crono-hms" id="sw-hms">
                    00:00:00
                </div>

                <div class="crono-mil" id="sw-mil">
                    .000
                </div>

            </div>

            <div class="crono-status" id="sw-status">
                Listo
            </div>

        </div>

        <div class="crono-btns">

            <button class="crono-btn cbtn-start-sw"
                    id="btn-sw-start"
                    onclick="swToggle()">
                Iniciar
            </button>

            <button class="crono-btn"
                    id="btn-lap"
                    onclick="swLap()">
                Vuelta
            </button>

            <button class="crono-btn"
                    id="btn-reset-sw"
                    onclick="swReset()">
                Reset
            </button>

        </div>

        <div class="laps-list" id="laps"></div>

    </div>

    <!-- COUNTDOWN -->

    <div class="crono-panel" id="panel-cd">

        <div class="crono-face">

            <div class="crono-ring" id="ring-cd">

                <div class="crono-hms" id="cd-hms">
                    00:00:00
                </div>

                <div class="crono-mil" id="cd-dot">
                    ⏳
                </div>

            </div>

            <div class="crono-status" id="cd-status">
                Configura el tiempo
            </div>

        </div>

        <span class="lbl">Tiempo a contar</span>

        <div class="cd-input-row">

            <div class="field">
                <span>Horas</span>
                <input type="number" id="cd-h" value="0" placeholder="0"
                       onblur="if(this.value=='' || isNaN(Number(this.value))) this.value='0';">
            </div>

            <div class="field">
                <span>Minutos</span>
                <input type="number" id="cd-m" value="0" placeholder="0"
                       onblur="if(this.value=='' || isNaN(Number(this.value))) this.value='0';">
            </div>

            <div class="field">
                <span>Segundos</span>
                <input type="number" id="cd-s" value="0" placeholder="0"
                       onblur="if(this.value=='' || isNaN(Number(this.value))) this.value='0';">
            </div>

        </div>

        <div class="crono-btns">

            <button class="crono-btn cbtn-start-cd"
                    id="btn-cd-start"
                    onclick="cdToggle()">
                Iniciar
            </button>

            <button class="crono-btn"
                    style="opacity:.35;cursor:default;">
                —
            </button>

            <button class="crono-btn"
                    id="btn-reset-cd"
                    onclick="cdReset()">
                Reset
            </button>

        </div>

    </div>

</div>

</div>

<!-- Solo queda el botón de cerrar -->
<button class="exit-btn" onclick="salir()">
    ⏻ Cerrar aplicación
</button>

<script>

/* ==================================================
   CALCULADORA
================================================== */

let currentOp = 'resta';

function setOp(val, btn){

    currentOp = val;

    document.querySelectorAll('.op-btn')
        .forEach(b => b.classList.remove('active'));

    btn.classList.add('active');

    document.getElementById('op-label').textContent =
        val === 'suma'
            ? 'Tiempo a sumar'
            : 'Tiempo a restar';
}

function calcular(e){

    e.preventDefault();

    const h1 = parseInt(document.getElementById('h1').value) || 0;
    const m1 = parseInt(document.getElementById('m1').value) || 0;
    const s1 = parseInt(document.getElementById('s1').value) || 0;

    const h2 = parseInt(document.getElementById('h2').value) || 0;
    const m2 = parseInt(document.getElementById('m2').value) || 0;
    const s2 = parseInt(document.getElementById('s2').value) || 0;

    const t1 = h1*3600 + m1*60 + s1;
    const t2 = h2*3600 + m2*60 + s2;

    const result = currentOp === 'suma'
        ? (t1 + t2) % 86400
        : ((t1 - t2) % 86400 + 86400) % 86400;

    const rh = Math.floor(result / 3600);
    const rm = Math.floor((result % 3600) / 60);
    const rs = result % 60;

    document.getElementById('calc-rval').textContent =
        `${String(rh).padStart(2,'0')}:${String(rm).padStart(2,'0')}:${String(rs).padStart(2,'0')}`;

    document.getElementById('calc-result').style.display = 'block';

    return false;
}

/* ==================================================
   TABS
================================================== */

function showTab(tab, btn){

    document.querySelectorAll('.tab-btn')
        .forEach(b => b.classList.remove('active'));

    btn.classList.add('active');

    document.getElementById('panel-sw')
        .classList.toggle('visible', tab === 'sw');

    document.getElementById('panel-cd')
        .classList.toggle('visible', tab === 'cd');
}

/* ==================================================
   STOPWATCH
================================================== */

let swT0 = 0;
let swElapsed = 0;
let swRunning = false;
let swRaf = null;

let swLaps = [];
let swLapT0 = 0;

function pad(n, w=2){
    return String(Math.floor(n)).padStart(w, '0');
}

function fmtMs(ms){

    return {

        hms:
            `${pad(ms/3600000)}:` +
            `${pad((ms%3600000)/60000)}:` +
            `${pad((ms%60000)/1000)}`,

        mil:
            `.${pad(ms%1000, 3)}`
    };
}

function swToggle(){

    const btn  = document.getElementById('btn-sw-start');
    const ring = document.getElementById('ring-sw');

    if(!swRunning){

        swT0 = Date.now() - swElapsed;

        if(swLaps.length === 0){
            swLapT0 = swT0;
        }

        swRunning = true;

        ring.classList.add('running');

        btn.textContent = 'Pausar';
        btn.className = 'crono-btn cbtn-start-sw running-s';

        document.getElementById('sw-status').textContent =
            'Corriendo…';

        swRaf = requestAnimationFrame(swTick);

    }else{

        swRunning = false;

        cancelAnimationFrame(swRaf);

        ring.classList.remove('running');

        btn.textContent = 'Continuar';
        btn.className = 'crono-btn cbtn-start-sw paused';

        document.getElementById('sw-status').textContent =
            'Pausado';
    }
}

function swTick(){

    swElapsed = Date.now() - swT0;

    const f = fmtMs(swElapsed);

    document.getElementById('sw-hms').textContent = f.hms;
    document.getElementById('sw-mil').textContent = f.mil;

    swRaf = requestAnimationFrame(swTick);
}

function swLap(){

    if(swElapsed === 0){
        return;
    }

    const now = Date.now();

    const lapMs = swRunning
        ? (now - swLapT0)
        : 0;

    swLapT0 = now;

    swLaps.push({
        n: swLaps.length + 1,
        lap: lapMs
    });

    swRenderLaps();
}

function swRenderLaps(){

    const times = swLaps
        .map(l => l.lap)
        .filter(t => t > 0);

    const best  = Math.min(...times);
    const worst = Math.max(...times);

    const el = document.getElementById('laps');

    el.innerHTML = '';

    [...swLaps].reverse().forEach(l => {

        const isBest  = times.length > 1 && l.lap === best;
        const isWorst = times.length > 1 && l.lap === worst;

        const cls =
            isBest
                ? 'best'
                : isWorst
                    ? 'worst'
                    : '';

        const f = fmtMs(l.lap);

        el.insertAdjacentHTML(

            'beforeend',

            `<div class="lap-row ${cls}">
                <span class="ln">Vuelta ${l.n}</span>
                <span class="lt">${f.hms}${f.mil}</span>
            </div>`
        );
    });
}

function swReset(){

    swRunning = false;

    cancelAnimationFrame(swRaf);

    swElapsed = 0;

    swLaps = [];

    swLapT0 = 0;

    document.getElementById('sw-hms').textContent =
        '00:00:00';

    document.getElementById('sw-mil').textContent =
        '.000';

    document.getElementById('ring-sw').className =
        'crono-ring';

    const btn =
        document.getElementById('btn-sw-start');

    btn.textContent = 'Iniciar';

    btn.className = 'crono-btn cbtn-start-sw';

    document.getElementById('sw-status').textContent =
        'Listo';

    document.getElementById('laps').innerHTML = '';
}

/* ==================================================
   COUNTDOWN
================================================== */

let cdRemaining = 0;
let cdRunning = false;
let cdInterval = null;
let cdDone = false;

function cdToggle(){

    const btn =
        document.getElementById('btn-cd-start');

    const ring =
        document.getElementById('ring-cd');

    if(cdDone){

        cdReset();

        return;
    }

    if(!cdRunning){

        if(cdRemaining <= 0){

            const h = parseInt(document.getElementById('cd-h').value) || 0;
            const m = parseInt(document.getElementById('cd-m').value) || 0;
            const s = parseInt(document.getElementById('cd-s').value) || 0;

            cdRemaining = h*3600 + m*60 + s;

            if(cdRemaining <= 0){
                return;
            }
        }

        cdRunning = true;

        ring.classList.remove('countdown-done');
        ring.classList.add('countdown-run');

        btn.textContent = 'Pausar';
        btn.className = 'crono-btn cbtn-start-cd running-c';

        document.getElementById('cd-status').textContent =
            'Contando…';

        cdUpdateDisplay();

        cdInterval = setInterval(cdTick, 1000);

    }else{

        cdRunning = false;

        clearInterval(cdInterval);

        ring.classList.remove('countdown-run');

        btn.textContent = 'Continuar';
        btn.className = 'crono-btn cbtn-start-cd';

        document.getElementById('cd-status').textContent =
            'Pausado';
    }
}

function cdTick(){

    cdRemaining--;

    cdUpdateDisplay();

    if(cdRemaining <= 0){

        cdDone = true;
        cdRunning = false;

        clearInterval(cdInterval);

        document.getElementById('ring-cd').className =
            'crono-ring countdown-done';

        document.getElementById('cd-status').textContent =
            '¡Tiempo!';

        document.getElementById('cd-dot').textContent =
            '🔔';

        const btn =
            document.getElementById('btn-cd-start');

        btn.textContent = 'Reiniciar';

        btn.className = 'crono-btn cbtn-start-cd';
    }
}

function cdUpdateDisplay(){

    const h = Math.floor(cdRemaining/3600);
    const m = Math.floor((cdRemaining%3600)/60);
    const s = cdRemaining%60;

    document.getElementById('cd-hms').textContent =
        `${pad(h)}:${pad(m)}:${pad(s)}`;
}

function cdReset(){

    cdRunning = false;
    cdDone = false;

    clearInterval(cdInterval);

    cdRemaining = 0;

    document.getElementById('cd-hms').textContent =
        '00:00:00';

    document.getElementById('cd-dot').textContent =
        '⏳';

    document.getElementById('ring-cd').className =
        'crono-ring';

    const btn =
        document.getElementById('btn-cd-start');

    btn.textContent = 'Iniciar';

    btn.className = 'crono-btn cbtn-start-cd';

    document.getElementById('cd-status').textContent =
        'Configura el tiempo';
}

/* ==================================================
   EXIT
================================================== */

function salir(){

    fetch('/salir', {
        method:'POST'
    }).finally(() => {
        window.close();
    });
}

</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/salir', methods=['POST'])
def salir():
    import os
    threading.Timer(0.3, lambda: os._exit(0)).start()
    return '', 204

def iniciar_servidor():
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False
    )

def abrir_ventana():
    time.sleep(1.5)
    url = "http://127.0.0.1:5000"
    subprocess.Popen(
        f'start msedge --app={url} --window-size=1100,820 '
        f'|| start chrome --app={url} --window-size=1100,820',
        shell=True
    )

if __name__ == '__main__':
    # Abre automáticamente la ventana al iniciar (como antes)
    threading.Thread(target=abrir_ventana, daemon=True).start()
    iniciar_servidor()