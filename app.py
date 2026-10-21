# This File contains the entire streamlit app. It handles the storefront, custom orders, the admin tools for gun, inventory 
    # tracking, Gold Balance, and the 3:1 queue system

import streamlit as st
import streamlit.components.v1 as components
import datetime
import os


#  Sets up the page and configures the browser tab 
st.set_page_config(
    page_title="Gunter's Royal Blacksmith Shop",
    page_icon="⚒️",
    layout="centered"
)

# AI Assisted in the styling section below
# The color variables, dark gradients, custom scrollbars
# and tab layouts below were assisted by Artificial Intelligence in the making. 
st.markdown("""
    <style>
    /*Import google fonts*/
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Alegreya+Sans:wght@400;500;700&display=swap');

    /*CSS root variables that define the color pallete for the blacksmith*/
    :root {
        --soot: #1B1816;
        --deep: #14110F;
        --anvil: #262120;
        --steel: #3E3733;
        --ember: #E2661F;
        --molten: #F2B84B;
        --parch: #EFE4CF;
        --ash: #A89D8A;
        color-scheme: dark;
    }

    /*Application Background and controls font settings*/
    .stApp {
        background:
            radial-gradient(ellipse 80% 38% at 50% -6%, rgba(226,102,31,.26), transparent 70%),
            var(--soot);
        color: var(--parch);
        font-family: 'Alegreya Sans', 'Segoe UI', sans-serif;
        font-size: 1.05rem;
    }
    
    /*Hides Strealit header and the default elements for the footer*/
    header[data-testid="stHeader"] { background: transparent; }
    footer { visibility: hidden; }
    [data-testid="stHeaderActionElements"] { display: none; }

    /*Centering the main container width for the app*/
    [data-testid="stMainBlockContainer"], .block-container {
        max-width: 960px !important;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    /*Custom styling for the scrollbar*/
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: var(--deep); }
    ::-webkit-scrollbar-thumb { background: var(--steel); border-radius: 6px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--ember); }

    /*Overrides the text colors*/
    .stApp, .stApp p, .stApp li, .stApp label,
    [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p {
        color: var(--parch);
    }
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { color: var(--ash); }

    /*heading style and appearance*/
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
        font-family: 'Cinzel', 'Georgia', serif;
        color: var(--parch);
        letter-spacing: .03em;
    }
    .stApp h1 {
        text-align: center;
        font-size: 2.7rem;
        font-weight: 700;
        padding-bottom: .2rem;
        text-shadow: 0 0 28px rgba(226,102,31,.55);
    }
    .stApp h2 { font-size: 1.6rem; font-weight: 700; }
    .stApp h3 { font-size: 1.25rem; font-weight: 700; }
    .stApp h4 { font-size: 1.05rem; font-weight: 700; color: var(--molten); }
    [data-testid="stWidgetLabel"] p { font-weight: 500; }

    /*Inline styling*/
    code, .stApp code {
        background: rgba(226,102,31,.16);
        color: var(--molten);
        border-radius: 6px;
        padding: .1rem .4rem;
        font-size: .92em;
    }

    /*Custom rule divider - Horizontal*/
    hr {
        border: 0 !important;
        height: 2px !important;
        margin: 1.4rem 0 !important;
        background: linear-gradient(90deg, transparent, var(--ember), var(--molten), var(--ember), transparent) !important;
        opacity: .65;
    }

    /*Styling for the widget and the radio button*/
    [data-testid="stElementContainer"]:has([data-testid="stRadio"]) { width: 100% !important; }
    [data-testid="stRadio"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        width: 100% !important;
        text-align: center;
    }
    [data-testid="stRadio"] > div {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    [data-testid="stRadio"] [data-testid="stWidgetLabel"] { width: 100%; justify-content: center; }
    [data-testid="stRadio"] [data-testid="stWidgetLabel"] p { text-align: center; }
    [data-testid="stRadio"] div[role="radiogroup"] {
        gap: .6rem;
        justify-content: center !important;
        width: 100%;
    }
    [data-testid="stRadio"] label {
        background: var(--anvil);
        border: 1px solid var(--steel);
        border-radius: 999px;
        padding: .45rem 1.4rem;
        cursor: pointer;
        transition: border-color .15s, background .15s;
    }
    [data-testid="stRadio"] label:hover { border-color: var(--ember); }
    [data-testid="stRadio"] label > div:first-child { display: none; }
    [data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, var(--ember), #B8480F);
        border-color: var(--molten);
        box-shadow: 0 0 18px rgba(226,102,31,.35);
    }
    [data-testid="stRadio"] label:has(input:checked) p { color: #FFF4E0; font-weight: 700; }

    /*Styling for the navigation tabs*/
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        justify-content: space-between !important;
        width: 100% !important;
        gap: 6px;
        border-bottom: 1px solid var(--steel);
    }
    .stTabs [data-baseweb="tab"] {
        flex-grow: 1 !important;
        text-align: center !important;
        height: 3rem;
        background: transparent;
        border-radius: 10px 10px 0 0;
    }
    .stTabs [data-baseweb="tab"]:hover { background: rgba(226,102,31,.08); }
    .stTabs [data-baseweb="tab"] p {
        font-family: 'Cinzel', serif;
        font-weight: 700;
        color: var(--ash);
        letter-spacing: .02em;
    }
    .stTabs [aria-selected="true"] p { color: var(--molten); }
    .stTabs [data-baseweb="tab-highlight"] { background: var(--ember); height: 3px; }
    .stTabs [data-baseweb="tab-border"] { background: transparent; }

    /*Form Boxes and containers*/
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--steel);
        border-left-width: 4px;
        border-left-color: var(--ember);
        border-radius: 12px;
    }
    [data-testid="stForm"] {
        background: var(--anvil);
        border: 1px solid var(--steel);
        border-top: 3px solid var(--ember);
        border-radius: 14px;
        padding: 1.5rem 1.6rem;
        box-shadow: 0 10px 30px rgba(0,0,0,.35);
    }

    /*Styling for the metric cards*/
    [data-testid="stMetric"] {
        background: var(--anvil);
        border: 1px solid var(--steel);
        border-top: 3px solid var(--ember);
        border-radius: 12px;
        padding: .9rem 1rem;
    }
    [data-testid="stMetricLabel"] p { color: var(--ash); font-weight: 500; }
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] div {
        font-family: 'Cinzel', serif;
        font-weight: 700;
        color: var(--molten);
        font-size: 1.6rem;
    }

    /*Notification for alerts and competed orders, etc*/
    [data-testid="stAlert"] {
        background: var(--anvil);
        border: 1px solid var(--steel);
        border-left: 4px solid var(--steel);
        border-radius: 12px;
        color: var(--parch);
    }
    [data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) { border-left-color: var(--ember); }
    [data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) { border-left-color: #6FBF73; }
    [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) { border-left-color: var(--molten); }
    [data-testid="stAlert"]:has([data-testid="stAlertContentError"]) { border-left-color: #E5534B; }
    [data-testid="stAlert"] h3 { color: var(--molten); margin-bottom: .3rem; }
    [data-testid="stToast"] {
        background: var(--anvil);
        border: 1px solid var(--ember);
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,.45);
    }

    /*Input, dropdown and text field styling*/
    [data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"] > div {
        background: var(--deep) !important;
        border-color: var(--steel) !important;
        border-radius: 8px !important;
    }
    [data-baseweb="input"]:focus-within, [data-baseweb="select"] > div:focus-within {
        border-color: var(--ember) !important;
        box-shadow: 0 0 0 1px var(--ember);
    }
    input, textarea, [data-baseweb="select"] * { color: var(--parch) !important; }
    input { -webkit-text-fill-color: var(--parch); }
    [data-baseweb="select"] svg { fill: var(--ash); }
    [data-testid="stNumberInput"] button { background: var(--steel); color: var(--parch); }
    [data-testid="stNumberInput"] button:hover { background: var(--ember); }
    div[data-baseweb="popover"] ul, div[data-baseweb="menu"] {
        background: var(--anvil) !important;
        border: 1px solid var(--steel);
        border-radius: 10px;
    }
    div[data-baseweb="popover"] li { color: var(--parch); }
    div[data-baseweb="popover"] li:hover, div[data-baseweb="popover"] li[aria-selected="true"] {
        background: rgba(226,102,31,.22) !important;
    }
    label[data-baseweb="checkbox"] > span:first-child { border-color: var(--steel) !important; background-color: var(--deep) !important; }
    label[data-baseweb="checkbox"]:has(input:checked) > span:first-child {
        background-color: var(--ember) !important;
        border-color: var(--molten) !important;
    }

    /*Button styling*/
    .stButton > button, [data-testid="stFormSubmitButton"] > button,
    [data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-secondaryFormSubmit"] {
        background: linear-gradient(135deg, var(--molten), var(--ember));
        border: 1px solid var(--molten);
        border-radius: 10px;
        padding: .5rem 1.2rem;
        box-shadow: 0 4px 14px rgba(226,102,31,.28);
        transition: transform .12s, box-shadow .12s, filter .12s;
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
        filter: brightness(1.08);
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(226,102,31,.42);
        border-color: var(--parch);
    }
    .stButton > button:active, [data-testid="stFormSubmitButton"] > button:active { transform: translateY(0); }
    .stButton > button p, [data-testid="stFormSubmitButton"] > button p,
    [data-testid="stBaseButton-secondary"] p, [data-testid="stBaseButton-secondaryFormSubmit"] p {
        color: #1B1816;
        font-family: 'Cinzel', serif;
        font-weight: 700;
    }
    [data-testid="stFormSubmitButton"] > button { width: 100%; padding: .65rem 1.2rem; }

    /*Sidebar layout and styling*/
    [data-testid="stSidebar"] {
        background: var(--deep);
        border-right: 1px solid var(--steel);
    }
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: linear-gradient(160deg, var(--anvil), var(--deep));
        border-top-color: var(--molten);
    }
    [data-testid="stSidebar"] [data-testid="stMetricValue"], [data-testid="stSidebar"] [data-testid="stMetricValue"] div {
        font-size: 1.9rem;
    }

    /*Progress Bar Styling*/
    .stProgress > div > div { background: var(--steel) !important; border-radius: 999px; }
    .stProgress > div > div > div, .stProgress [role="progressbar"] > div {
        background: linear-gradient(90deg, #B8480F, var(--ember), var(--molten)) !important;
        border-radius: 999px;
    }
    </style>
""", unsafe_allow_html=True)

# Initializes the session state variables if they are not set already
if "orders" not in st.session_state:
    st.session_state.orders = []

if "gold_vault" not in st.session_state:
    st.session_state.gold_vault = 0

if "gunter_points" not in st.session_state:
    st.session_state.gunter_points = 50

if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Iron Ingots": 50,
        "Steel Plates": 50,
        "Mithril Ores": 50,
        "Bronze Bars": 50
    }

if "form_key" not in st.session_state:
    st.session_state.form_key = 0

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Session state to persist game outcomes permanently across reruns
if "last_game_result" not in st.session_state:
    st.session_state.last_game_result = None

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "shop"

# Minecart Dropper game shown on the page after "Close App".
# It is plain HTML + JavaScript on a canvas, embedded straight into Streamlit, so there is
# nothing to build and no extra files or static folders are needed.
DROPPER_GAME_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&display=swap">
<style>
  html, body { margin: 0; padding: 0; background: transparent; overflow: hidden; }
  #wrap { display: flex; justify-content: center; }
  canvas {
    width: 100%; max-width: 720px; height: auto; display: block;
    background: #14110F;
    border: 1px solid #3E3733; border-top: 3px solid #E2661F; border-radius: 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,.45);
    touch-action: none; outline: none; cursor: pointer;
  }
  canvas:focus-visible { box-shadow: 0 0 0 2px #F2B84B, 0 10px 30px rgba(0,0,0,.45); }
</style>
</head>
<body>
<div id="wrap">
  <canvas id="c" width="720" height="480" tabindex="0" aria-label="Minecart Dropper game. Move the cart with the arrow keys, A and D, or the mouse. Catch ore and avoid fire."></canvas>
</div>
<script>
(function () {
  'use strict';

  var cv = document.getElementById('c');
  var ctx = cv.getContext('2d');
  var W = cv.width, H = cv.height;

  var GOAL = 15;          // ore needed to close the shop
  var MAX_LIVES = 3;
  var RAIL_Y = H - 24;
  var CART_W = 120;
  var CART_H = 46;
  var CART_TOP = RAIL_Y - 12 - CART_H;   // y of the cart rim

  var COL = {
    soot: '#1B1816', deep: '#14110F', anvil: '#262120', steel: '#3E3733',
    ember: '#E2661F', molten: '#F2B84B', parch: '#EFE4CF', ash: '#A89D8A'
  };
  var SERIF = "'Cinzel', Georgia, 'Times New Roman', serif";
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // make sure the display font is ready before the first canvas text is drawn
  if (document.fonts && document.fonts.load) {
    document.fonts.load("700 30px 'Cinzel'").catch(function () {});
    document.fonts.load("500 16px 'Cinzel'").catch(function () {});
  }

  // ---------- ore + fire art ----------
  var ORE = [
    { base: '#8A95A1', hi: '#D3DCE2', lo: '#555E68' },   // iron
    { base: '#D49A22', hi: '#FFE394', lo: '#8A5A0B' },   // gold
    { base: '#46BCCD', hi: '#C9F8FC', lo: '#237887' }    // mithril
  ];
  var SHAPE = [1, 0.82, 0.96, 0.78, 1, 0.86, 0.94, 0.8];

  function drawOre(kind, r) {
    var o = ORE[kind];
    ctx.beginPath();
    for (var i = 0; i < SHAPE.length; i++) {
      var a = (i / SHAPE.length) * Math.PI * 2;
      var px = Math.cos(a) * r * SHAPE[i], py = Math.sin(a) * r * SHAPE[i];
      if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
    ctx.closePath();
    var g = ctx.createLinearGradient(-r, -r, r, r);
    g.addColorStop(0, o.hi); g.addColorStop(0.45, o.base); g.addColorStop(1, o.lo);
    ctx.fillStyle = g; ctx.fill();
    ctx.lineWidth = 1.5; ctx.strokeStyle = 'rgba(20,17,15,.85)'; ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(-r * 0.55, -r * 0.1); ctx.lineTo(-r * 0.05, -r * 0.4); ctx.lineTo(r * 0.38, r * 0.08);
    ctx.lineWidth = 1.2; ctx.strokeStyle = 'rgba(255,255,255,.4)'; ctx.stroke();
  }

  function flamePath(s) {
    ctx.beginPath();
    ctx.moveTo(0, -s * 1.3);
    ctx.bezierCurveTo(s * 0.35, -s * 0.7, s * 0.95, -s * 0.15, s * 0.7, s * 0.45);
    ctx.bezierCurveTo(s * 0.5, s * 1.0, -s * 0.5, s * 1.0, -s * 0.7, s * 0.45);
    ctx.bezierCurveTo(-s * 0.95, -s * 0.15, -s * 0.35, -s * 0.7, 0, -s * 1.3);
    ctx.closePath();
  }

  function drawFire(r, time, phase) {
    var f = 1 + Math.sin(time * 16 + phase) * 0.07;
    ctx.save();
    ctx.scale(1, f);
    ctx.shadowColor = 'rgba(226,102,31,.9)'; ctx.shadowBlur = 18;
    flamePath(r); ctx.fillStyle = '#C2410C'; ctx.fill();
    ctx.shadowBlur = 0;
    ctx.save(); ctx.translate(0, r * 0.12);
    flamePath(r * 0.68); ctx.fillStyle = COL.ember; ctx.fill();
    ctx.restore();
    ctx.save(); ctx.translate(0, r * 0.28);
    flamePath(r * 0.38); ctx.fillStyle = COL.molten; ctx.fill();
    ctx.restore();
    ctx.restore();
  }

  function drawHeart(x, y, s, fill, stroke) {
    ctx.save(); ctx.translate(x, y);
    ctx.beginPath();
    ctx.moveTo(0, s * 0.9);
    ctx.bezierCurveTo(-s * 1.3, -s * 0.1, -s * 0.7, -s * 1.0, 0, -s * 0.4);
    ctx.bezierCurveTo(s * 0.7, -s * 1.0, s * 1.3, -s * 0.1, 0, s * 0.9);
    ctx.closePath();
    ctx.fillStyle = fill; ctx.fill();
    ctx.lineWidth = 1.5; ctx.strokeStyle = stroke; ctx.stroke();
    ctx.restore();
  }

  // ---------- pre-rendered cave background ----------
  var bg = document.createElement('canvas');
  bg.width = W; bg.height = H;
  (function paintBackground() {
    var b = bg.getContext('2d');
    var g = b.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, '#0F0C0A'); g.addColorStop(0.6, '#1B1816'); g.addColorStop(1, '#2B1A11');
    b.fillStyle = g; b.fillRect(0, 0, W, H);

    g = b.createRadialGradient(W / 2, H + 30, 10, W / 2, H + 30, W * 0.75);
    g.addColorStop(0, 'rgba(226,102,31,.38)'); g.addColorStop(1, 'rgba(226,102,31,0)');
    b.fillStyle = g; b.fillRect(0, 0, W, H);

    // stalactites from a fixed sequence so the cave never changes between runs
    var seed = 7;
    function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
    b.fillStyle = '#100D0B'; b.strokeStyle = '#262120'; b.lineWidth = 1.5;
    for (var x = -10; x < W + 20; x += 34 + rnd() * 24) {
      var w = 22 + rnd() * 30, h = 22 + rnd() * 62;
      b.beginPath(); b.moveTo(x, -2); b.lineTo(x + w, -2); b.lineTo(x + w * (0.35 + rnd() * 0.3), h); b.closePath();
      b.fill(); b.stroke();
    }

    // cave floor + rails
    b.fillStyle = '#0D0A08'; b.fillRect(0, RAIL_Y + 6, W, H - RAIL_Y);
    for (var sx = 6; sx < W; sx += 38) {
      b.fillStyle = '#3A2A1E'; b.fillRect(sx, RAIL_Y + 2, 14, 12);
      b.fillStyle = '#2A1D14'; b.fillRect(sx, RAIL_Y + 11, 14, 3);
    }
    b.fillStyle = '#7C6D60'; b.fillRect(0, RAIL_Y - 1, W, 5);
    b.fillStyle = '#A89D8A'; b.fillRect(0, RAIL_Y - 1, W, 1.5);
  })();

  // ---------- game state ----------
  var state = 'ready';            // ready | playing | won | lost
  var t = 0;
  var cart = { x: W / 2 };
  var items = [], particles = [], pile = [], motes = [];
  var ore = 0, lives = MAX_LIVES;
  var spawnTimer = 0, shake = 0, flash = 0, endAt = 0;
  var input = { left: false, right: false, pointerX: null };

  for (var m = 0; m < 22; m++) {
    motes.push({ x: Math.random() * W, y: Math.random() * H, v: 6 + Math.random() * 10, s: 0.8 + Math.random() * 1.4, a: 0.1 + Math.random() * 0.25 });
  }

  function rand(a, b) { return a + Math.random() * (b - a); }

  function resetGame() {
    items = []; particles = []; pile = [];
    ore = 0; lives = MAX_LIVES;
    spawnTimer = 0.5; shake = 0; flash = 0;
    state = 'playing';
  }

  function endGame(result) {
    state = result; endAt = t; items = [];
  }

  function spawn() {
    var isFire = Math.random() < Math.min(0.42, 0.26 + ore * 0.011);
    var k = Math.random();
    items.push({
      type: isFire ? 'fire' : 'ore',
      kind: k < 0.5 ? 0 : (k < 0.85 ? 1 : 2),
      x: rand(34, W - 34), y: -30,
      r: isFire ? 17 : 14,
      vy: rand(170, 235) + ore * 9,
      rot: rand(0, 6.28), vr: rand(-2.6, 2.6), ph: rand(0, 6.28)
    });
  }

  function burst(x, y, colors, n, speed) {
    for (var i = 0; i < n; i++) {
      var a = rand(0, Math.PI * 2), s = rand(speed * 0.35, speed);
      particles.push({ x: x, y: y, vx: Math.cos(a) * s, vy: Math.sin(a) * s - speed * 0.25,
        life: 0, max: rand(0.35, 0.8), size: rand(1.6, 3.6), color: colors[(Math.random() * colors.length) | 0] });
    }
  }

  // ---------- update ----------
  function moveCart(dt) {
    var dir = (input.right ? 1 : 0) - (input.left ? 1 : 0);
    if (dir !== 0) {
      input.pointerX = null;
      cart.x += dir * 540 * dt;
    } else if (input.pointerX !== null) {
      cart.x += (input.pointerX - cart.x) * Math.min(1, 16 * dt);
    }
    var half = CART_W / 2 + 6;
    cart.x = Math.max(half, Math.min(W - half, cart.x));
  }

  function update(dt) {
    t += dt;
    moveCart(dt);

    if (state === 'playing') {
      spawnTimer -= dt;
      if (spawnTimer <= 0) {
        spawn();
        spawnTimer = Math.max(0.33, 0.92 - ore * 0.034) * rand(0.8, 1.2);
      }
      for (var i = items.length - 1; i >= 0; i--) {
        var it = items[i];
        it.y += it.vy * dt;
        it.rot += it.vr * dt;

        var inRim = it.y + it.r * 0.6 >= CART_TOP && it.y - it.r < CART_TOP + 28;
        var overCart = Math.abs(it.x - cart.x) <= CART_W / 2 - 6 + it.r * 0.5;

        if (inRim && overCart) {
          items.splice(i, 1);
          if (it.type === 'ore') {
            ore++;
            pile.push({ dx: rand(-CART_W / 2 + 20, CART_W / 2 - 20), rise: Math.random(), kind: it.kind, r: rand(8, 10.5), rot: rand(0, 6.28) });
            var c = ORE[it.kind];
            burst(it.x, CART_TOP, [c.hi, c.base, COL.molten], 14, 190);
            if (ore >= GOAL) { endGame('won'); burst(cart.x, CART_TOP - 10, [COL.molten, COL.ember, COL.parch], 70, 320); }
          } else {
            lives--;
            shake = reduceMotion ? 0 : 0.35; flash = 0.35;
            burst(it.x, CART_TOP, [COL.ember, COL.molten, '#C2410C'], 26, 260);
            if (lives <= 0) endGame('lost');
          }
        } else if (it.y - it.r * 1.5 > H) {
          items.splice(i, 1);
        }
        if (state !== 'playing') break;   // game ended mid-loop (endGame clears items)
      }
    }

    for (var p = particles.length - 1; p >= 0; p--) {
      var q = particles[p];
      q.life += dt;
      if (q.life >= q.max) { particles.splice(p, 1); continue; }
      q.vy += 520 * dt; q.x += q.vx * dt; q.y += q.vy * dt;
    }
    for (var d = 0; d < motes.length; d++) {
      var mo = motes[d];
      mo.y -= mo.v * dt;
      if (mo.y < -4) { mo.y = H + 4; mo.x = Math.random() * W; }
    }
    shake = Math.max(0, shake - dt);
    flash = Math.max(0, flash - dt);
  }

  // ---------- draw ----------
  function label(str, x, y, size, weight, color, align, glow) {
    ctx.font = weight + ' ' + size + 'px ' + SERIF;
    ctx.textAlign = align || 'left';
    ctx.textBaseline = 'alphabetic';
    if (glow) { ctx.shadowColor = glow; ctx.shadowBlur = 18; }
    ctx.fillStyle = color;
    ctx.fillText(str, x, y);
    ctx.shadowBlur = 0;
  }

  function drawCart() {
    var w = CART_W, h = CART_H;
    ctx.save();
    ctx.translate(cart.x, CART_TOP);

    // ore heaped inside the cart (behind the front wall)
    for (var i = 0; i < pile.length; i++) {
      var o = pile[i];
      ctx.save();
      ctx.translate(o.dx, -4 - (pile.length / GOAL) * 15 * o.rise);
      ctx.rotate(o.rot);
      drawOre(o.kind, o.r);
      ctx.restore();
    }

    // wheels
    var wheelY = h + 0;
    [-w / 2 + 25, w / 2 - 25].forEach(function (wx) {
      ctx.save(); ctx.translate(wx, wheelY);
      ctx.beginPath(); ctx.arc(0, 0, 11, 0, Math.PI * 2);
      ctx.fillStyle = COL.anvil; ctx.fill();
      ctx.lineWidth = 2.5; ctx.strokeStyle = COL.ash; ctx.stroke();
      ctx.rotate(cart.x / 11);
      ctx.beginPath(); ctx.moveTo(-8, 0); ctx.lineTo(8, 0); ctx.moveTo(0, -8); ctx.lineTo(0, 8);
      ctx.lineWidth = 1.5; ctx.strokeStyle = COL.steel; ctx.stroke();
      ctx.restore();
    });

    // body
    ctx.beginPath();
    ctx.moveTo(-w / 2, 0); ctx.lineTo(w / 2, 0); ctx.lineTo(w / 2 - 11, h); ctx.lineTo(-w / 2 + 11, h);
    ctx.closePath();
    var g = ctx.createLinearGradient(0, 0, 0, h);
    g.addColorStop(0, '#6A5C52'); g.addColorStop(0.5, '#4A403A'); g.addColorStop(1, '#2F2824');
    ctx.fillStyle = g; ctx.fill();
    ctx.lineWidth = 2; ctx.strokeStyle = COL.deep; ctx.stroke();

    // iron bands + rivets
    ctx.fillStyle = 'rgba(20,17,15,.45)';
    ctx.fillRect(-w / 2 + 14, 14, w - 28, 3);
    ctx.fillRect(-w / 2 + 14, 32, w - 28, 3);
    ctx.fillStyle = COL.ash;
    for (var rx = -w / 2 + 12; rx <= w / 2 - 10; rx += 20) {
      ctx.beginPath(); ctx.arc(rx, 8, 1.8, 0, Math.PI * 2); ctx.fill();
    }

    // rim
    ctx.fillStyle = '#7E6F63'; ctx.strokeStyle = COL.deep; ctx.lineWidth = 2;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(-w / 2 - 5, -5, w + 10, 11, 3); else ctx.rect(-w / 2 - 5, -5, w + 10, 11);
    ctx.fill(); ctx.stroke();
    ctx.fillStyle = 'rgba(255,255,255,.2)'; ctx.fillRect(-w / 2 - 3, -4, w + 6, 2);
    ctx.restore();
  }

  function drawHud() {
    label('ORE', 18, 30, 14, 700, COL.ash, 'left');
    label(ore + ' / ' + GOAL, 62, 31, 22, 700, COL.molten, 'left');
    // progress bar
    var bx = 18, by = 42, bw = 220, bh = 10;
    ctx.fillStyle = COL.deep; ctx.fillRect(bx, by, bw, bh);
    var pg = ctx.createLinearGradient(bx, 0, bx + bw, 0);
    pg.addColorStop(0, '#B8480F'); pg.addColorStop(0.5, COL.ember); pg.addColorStop(1, COL.molten);
    ctx.fillStyle = pg; ctx.fillRect(bx, by, bw * (ore / GOAL), bh);
    ctx.lineWidth = 1; ctx.strokeStyle = COL.steel; ctx.strokeRect(bx + 0.5, by + 0.5, bw - 1, bh - 1);
    // lives
    for (var i = 0; i < MAX_LIVES; i++) {
      var on = i < lives;
      drawHeart(W - 32 - (MAX_LIVES - 1 - i) * 34, 32, 11, on ? '#D8432F' : COL.anvil, on ? '#FFB4A0' : COL.steel);
    }
  }

  function panel(title, lines, titleColor) {
    ctx.fillStyle = 'rgba(15,12,10,.82)';
    ctx.fillRect(0, 0, W, H);
    var pw = 520, ph = 232, px = (W - pw) / 2, py = (H - ph) / 2 - 8;
    ctx.fillStyle = COL.anvil; ctx.fillRect(px, py, pw, ph);
    ctx.fillStyle = COL.ember; ctx.fillRect(px, py, pw, 3);
    ctx.lineWidth = 1; ctx.strokeStyle = COL.steel; ctx.strokeRect(px + 0.5, py + 0.5, pw - 1, ph - 1);
    label(title, W / 2, py + 62, 32, 700, titleColor || COL.parch, 'center', 'rgba(226,102,31,.55)');
    var y = py + 104;
    for (var i = 0; i < lines.length; i++) {
      label(lines[i].t, W / 2, y, lines[i].s || 17, lines[i].w || 500, lines[i].c || COL.parch, 'center');
      y += lines[i].gap || 28;
    }
  }

  function draw(time) {
    ctx.save();
    if (shake > 0) ctx.translate(rand(-5, 5) * (shake / 0.35), rand(-4, 4) * (shake / 0.35));
    ctx.drawImage(bg, 0, 0);

    for (var d = 0; d < motes.length; d++) {
      var mo = motes[d];
      ctx.fillStyle = 'rgba(242,184,75,' + mo.a + ')';
      ctx.fillRect(mo.x, mo.y, mo.s, mo.s);
    }

    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      ctx.save();
      ctx.translate(it.x, it.y);
      if (it.type === 'ore') { ctx.rotate(it.rot); drawOre(it.kind, it.r); }
      else { drawFire(it.r, time, it.ph); }
      ctx.restore();
    }

    drawCart();

    for (var p = 0; p < particles.length; p++) {
      var q = particles[p];
      ctx.globalAlpha = 1 - q.life / q.max;
      ctx.fillStyle = q.color;
      ctx.fillRect(q.x - q.size / 2, q.y - q.size / 2, q.size, q.size);
    }
    ctx.globalAlpha = 1;
    ctx.restore();

    if (flash > 0) { ctx.fillStyle = 'rgba(216,67,47,' + (flash / 0.35) * 0.32 + ')'; ctx.fillRect(0, 0, W, H); }

    drawHud();

    if (state === 'ready') {
      panel('Minecart Dropper', [
        { t: 'Catch the falling ore. Dodge the fire.', gap: 26 },
        { t: 'Collect ' + GOAL + ' ore to close the shop for the day.', gap: 36 },
        { t: 'Click, tap or press Space to begin', s: 18, w: 700, c: COL.molten, gap: 28 },
        { t: 'Move: \u2190 \u2192 or A D, or the mouse / your finger', s: 14, c: COL.ash }
      ]);
    } else if (state === 'won') {
      panel('The Shop Is Closed', [
        { t: GOAL + ' ore gathered. Gunter can rest at last.', gap: 26 },
        { t: 'Use \u201cOpen Shop\u201d above to get back to work.', gap: 36, c: COL.ash },
        { t: (t - endAt > 0.7) ? 'Click or press Space to play again' : ' ', s: 18, w: 700, c: COL.molten }
      ], COL.molten);
    } else if (state === 'lost') {
      panel('Burned Out', [
        { t: 'The fire got you with ' + ore + ' of ' + GOAL + ' ore in the cart.', gap: 26 },
        { t: 'The shop stays open a little longer.', gap: 36, c: COL.ash },
        { t: (t - endAt > 0.7) ? 'Click or press Space to try again' : ' ', s: 18, w: 700, c: COL.molten }
      ], '#F08A6B');
    }
  }

  // ---------- input ----------
  function startOrRestart() {
    if (state === 'ready' || ((state === 'won' || state === 'lost') && t - endAt > 0.7)) resetGame();
  }

  function setPointer(e) {
    var rect = cv.getBoundingClientRect();
    input.pointerX = (e.clientX - rect.left) * (W / rect.width);
  }

  cv.addEventListener('pointermove', setPointer);
  cv.addEventListener('pointerdown', function (e) {
    cv.focus();
    setPointer(e);
    if (e.pointerType !== 'mouse' && cv.setPointerCapture) { try { cv.setPointerCapture(e.pointerId); } catch (err) {} }
    startOrRestart();
  });

  window.addEventListener('keydown', function (e) {
    var k = e.key;
    if (k === 'ArrowLeft' || k === 'a' || k === 'A') { input.left = true; e.preventDefault(); }
    else if (k === 'ArrowRight' || k === 'd' || k === 'D') { input.right = true; e.preventDefault(); }
    else if (k === ' ' || k === 'Enter') { startOrRestart(); e.preventDefault(); }
    else if (k === 'ArrowUp' || k === 'ArrowDown') { e.preventDefault(); }
  });
  window.addEventListener('keyup', function (e) {
    var k = e.key;
    if (k === 'ArrowLeft' || k === 'a' || k === 'A') input.left = false;
    else if (k === 'ArrowRight' || k === 'd' || k === 'D') input.right = false;
  });
  window.addEventListener('blur', function () { input.left = input.right = false; });

  // ---------- loop ----------
  var last = performance.now();
  function frame(now) {
    requestAnimationFrame(frame);   // schedule first so a stray error can never freeze the loop
    var dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    update(dt);
    draw(now / 1000);
  }
  requestAnimationFrame(frame);
})();
</script>
</body>
</html>
"""

# Arranges active orders in a way that for every 3 express orders a regular order appears to keep it fair for everybody
def get_ordered_queue(orders_list):
    active_orders = [o for o in orders_list if o['status'] != "Completed"]
    express_orders = [o for o in active_orders if o.get('is_express')]
    standard_orders = [o for o in active_orders if not o.get('is_express')]
    
    interleaved = []
    exp_idx = 0
    std_idx = 0
    
    while exp_idx < len(express_orders) or std_idx < len(standard_orders):
        for _ in range(3):
            if exp_idx < len(express_orders):
                interleaved.append(express_orders[exp_idx])
                exp_idx += 1
        if std_idx < len(standard_orders):
            interleaved.append(standard_orders[std_idx])
            std_idx += 1
            
    return interleaved

if st.session_state.view_mode == "game":
    # open shop button
    col_top1, col_top2 = st.columns([6, 1])
    with col_top2:
        if st.button("Open Shop"):
            st.session_state.view_mode = "shop"
            st.rerun()
    
    st.markdown("<h1 style='text-align: center;'>🎯 Dropper Game </h1>", unsafe_allow_html=True)
    st.divider()

    st.write("Catch the falling ore, dodge the fire, and collect 15 ore to close up the shop for the day.")
    components.html(DROPPER_GAME_HTML, height=500)
    st.caption("Click the game once to start. Move the cart with ← → or A / D, or with your mouse / finger. You have 3 lives.")
    
    

else:
    # close shop button
    col_title, col_btn = st.columns([5, 1])
    with col_title:
        # App title and portal switch
        st.title("Gunter's Royal Blacksmith Shop")
    with col_btn:
        st.write("")
        if st.button("❌ Close App"):
            st.session_state.view_mode = "game"
            st.rerun()

    st.divider()

    portal_choice = st.radio(
        "Select Portal View:",
        ["Customer", "Gunter's Forge Hub"],
        horizontal=True
    )

    st.divider()

    # Handle customer portal view 
    if portal_choice == "Customer":
        tab_store, tab_queue = st.tabs([
            "🛒 Storefront & Order", 
            "📜 To-Do Queue"
        ])

    # Tab for placing orders
        with tab_store:
            st.subheader("Select Your Blacksmith Gear")
            st.write("Browse Gunter's legendary catalog using your magical orb.")

            catalog = {
                "Sword": {"base_price": 120, "icon": "🗡️", "desc": "Master-crafted blade balanced for royal guards and adventurers."},
                "Plate Armor": {"base_price": 350, "icon": "🛡️", "desc": "Impenetrable steel plating designed to withstand dragon fire."},
                "Chain Mail": {"base_price": 200, "icon": "⛓️", "desc": "Flexible interlocking rings providing maximum agility in battle."},
                "Cooking Pot": {"base_price": 45, "icon": "🍲", "desc": "Indestructible cast-iron pot for campfires and royal feasts."}
            }

            selected_item = st.selectbox("Choose Equipment:", list(catalog.keys()), key=f"item_{st.session_state.form_key}")
            item_info = catalog[selected_item]
            
            st.info(f"### {item_info['icon']} {selected_item}\n{item_info['desc']}\n\n**Base Price:** {item_info['base_price']} Gold Coins")

            material = st.selectbox("Select Material Grade:", [
                "Iron (Standard)", 
                "Steel (+50 Gold)", 
                "Mithril (+150 Gold)", 
                "Bronze (-20 Gold)"
            ], key=f"mat_{selected_item}_{st.session_state.form_key}")
            
            rune_enhancement = st.selectbox("Select Rune Enhancement:", [
                "None", 
                "Flame Rune (+25 Gold)", 
                "Frost Rune (+25 Gold)", 
                "Lightning Rune (+35 Gold)"
            ], key=f"rune_{selected_item}_{st.session_state.form_key}")

            st.markdown("#### ⚡ Gunter's Express Forge Service")
            express_priority = st.checkbox("Rush Order: Express Forge Priority (+50 Gold)", key=f"express_{selected_item}_{st.session_state.form_key}")

            material_extra = 0
            if "Steel" in material: material_extra = 50
            elif "Mithril" in material: material_extra = 150
            elif "Bronze" in material: material_extra = -20

            rune_cost = 0
            if "Flame" in rune_enhancement or "Frost" in rune_enhancement: rune_cost = 25
            elif "Lightning" in rune_enhancement: rune_cost = 35

            express_cost = 50 if express_priority else 0
            total_cost = item_info['base_price'] + material_extra + rune_cost + express_cost
            
            st.write(f"💰 **Total Price:** `{total_cost} Gold Coins`")

            with st.form("order_placement_form"):
                customer_name = st.text_input("Adventurer / Guild Name:", key=f"name_{st.session_state.form_key}")

                submit_btn = st.form_submit_button("Submit Order to Gunter")
                
                # Validates the input and adds the order to the session state after submitting the order
                if submit_btn:
                    if not customer_name.strip():
                        st.error("⚠️ Please enter your name before submitting!")
                    else:
                        new_id = f"Order {len(st.session_state.orders) + 101}"
                        timestamp = datetime.datetime.now().strftime("%I:%M %p")
                        
                        extra_details = rune_enhancement if rune_enhancement != "None" else "Standard Enhancement"
                        
                        mat_type = material.split(" ")[0]
                        mat_key_map = {
                            "Iron": "Iron Ingots",
                            "Steel": "Steel Plates",
                            "Mithril": "Mithril Ores",
                            "Bronze": "Bronze Bars"
                        }
                        
                        st.session_state.orders.append({
                            "id": new_id,
                            "item": selected_item,
                            "material": mat_type,
                            "material_inventory_key": mat_key_map[mat_type],
                            "extra": extra_details,
                            "is_express": express_priority,
                            "status": "Pending",
                            "time": timestamp,
                            "customer": customer_name,
                            "cost": total_cost,
                            "collected": False,
                            "materials_deducted": False
                        })
                        
                        st.session_state.form_key += 1
                        st.toast(f"🎉 Success, {customer_name}! {new_id} ({selected_item}) submitted!", icon="⚒️")
                        st.balloons()
                        st.rerun()

        # To do Queue tab for customers to see where their order lies in Gunter's active orders list
        with tab_queue:
            st.subheader("📜 To-Do Queue")

            priority_queue = get_ordered_queue(st.session_state.orders)

            if not priority_queue:
                st.info("No active orders in the forge queue right now. Place an order in the Storefront tab to see it here!")
            else:
                for idx, order in enumerate(priority_queue):
                    tag = "⚡ EXPRESS" if order.get('is_express') else "📜 STANDARD"
                    status_color = {"Pending": "🟡", "Forging": "🔥", "Ready": "🟢"}.get(order['status'], "⚪")
                    with st.container(border=True):
                        st.markdown(f"**Priority #{idx + 1} | {order['id']}** ({tag})")
                        st.write(f"👤 **Customer:** {order['customer']}")
                        st.write(f"⚒️ **Equipment:** {order['item']} ({order['material']})")
                        st.write(f"✨ **Engravings / Details:** {order['extra']}")
                        st.write(f"💰 **Total Price:** {order['cost']} Gold")
                        st.write(f"📌 **Status:** {status_color} `{order['status']}`")

    # Handles the Gunter's portal view
    else:

        # Authentication check by asking for a password
        if not st.session_state.authenticated:
            st.subheader("🔒 Gunter's Private Forge Master Portal")
            passcode = st.text_input("Enter Password:", type="password")

            if passcode.strip().lower() == "gunter":
                st.session_state.authenticated = True
                st.toast("🔓 Access Granted! Welcome back, Master Gunter.", icon="⚒️")
                st.rerun()
            elif passcode.strip() != "":
                st.error("⚠️ Access Denied! Invalid Passcode. Please try again.")
        else:

            # The sidebar for the gold balance that updates dynamically 
            st.sidebar.markdown("### 🪙 Gunter's Vault")
            st.sidebar.metric("Gold Vault Balance", f"{st.session_state.gold_vault} Gold")
            st.sidebar.caption("Updates automatically on completed orders & merchant purchases.")
            
            if st.sidebar.button("🔒 Logout of Portal"):
                st.session_state.authenticated = False
                st.rerun()

            tab_manage, tab_completed, tab_gamble = st.tabs([
                "📊 Forge Dashboard & Queue", 
                "✅ Completed Orders",
                "🎲 The Tavern & Gamble"
            ])

            # Forge Dashboard tab for managing the inventory and orders that come in for Gunter
            with tab_manage:
                st.subheader("📊 Forge Master Dashboard")
                st.write("Manage workflow, update order statuses, deduct raw materials, and monitor shop earnings.")

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Orders", len(st.session_state.orders))
                col2.metric("In Forge 🔥", sum(1 for o in st.session_state.orders if o['status'] == "Forging"))
                col3.metric("Ready 🟢", sum(1 for o in st.session_state.orders if o['status'] == "Ready"))
                col4.metric("Gold Vault 🪙", f"{st.session_state.gold_vault}g")

                st.divider()
                st.subheader("🛠️ Active Orders")

                priority_queue = get_ordered_queue(st.session_state.orders)

                if not priority_queue:
                    st.info("No pending or active orders to manage right now.")
                else:
                    for idx, order in enumerate(priority_queue):
                        tag = "⚡ EXPRESS" if order.get('is_express') else "📜 STANDARD"
                        status_color = {"Pending": "🟡", "Forging": "🔥", "Ready": "🟢"}.get(order['status'], "⚪")
                        
                        with st.container(border=True):
                            st.markdown(f"### **Priority #{idx + 1} | {order['id']}** ({tag})")
                            col_info, col_action = st.columns([2, 1])
                            
                            with col_info:
                                st.write(f"👤 **Customer:** {order['customer']}")
                                st.write(f"⚒️ **Equipment:** {order['item']} ({order['material']})")
                                st.write(f"✨ **Engravings / Details:** {order['extra']}")
                                st.write(f"💰 **Total Price:** {order['cost']} Gold Coins")
                                st.write(f"📌 **Current Status:** {status_color} `{order['status']}`")

                            with col_action:
                                st.markdown("#### Update Status")
                                status_index = ["Pending", "Forging", "Ready", "Completed"].index(order['status']) if order['status'] in ["Pending", "Forging", "Ready", "Completed"] else 0
                                new_status = st.selectbox(
                                    "Select Status:",
                                    ["Pending", "Forging", "Ready", "Completed"],
                                    index=status_index,
                                    key=f"status_select_{order['id']}"
                                )

                                # Applies the status update, updates the inventory, and collects the gold from the order if completed
                                if st.button("Apply Update", key=f"btn_update_{order['id']}"):
                                    required_mat = order['material_inventory_key']
                                    
                                    if new_status in ["Forging", "Ready", "Completed"] and not order['materials_deducted']:
                                        if st.session_state.inventory[required_mat] < 1:
                                            st.error(f"⚠️ Insufficient {required_mat}! Restock from materials below before forging.")
                                            st.stop()
                                        else:
                                            st.session_state.inventory[required_mat] -= 1
                                            order['materials_deducted'] = True
                                            st.toast(f"⚒️ Used 1 unit of {required_mat} from inventory!", icon="📦")

                                    order['status'] = new_status
                                    
                                    if new_status == "Completed" and not order['collected']:
                                        st.session_state.gold_vault += order['cost']
                                        order['collected'] = True
                                        st.toast(f"💰 Collected {order['cost']} Gold from {order['id']} into Gunter's Vault!", icon="🪙")
                                    
                                    st.success(f"{order['id']} updated to {new_status}!")
                                    st.rerun()

                st.divider()
                st.subheader("📦 Materials")
                st.write("Purchase raw supplies directly using Gold from Gunter's Vault.")

                prices = {
                    "Iron Ingots": 25,
                    "Steel Plates": 50,
                    "Mithril Ores": 100,
                    "Bronze Bars": 10
                }

                for mat_name, count in st.session_state.inventory.items():
                    st.markdown(f"#### **{mat_name}** ({count} / 50 units remaining)")
                    st.progress(min(count / 50.0, 1.0))
                    
                    unit_cost = prices[mat_name]
                    max_purchasable = 50 - count
                    
                    if max_purchasable <= 0:
                        st.caption("✅ Storage for this material is at full capacity (50/50).")
                    else:
                        col_num, col_btn = st.columns([2, 1])
                        with col_num:
                            qty_to_buy = st.number_input(
                                f"Units to buy (Cost: {unit_cost} Gold/unit):",
                                min_value=1,
                                max_value=max_purchasable,
                                value=min(5, max_purchasable),
                                key=f"buy_qty_{mat_name}"
                            )
                        with col_btn:
                            total_purchase_cost = qty_to_buy * unit_cost
                            st.write("")
                            st.write("")

                            # Handles the purchasing of the raw materials using the gold from Gunter's vault
                            if st.button(f"Buy ({total_purchase_cost}g)", key=f"buy_btn_{mat_name}"):
                                if st.session_state.gold_vault < total_purchase_cost:
                                    st.error(f"⚠️ Insufficient Gold in Vault! Need {total_purchase_cost} Gold, but only have {st.session_state.gold_vault} Gold.")
                                else:
                                    st.session_state.gold_vault -= total_purchase_cost
                                    st.session_state.inventory[mat_name] += qty_to_buy
                                    st.toast(f"📦 Purchased {qty_to_buy} units of {mat_name} for {total_purchase_cost} Gold!", icon="🛒")
                                    st.rerun()
                    st.write("---")

            # The completed orders tab where when Gunter updates an order as completed it goes here
            with tab_completed:
                st.subheader("✅ Completed Orders")
                st.write("Successfully forged and delivered orders.")

                completed_orders = [o for o in st.session_state.orders if o['status'] == "Completed"]

                if not completed_orders:
                    st.info("No completed orders in the archive yet.")
                else:
                    for order in completed_orders:
                        with st.container(border=True):
                            st.markdown(f"**{order['id']}** {'⚡ [EXPRESS]' if order.get('is_express') else ''}")
                            st.write(f"👤 **Customer:** {order['customer']}")
                            st.write(f"⚒️ **Item:** {order['item']} ({order['material']})")
                            st.write(f"✨ **Details:** {order['extra']}")
                            st.write(f"💰 **Revenue Collected:** {order['cost']} Gold")
                            st.write(f"📌 **Status:** ✅ `Completed`")

            # Gambling games for Gunter
            with tab_gamble:
                st.subheader("🍺 The Rusty Tavern")
                st.write("Welcome, Master Gunter.")
                
                col_p1, col_p2 = st.columns(2)
                col_p1.metric("🎲 Tavern Points", f"{st.session_state.gunter_points} pts")
                col_p2.metric("🪙 Vault Gold", f"{st.session_state.gold_vault} Gold")
                
                st.divider()
                
                st.markdown("#### 💱 Money & Points Changers")
                
                col_conv1, col_conv2 = st.columns(2)
                
                with col_conv1:
                    st.markdown("##### Points to Gold Vault")
                    st.write("Rate: 1 Point = 1 Gold Coin")
                    pts_to_gold = st.number_input("Points to convert:", min_value=1, max_value=max(1000000, st.session_state.gunter_points), value=1, key="pts_to_gold_qty")
                    if st.button("Convert Points ➔ Gold"):
                        if st.session_state.gunter_points <= 0 or pts_to_gold > st.session_state.gunter_points:
                            st.error("⚠️ You don't have enough points. Gamble more.")
                        else:
                            st.session_state.gunter_points -= pts_to_gold
                            st.session_state.gold_vault += pts_to_gold
                            st.toast(f"🪙 Converted {pts_to_gold} points into {pts_to_gold} gold coins!", icon="💰")
                            st.rerun()

                with col_conv2:
                    st.markdown("##### Gold Vault to Points")
                    st.write("Rate: 1 Gold Coin = 1 Point")
                    gold_to_pts = st.number_input("Gold to convert:", min_value=1, max_value=max(1000000, st.session_state.gold_vault), value=1, key="gold_to_pts_qty")
                    if st.button("Convert Gold ➔ Points"):
                        if st.session_state.gold_vault <= 0 or gold_to_pts > st.session_state.gold_vault:
                            st.error("⚠️ You don't have enough gold in your vault!")
                        else:
                            st.session_state.gold_vault -= gold_to_pts
                            st.session_state.gunter_points += gold_to_pts
                            st.toast(f"🎲 Converted {gold_to_pts} gold into {gold_to_pts} tavern points!", icon="🪙")
                            st.rerun()
                    
                st.divider()
                
                game_choice = st.radio("Choose Your Game of Chance:", ["🪙 Coin Toss (50/50)", "🎲 Hazard Dice"], horizontal=True, key="gambling_game_select")
                
                import random
                
                if "Coin Toss" in game_choice:
                    st.markdown("#### 🪙 The Royal Coin Toss")
                    st.write("Get the Flip right to double your wage.")
                    
                    max_toss_bet = max(1, st.session_state.gunter_points)
                    default_toss_val = min(10, max_toss_bet)
                    toss_bet = st.number_input("Wager Points:", min_value=1, max_value=max_toss_bet, value=default_toss_val, key="toss_bet_input")
                    coin_choice = st.radio("King or Witch?", ["King", "Witch"], horizontal=True, key="coin_call_choice")
                    
                    if st.button("Flip the Coin!", key="toss_submit_btn"):
                        if st.session_state.gunter_points <= 0:
                            st.error("⚠️ You have 0 points! Earn or convert more before gambling.")
                        elif toss_bet > st.session_state.gunter_points:
                            st.error("⚠️ You don't have enough points. Gamble more.")
                        else:
                            outcome = random.choice(["King", "Witch"])
                            img_filename = "CoinHeads.png" if outcome == "King" else "CoinTails.png"
                            
                            if coin_choice == outcome:
                                st.session_state.gunter_points += toss_bet
                                msg = f"🎉 You won `{toss_bet}` points!"
                                status_type = "success"
                            else:
                                st.session_state.gunter_points -= toss_bet
                                msg = f"💀 You lost `{toss_bet}` points."
                                status_type = "error"
                            
                            # Store in session state and trigger one-time balloons
                            st.session_state.last_game_result = {
                                "type": "coin",
                                "outcome": outcome,
                                "img": img_filename,
                                "msg": msg,
                                "status": status_type
                            }
                            if status_type == "success":
                                st.session_state.show_balloons = True
                            st.rerun()
                
                else:
                    st.markdown("#### 🎲 Hazard Dice")
                    st.write("Set your target number on a 6-sided die, then guess whether the roll will land High or Low.")
                    
                    max_hazard_bet = max(1, st.session_state.gunter_points)
                    default_hazard_val = min(10, max_hazard_bet)
                    hazard_bet = st.number_input("Wager Points:", min_value=1, max_value=max_hazard_bet, value=default_hazard_val, key="hazard_bet_input")
                    target_num = st.selectbox("Select Target Number:", [1, 2, 3, 4, 5, 6], key="hazard_target_select")
                    guess = st.radio("Will the roll be High (Above target) or Low (Below target)?", ["High", "Low"], horizontal=True, key="hazard_guess_select")
                    
                    st.caption(f"ℹ️ Target is **{target_num}**. If you pick **High**, you win if the die rolls above {target_num}. If you pick **Low**, you win if it rolls below {target_num}. (Exact matches house wins).")
                    
                    if st.button("Roll the Die!", key="hazard_roll_btn"):
                        if st.session_state.gunter_points <= 0:
                            st.error("⚠️ You have 0 points! Earn or convert more before gambling.")
                        elif hazard_bet > st.session_state.gunter_points:
                            st.error("⚠️ You don't have enough points. Gamble more.")
                        else:
                            rolled = random.randint(1, 6)
                            dice_filename = f"Dice{rolled}.png"
                            
                            won = False
                            house_win = False
                            
                            if rolled == target_num:
                                house_win = True
                            elif guess == "High" and rolled > target_num:
                                won = True
                            elif guess == "Low" and rolled < target_num:
                                won = True
                                
                            if house_win:
                                st.session_state.gunter_points -= hazard_bet
                                msg = f"🏛️ The roll matched your target exactly ({rolled}). The house takes your wager. You lost `{hazard_bet}` points."
                                status_type = "warning"
                            elif won:
                                st.session_state.gunter_points += hazard_bet
                                msg = f"🎉 Your prediction was correct! You won `{hazard_bet}` points."
                                status_type = "success"
                            else:
                                st.session_state.gunter_points -= hazard_bet
                                msg = f"💀 You lost `{hazard_bet}` points."
                                status_type = "error"
                                
                            # Store in session state and trigger one-time balloons
                            st.session_state.last_game_result = {
                                "type": "dice",
                                "rolled": rolled,
                                "img": dice_filename,
                                "msg": msg,
                                "status": status_type
                            }
                            if status_type == "success":
                                st.session_state.show_balloons = True
                            st.rerun()

                # Display the last game result the without looping balloons on reruns
                if st.session_state.last_game_result:
                    res = st.session_state.last_game_result
                    st.divider()
                    st.markdown("### 📜 Last Tavern Game Result")
                    
                    if res["type"] == "coin":
                        st.write(f"🪙 **Result:** The coin landed on **{res['outcome']}**!")
                    else:
                        st.write(f"🎲 **Result:** The die rolled a **{res['rolled']}**!")
                    
                    img_path = os.path.join(os.path.dirname(__file__), res["img"])
                    if os.path.exists(img_path):
                        st.image(img_path, width=130)
                    else:
                        st.warning(f"⚠️ Image file `{res['img']}` not found in app directory.")
                    
                    if res["status"] == "success":
                        st.success(res["msg"])
                        if st.session_state.show_balloons:
                            st.balloons()
                            st.session_state.show_balloons = False # Reset so balloons only fire once per win
                    elif res["status"] == "warning":
                        st.warning(res["msg"])
                    else:
                        st.error(res["msg"])
