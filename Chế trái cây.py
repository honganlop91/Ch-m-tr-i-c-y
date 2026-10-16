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
    padding: 14px 16px;
    color: #fff;
    text-shadow: 0 2px 6px rgba(0,0,0,0.6);
    font-weight: 800;
    font-size: 17px;
    gap: 8px;
  }
  .score-box, .lives-box, .timer-box {
    background: linear-gradient(135deg, rgba(0,0,0,0.45), rgba(0,0,0,0.25));
    border-radius: 14px;
    padding: 7px 14px;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
  }
  .lives-box span { color: #ff5252; margin-left: 3px; }
  #pause-btn {
    pointer-events: auto;
    background: linear-gradient(135deg, rgba(0,0,0,0.5), rgba(0,0,0,0.3));
    border: 1px solid rgba(255,255,255,0.15);
    color: #fff;
    width: 42px; height: 42px;
    border-radius: 50%;
    font-size: 18px;
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
    background: linear-gradient(165deg, rgba(8,30,18,0.94) 0%, rgba(15,50,28,0.96) 50%, rgba(10,35,20,0.97) 100%);
    z-index: 20;
    pointer-events: auto;
    padding: 24px;
    text-align: center;
  }
  .screen.hidden { display: none; }
  .logo {
    font-size: 46px;
    font-weight: 900;
    background: linear-gradient(90deg, #ff1744, #ff6d00, #ffea00, #00e676, #00b0ff, #d500f9);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
    letter-spacing: 1px;
    animation: logoShine 4s linear infinite;
    filter: drop-shadow(0 4px 12px rgba(0,0,0,0.4));
  }
  @keyframes logoShine {
    to { background-position: 200% center; }
  }
  .logo span {
    font-size: 30px;
    display: block;
    color: #fff;
    -webkit-text-fill-color: #fff;
    margin-top: 2px;
    letter-spacing: 6px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.5);
  }
  .btn {
    background: linear-gradient(180deg, #ff8a00 0%, #e65100 100%);
    border: none;
    color: #fff;
    font-size: 20px;
    font-weight: 800;
    padding: 15px 52px;
    border-radius: 50px;
    margin: 9px 0;
    cursor: pointer;
    box-shadow: 0 7px 0 #bf360c, 0 10px 20px rgba(0,0,0,0.35);
    transition: transform 0.08s, box-shadow 0.08s;
    min-width: 230px;
    letter-spacing: 1px;
    text-shadow: 0 1px 2px rgba(0,0,0,0.3);
  }
  .btn:active { transform: translateY(5px); box-shadow: 0 2px 0 #bf360c, 0 4px 10px rgba(0,0,0,0.3); }
  .btn.secondary {
    background: linear-gradient(180deg, #607d8b, #455a64);
    box-shadow: 0 7px 0 #263238, 0 10px 20px rgba(0,0,0,0.35);
  }
  .btn.green {
    background: linear-gradient(180deg, #66bb6a, #2e7d32);
    box-shadow: 0 7px 0 #1b5e20, 0 10px 20px rgba(0,0,0,0.35);
  }
  .mode-select { margin: 18px 0 10px; }
  .mode-select label {
    display: inline-block;
    margin: 5px;
    padding: 11px 20px;
    background: rgba(255,255,255,0.1);
    border-radius: 24px;
    color: #e0e0e0;
    cursor: pointer;
    font-size: 15px;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.12);
    transition: all 0.2s;
  }
  .mode-select input { display: none; }
  .mode-select input:checked + label {
    background: linear-gradient(135deg, #ff6b00, #ff8f00);
    color: #fff;
    box-shadow: 0 0 18px rgba(255,107,0,0.55);
    border-color: transparent;
  }
  .highscore {
    color: #ffd740;
    font-size: 16px;
    margin: 10px 0;
    font-weight: 600;
    text-shadow: 0 2px 6px rgba(0,0,0,0.4);
  }
  .instructions {
    color: #90a4ae;
    font-size: 13.5px;
    max-width: 300px;
    line-height: 1.55;
    margin-top: 14px;
  }
  .gameover-score {
    font-size: 56px;
    color: #ffd740;
    font-weight: 900;
    margin: 10px 0;
    text-shadow: 0 0 20px rgba(255,215,64,0.4), 0 4px 8px rgba(0,0,0,0.4);
  }
  .combo-text {
    position: absolute;
    font-size: 30px;
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
    top: 14px; right: 16px;
    background: linear-gradient(135deg, rgba(0,0,0,0.5), rgba(0,0,0,0.3));
    border: 1px solid rgba(255,255,255,0.12);
    color: #fff;
    width:
