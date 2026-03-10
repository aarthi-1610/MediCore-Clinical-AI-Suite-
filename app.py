import streamlit as st
import pandas as pd
import sqlite3
import joblib
import json
import requests
import io


import os
import gdown

def download_models():
    if not os.path.exists("billing_model.pkl"):
        gdown.download(
            "https://drive.google.com/uc?id=1jetZTPH0TwFT0SLHcUXT0tl-4R0nAQXi",
            "billing_model.pkl", quiet=False
        )

download_models()


# ── PDF GENERATION ──
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

st.set_page_config(page_title="MediCore | Healthcare System", page_icon="⚕️", layout="wide")

# ── HuggingFace Spaces compatibility ──
import os
os.environ["STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION"] = "false"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=DM+Mono:wght@400;500&display=swap');

:root {
    --ink:          #0a0f1e;
    --ink-2:        #1e2a42;
    --ink-3:        #3a4d6e;
    --muted:        #6b7fa0;
    --muted-lt:     #9aabc4;
    --surface:      #ffffff;
    --surface-2:    #f0f5ff;
    --surface-3:    #e4ecff;
    --blue:         #1a6cf0;
    --blue-dk:      #0f4db8;
    --blue-lt:      #deeaff;
    --blue-glow:    rgba(26,108,240,0.22);
    --cyan:         #00b8d4;
    --cyan-lt:      #e0f7fb;
    --teal:         #00897b;
    --teal-lt:      #e0f2ef;
    --amber:        #e67c00;
    --amber-lt:     #fff4e0;
    --rose:         #d62b2b;
    --rose-lt:      #ffeaea;
    --grad-hero:    linear-gradient(135deg, #060e2e 0%, #0d2260 45%, #0a5a8a 100%);
    --r-sm:  10px;
    --r-md:  16px;
    --r-lg:  22px;
    --r-xl:  32px;
    --sh-sm:  0 2px 8px rgba(10,20,60,0.08), 0 1px 3px rgba(10,20,60,0.05);
    --sh-md:  0 8px 28px rgba(10,20,60,0.13), 0 2px 8px rgba(10,20,60,0.07);
    --sh-lg:  0 20px 60px rgba(10,20,60,0.16), 0 4px 16px rgba(10,20,60,0.08);
    --sh-blue: 0 8px 32px rgba(26,108,240,0.28);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background: #e8eeff !important;
    color: var(--ink) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 4rem !important; max-width: 1200px !important; }

body::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 900px 700px at 10% 10%, rgba(26,108,240,0.13) 0%, transparent 65%),
        radial-gradient(ellipse 700px 600px at 90% 80%, rgba(0,184,212,0.11) 0%, transparent 65%),
        radial-gradient(ellipse 500px 400px at 50% 50%, rgba(10,90,138,0.07) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: bg-breathe 8s ease-in-out infinite alternate;
}
@keyframes bg-breathe {
    0%   { opacity: 0.7; transform: scale(1); }
    100% { opacity: 1;   transform: scale(1.03); }
}

body::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%231a6cf0' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
}

@keyframes reveal-up {
    from { opacity: 0; transform: translateY(36px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes reveal-left {
    from { opacity: 0; transform: translateX(-28px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes reveal-right {
    from { opacity: 0; transform: translateX(28px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes reveal-scale {
    from { opacity: 0; transform: scale(0.88); }
    to   { opacity: 1; transform: scale(1); }
}
.anim-up    { animation: reveal-up    0.65s cubic-bezier(0.16,1,0.3,1) both; }
.anim-left  { animation: reveal-left  0.65s cubic-bezier(0.16,1,0.3,1) both; }
.anim-right { animation: reveal-right 0.65s cubic-bezier(0.16,1,0.3,1) both; }
.anim-scale { animation: reveal-scale 0.55s cubic-bezier(0.34,1.56,0.64,1) both; }
.d1 { animation-delay: 0.05s; }
.d2 { animation-delay: 0.12s; }
.d3 { animation-delay: 0.20s; }
.d4 { animation-delay: 0.28s; }
.d5 { animation-delay: 0.36s; }

.mc-header {
    background: var(--grad-hero);
    margin: 0 -2rem 0;
    padding: 0 2.5rem;
    height: 64px;
    display: flex;
    align-items: center;
    gap: 16px;
    position: relative;
    overflow: hidden;
    margin-bottom: 0 !important;
    box-shadow: 0 4px 24px rgba(6,14,46,0.4);
    animation: reveal-up 0.6s cubic-bezier(0.16,1,0.3,1) both;
}
.mc-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(0,184,212,0.08);
}
.mc-header-glow {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00d4ff, #1a6cf0, #00d4ff, transparent);
    animation: shimmer 3s ease-in-out infinite;
}
@keyframes shimmer {
    0%,100% { opacity: 0.5; background-position: -200% center; }
    50%      { opacity: 1;   background-position: 200% center; }
}
.mc-logo-wrap { display: flex; align-items: center; gap: 10px; }
.mc-logo-icon {
    width: 36px; height: 36px;
    background: rgba(0,212,255,0.15);
    border: 1.5px solid rgba(0,212,255,0.3);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    backdrop-filter: blur(8px);
    box-shadow: 0 0 12px rgba(0,212,255,0.2);
    transition: transform 0.3s ease;
}
.mc-logo-icon:hover { transform: rotate(10deg) scale(1.1); }
.mc-logo-text { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 21px; color: white; letter-spacing: -0.5px; }
.mc-logo-text span { color: #62d4ff; }
.mc-divider { width: 1px; height: 26px; background: rgba(255,255,255,0.18); margin: 0 4px; }
.mc-subtitle { font-size: 12px; color: rgba(255,255,255,0.55); font-weight: 400; letter-spacing: 0.3px; }
.mc-status {
    margin-left: auto;
    display: flex; align-items: center; gap: 7px;
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.25);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    color: rgba(255,255,255,0.85);
    font-weight: 500;
}
.mc-status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #4dffcc;
    box-shadow: 0 0 8px rgba(77,255,204,0.9);
    animation: pulse-dot 2s infinite;
}
.mc-admin-badge {
    display: flex; align-items: center; gap: 7px;
    background: rgba(180,100,255,0.15);
    border: 1px solid rgba(180,100,255,0.35);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    color: #d090ff;
    font-weight: 600;
    margin-left: 10px;
}
.mc-patient-badge {
    display: flex; align-items: center; gap: 7px;
    background: rgba(0,212,255,0.15);
    border: 1px solid rgba(0,212,255,0.35);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    color: #62d4ff;
    font-weight: 600;
    margin-left: 10px;
}
@keyframes pulse-dot {
    0%,100% { box-shadow: 0 0 8px rgba(77,255,204,0.9); }
    50%      { box-shadow: 0 0 18px rgba(77,255,204,1), 0 0 4px rgba(77,255,204,0.6); }
}

.stButton > button {
    background: transparent !important;
    color: var(--muted) !important;
    border: none !important;
    border-radius: 0 !important;
    border-bottom: 2.5px solid transparent !important;
    padding: 16px 20px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.1px !important;
    position: relative !important;
}
.stButton > button:hover {
    color: var(--blue) !important;
    border-bottom-color: var(--blue) !important;
    background: var(--blue-lt) !important;
    border-radius: var(--r-sm) var(--r-sm) 0 0 !important;
    transform: translateY(-2px) !important;
}

h1 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; font-size: 32px !important; color: var(--ink) !important; letter-spacing: -1px !important; -webkit-text-fill-color: unset !important; background: none !important; line-height: 1.15 !important; }
h2, h3 { font-family: 'Syne', sans-serif !important; font-weight: 700 !important; color: var(--ink) !important; -webkit-text-fill-color: unset !important; background: none !important; }

.hero-wrap {
    background: var(--grad-hero);
    border-radius: var(--r-xl);
    padding: 48px 52px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--sh-lg), 0 0 0 1px rgba(0,212,255,0.15);
    animation: reveal-up 0.7s cubic-bezier(0.16,1,0.3,1) both;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 380px; height: 380px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,212,255,0.1) 0%, transparent 65%);
    animation: orb-float 10s ease-in-out infinite;
}
@keyframes orb-float {
    0%,100% { transform: translate(0,0) scale(1); }
    50%      { transform: translate(-20px, 15px) scale(1.05); }
}
.hero-border-top {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00d4ff 30%, #62d4ff 60%, transparent);
    border-radius: var(--r-xl) var(--r-xl) 0 0;
}
.hero-eyebrow { font-family: 'DM Mono', monospace; font-size: 11px; color: rgba(98,212,255,0.7); letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 14px; animation: reveal-left 0.6s 0.2s both; }
.hero-title { font-family: 'Syne', sans-serif; font-size: 38px; font-weight: 800; color: white; line-height: 1.12; letter-spacing: -1.5px; margin-bottom: 16px; animation: reveal-up 0.65s 0.25s both; }
.hero-title em { font-style: normal; color: #62d4ff; text-shadow: 0 0 20px rgba(98,212,255,0.4); }
.hero-desc { font-size: 15px; color: rgba(255,255,255,0.68); max-width: 520px; line-height: 1.8; font-weight: 300; animation: reveal-up 0.65s 0.32s both; }
.hero-badge-row { display: flex; gap: 10px; margin-top: 28px; flex-wrap: wrap; animation: reveal-up 0.65s 0.4s both; }
.hero-badge {
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 12px;
    color: rgba(255,255,255,0.8);
    font-weight: 500;
    backdrop-filter: blur(8px);
    transition: all 0.25s;
    cursor: default;
}
.hero-badge:hover {
    background: rgba(0,212,255,0.25);
    border-color: rgba(0,212,255,0.5);
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 8px 20px rgba(0,212,255,0.2);
}
.hero-icon-wrap {
    position: absolute; right: 52px; top: 50%;
    transform: translateY(-50%);
    font-size: 100px; opacity: 0.12;
    animation: float-icon 6s ease-in-out infinite; z-index: 1;
    filter: drop-shadow(0 0 30px rgba(0,212,255,0.3));
}
@keyframes float-icon {
    0%,100% { transform: translateY(-50%) rotate(-3deg) scale(1); }
    50%      { transform: translateY(calc(-50% - 14px)) rotate(3deg) scale(1.05); }
}

.stats-bar {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}
.stat-card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(12px);
    border-radius: var(--r-md);
    padding: 20px 24px;
    border: 1px solid rgba(26,108,240,0.12);
    box-shadow: var(--sh-sm);
    text-align: center;
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
    cursor: default;
}
.stat-card:hover {
    transform: translateY(-6px);
    box-shadow: var(--sh-md);
    border-color: var(--blue);
    background: white;
}
.stat-card-icon { font-size: 28px; margin-bottom: 8px; display: block; }
.stat-card-value { font-family: 'Syne', sans-serif; font-size: 26px; font-weight: 800; color: var(--blue); letter-spacing: -1px; }
.stat-card-label { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--muted-lt); letter-spacing: 1.5px; text-transform: uppercase; margin-top: 4px; }

.sec-label { display: flex; align-items: center; gap: 12px; margin: 28px 0 16px; }
.sec-label-line { flex: 1; height: 1px; background: linear-gradient(90deg, rgba(26,108,240,0.25), transparent); }
.sec-label-line.rev { background: linear-gradient(90deg, transparent, rgba(26,108,240,0.25)); }
.sec-label-txt { font-family: 'DM Mono', monospace; font-size: 10.5px; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; white-space: nowrap; }

.feat-card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(12px);
    border-radius: var(--r-lg);
    padding: 28px 26px;
    border: 1px solid rgba(26,108,240,0.12);
    box-shadow: var(--sh-sm);
    transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
    height: 100%; position: relative; overflow: hidden;
    cursor: default;
}
.feat-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    border-radius: var(--r-lg) var(--r-lg) 0 0;
    opacity: 0; transition: opacity 0.3s;
}
.feat-card::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(26,108,240,0.04), transparent 60%);
    opacity: 0;
    transition: opacity 0.3s;
    border-radius: var(--r-lg);
}
.feat-card:hover { box-shadow: var(--sh-lg); transform: translateY(-8px) scale(1.01); border-color: rgba(26,108,240,0.3); background: white; }
.feat-card:hover::before { opacity: 1; }
.feat-card:hover::after  { opacity: 1; }
.feat-card.blue::before  { background: linear-gradient(90deg, var(--blue), var(--cyan)); }
.feat-card.teal::before  { background: linear-gradient(90deg, var(--teal), var(--cyan)); }
.feat-card.amber::before { background: linear-gradient(90deg, var(--amber), #ffd600); }
.feat-card.purple::before{ background: linear-gradient(90deg, #7c3aed, #ec4899); }
.feat-icon-wrap { width: 52px; height: 52px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 24px; margin-bottom: 18px; transition: transform 0.35s cubic-bezier(0.34,1.56,0.64,1); }
.feat-card:hover .feat-icon-wrap { transform: scale(1.15) rotate(-8deg); }
.feat-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 16px; color: var(--ink); margin-bottom: 10px; letter-spacing: -0.3px; }
.feat-body { font-size: 14px; color: var(--muted); line-height: 1.8; }
.feat-link { margin-top: 18px; font-size: 13px; font-weight: 600; color: var(--blue); display: flex; align-items: center; gap: 4px; transition: gap 0.2s; }
.feat-card:hover .feat-link { gap: 8px; }

.howto-card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(12px);
    border-radius: var(--r-lg);
    padding: 28px 30px;
    border: 1px solid rgba(26,108,240,0.12);
    box-shadow: var(--sh-sm);
    transition: box-shadow 0.3s;
}
.howto-card:hover { box-shadow: var(--sh-md); }
.howto-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 16px; color: var(--ink); margin-bottom: 18px; display: flex; align-items: center; gap: 8px; }
.howto-step { display: flex; align-items: flex-start; gap: 14px; padding: 12px 0; border-bottom: 1px dashed rgba(26,108,240,0.12); transition: padding-left 0.3s; }
.howto-step:last-child { border-bottom: none; }
.howto-step:hover { padding-left: 6px; }
.howto-num { width: 28px; height: 28px; border-radius: 50%; background: var(--blue-lt); border: 1.5px solid rgba(26,108,240,0.2); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; color: var(--blue); flex-shrink: 0; transition: all 0.3s; }
.howto-step:hover .howto-num { background: var(--blue); color: white; transform: scale(1.1); }
.howto-text { font-size: 14px; color: var(--ink-3); line-height: 1.65; }
.howto-text b { color: var(--ink); font-weight: 600; }

.det-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; margin: 16px 0; }
.det-item {
    background: rgba(255,255,255,0.85);
    border: 1px solid rgba(26,108,240,0.12);
    border-radius: var(--r-sm);
    padding: 14px 16px;
    transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1);
    backdrop-filter: blur(8px);
}
.det-item:hover { border-color: var(--blue); background: white; transform: translateY(-4px) scale(1.02); box-shadow: 0 6px 20px rgba(26,108,240,0.14); }
.det-lbl { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--muted-lt); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px; }
.det-val { font-size: 14px; font-weight: 600; color: var(--ink); letter-spacing: -0.2px; }

.res-card { border-radius: var(--r-lg); padding: 32px 28px; text-align: center; position: relative; overflow: hidden; animation: slide-up 0.5s cubic-bezier(0.16, 1, 0.3, 1); transition: transform 0.3s, box-shadow 0.3s; }
.res-card:hover { transform: translateY(-4px); box-shadow: var(--sh-md); }
@keyframes slide-up { from { opacity: 0; transform: translateY(28px) scale(0.96); } to { opacity: 1; transform: translateY(0) scale(1); } }
.res-card.risk-low { background: linear-gradient(145deg, #f0fff8, #dcfbef); border: 1.5px solid #80e8b4; }
.res-card.risk-med { background: linear-gradient(145deg, #fffbf0, #fef4d9); border: 1.5px solid #fcd37c; }
.res-card.risk-hi  { background: linear-gradient(145deg, #fff5f5, #fde4e4); border: 1.5px solid #f5a0a0; }
.res-card.bill     { background: linear-gradient(145deg, #eef4ff, #dce8ff); border: 1.5px solid #90b4f8; }
.res-eyebrow { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); margin-bottom: 12px; }
.res-value { font-family: 'Syne', sans-serif; font-size: 48px; font-weight: 800; letter-spacing: -3px; line-height: 1; margin: 8px 0 12px; animation: count-in 0.8s cubic-bezier(0.16,1,0.3,1); }
@keyframes count-in { from { opacity: 0; transform: scale(0.6); } to { opacity: 1; transform: scale(1); } }
.res-confidence { display: inline-block; background: rgba(255,255,255,0.7); border: 1px solid rgba(255,255,255,0.9); border-radius: 20px; padding: 5px 16px; font-size: 12.5px; font-weight: 600; color: var(--ink-3); backdrop-filter: blur(8px); }
.res-note { font-size: 13px; color: var(--muted); margin-top: 12px; font-weight: 400; }

.prec-card { border-radius: var(--r-md); padding: 24px 26px; animation: slide-up 0.6s 0.1s cubic-bezier(0.16, 1, 0.3, 1) both; }
.prec-card.low { background: #f0fff8; border: 1.5px solid #80e8b4; }
.prec-card.med { background: #fffbf0; border: 1.5px solid #fcd37c; }
.prec-card.hi  { background: #fff5f5; border: 1.5px solid #f5a0a0; }
.prec-header { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 15px; color: var(--ink); margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }
.prec-list { list-style: none; padding: 0; }
.prec-list li { font-size: 14px; color: var(--ink-3); padding: 7px 0; border-bottom: 1px dashed rgba(26,108,240,0.1); display: flex; align-items: flex-start; gap: 10px; line-height: 1.6; transition: padding-left 0.25s; }
.prec-list li:last-child { border-bottom: none; }
.prec-list li:hover { padding-left: 6px; }
.prec-list li::before { content: '→'; font-weight: 700; color: var(--blue); opacity: 0.5; flex-shrink: 0; margin-top: 1px; }

.badge { display: inline-flex; align-items: center; gap: 7px; padding: 6px 16px; border-radius: 20px; font-size: 13px; font-weight: 600; letter-spacing: 0.1px; animation: badge-in 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
@keyframes badge-in { from { opacity: 0; transform: scale(0.75); } to { opacity: 1; transform: scale(1); } }
.badge-ok  { background: #e0faf0; color: #0d7a55; border: 1.5px solid #5ddba8; }
.badge-err { background: #ffeaea; color: #b52020; border: 1.5px solid #f5a0a0; }
.badge-dot { width: 7px; height: 7px; border-radius: 50%; }
.badge-ok  .badge-dot { background: #0d7a55; animation: pulse-dot 2s infinite; }
.badge-err .badge-dot { background: #b52020; }

.form-card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(12px);
    border-radius: var(--r-lg);
    padding: 32px 28px;
    border: 1px solid rgba(26,108,240,0.12);
    box-shadow: var(--sh-sm);
    margin-bottom: 20px;
    transition: box-shadow 0.3s;
}
.form-card:hover { box-shadow: var(--sh-md); }

.stTextInput input, .stNumberInput input {
    border-radius: var(--r-sm) !important;
    border: 1.5px solid rgba(26,108,240,0.18) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    background: var(--surface-2) !important;
    color: var(--ink) !important;
    padding: 12px 14px !important;
    transition: all 0.25s !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--blue) !important;
    background: white !important;
    box-shadow: 0 0 0 4px rgba(26,108,240,0.1) !important;
    outline: none !important;
}
.stSelectbox > div > div {
    border-radius: var(--r-sm) !important;
    border: 1.5px solid rgba(26,108,240,0.18) !important;
    background: var(--surface-2) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    transition: all 0.25s !important;
}
label, .stSelectbox label, div[data-testid="stWidgetLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
}

div[data-testid="stVerticalBlock"] > div:last-child .stButton > button,
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--blue) 0%, var(--blue-dk) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--r-md) !important;
    padding: 14px 28px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    box-shadow: var(--sh-blue) !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.3px !important;
}
div[data-testid="stVerticalBlock"] > div:last-child .stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 14px 44px rgba(26,108,240,0.45) !important;
}

.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.7) !important; backdrop-filter: blur(8px) !important; border-radius: var(--r-md) !important; padding: 5px !important; border: 1px solid rgba(26,108,240,0.14) !important; gap: 4px !important; }
.stTabs [data-baseweb="tab"] { border-radius: var(--r-sm) !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 13.5px !important; color: var(--muted) !important; padding: 10px 26px !important; transition: all 0.25s !important; }
.stTabs [aria-selected="true"] { background: white !important; color: var(--blue) !important; box-shadow: var(--sh-sm) !important; }

[data-testid="metric-container"] { background: rgba(255,255,255,0.9) !important; border-radius: var(--r-md) !important; border: 1px solid rgba(26,108,240,0.12) !important; padding: 18px 20px !important; box-shadow: var(--sh-sm) !important; transition: all 0.3s !important; backdrop-filter: blur(8px) !important; }
[data-testid="metric-container"]:hover { box-shadow: var(--sh-md) !important; border-color: var(--blue) !important; transform: translateY(-3px); }
[data-testid="stMetricValue"] { font-family: 'Syne', sans-serif !important; font-size: 26px !important; font-weight: 800 !important; color: var(--blue) !important; letter-spacing: -1px !important; }

.login-bg-orb-1 { position: fixed; top: -120px; left: -120px; width: 550px; height: 550px; border-radius: 50%; background: radial-gradient(circle, rgba(26,108,240,0.12), transparent 65%); pointer-events: none; animation: orb-float 12s ease-in-out infinite; }
.login-bg-orb-2 { position: fixed; bottom: -100px; right: -100px; width: 450px; height: 450px; border-radius: 50%; background: radial-gradient(circle, rgba(0,184,212,0.1), transparent 65%); pointer-events: none; animation: orb-float 14s ease-in-out infinite reverse; }
.login-brand-wrap { text-align: center; margin-bottom: 32px; animation: reveal-up 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
.login-icon { font-size: 44px; margin-bottom: 12px; display: block; animation: float-icon 4s ease-in-out infinite; filter: drop-shadow(0 0 12px rgba(26,108,240,0.3)); }
.login-brand-title { font-family: 'Syne', sans-serif; font-size: 34px; font-weight: 800; color: var(--ink); letter-spacing: -1.5px; margin-bottom: 6px; }
.login-brand-title em { font-style: normal; background: linear-gradient(135deg, var(--blue), var(--cyan)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.login-brand-sub { font-size: 14px; color: var(--muted); font-weight: 400; }
.login-card { background: rgba(255,255,255,0.9); backdrop-filter: blur(20px); border-radius: var(--r-xl); padding: 40px 36px 32px; border: 1px solid rgba(26,108,240,0.15); box-shadow: var(--sh-lg); width: 100%; animation: reveal-up 0.6s 0.15s cubic-bezier(0.16, 1, 0.3, 1) both; transition: box-shadow 0.3s; }
.login-card:hover { box-shadow: 0 28px 80px rgba(10,20,60,0.2), 0 8px 24px rgba(10,20,60,0.1); }
.login-footer { text-align: center; font-size: 12px; color: var(--muted-lt); margin-top: 20px; letter-spacing: 0.5px; animation: reveal-up 0.5s 0.4s both; }

.page-title-area { margin-bottom: 28px; animation: reveal-up 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
.page-title { font-family: 'Syne', sans-serif; font-size: 30px; font-weight: 800; color: var(--ink); letter-spacing: -1px; margin-bottom: 6px; }
.page-subtitle { font-size: 14px; color: var(--muted); font-weight: 400; line-height: 1.6; }

.divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(26,108,240,0.2), transparent); margin: 24px 0; }

.pid-banner {
    background: linear-gradient(135deg, #060e2e, #0d2260, #0a5a8a);
    border-radius: 16px;
    padding: 24px 32px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(6,14,46,0.35), 0 0 0 1px rgba(0,212,255,0.15);
    flex-wrap: wrap; gap: 16px;
    position: relative; overflow: hidden;
    animation: reveal-scale 0.6s cubic-bezier(0.34,1.56,0.64,1);
}
.pid-banner::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1.5px;
    background: linear-gradient(90deg, transparent, #00d4ff, transparent);
}
.pid-label { font-family: 'DM Mono', monospace; font-size: 10px; color: rgba(98,212,255,0.6); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; }
.pid-sub   { font-family: 'Syne', sans-serif; font-size: 14px; color: rgba(255,255,255,0.65); margin-bottom: 4px; }
.pid-value { font-family: 'Syne', sans-serif; font-size: 32px; font-weight: 800; color: #62d4ff; letter-spacing: -1px; text-shadow: 0 0 20px rgba(98,212,255,0.3); }
.pid-hint  { background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.2); border-radius: 12px; padding: 14px 20px; text-align: center; }
.pid-hint-lbl { font-size: 11px; color: rgba(255,255,255,0.45); margin-bottom: 4px; }
.pid-hint-val { font-size: 13px; color: white; font-weight: 600; }

.admin-welcome {
    background: linear-gradient(135deg, #1a0533 0%, #2d0a5e 40%, #0d2260 100%);
    border-radius: var(--r-xl);
    padding: 48px 52px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--sh-lg), 0 0 0 1px rgba(180,100,255,0.2);
    text-align: center;
    animation: reveal-up 0.7s cubic-bezier(0.16,1,0.3,1);
}
.admin-welcome::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 380px; height: 380px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(180,100,255,0.1) 0%, transparent 65%);
    animation: orb-float 10s ease-in-out infinite;
}
.admin-welcome-border {
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #b464ff 30%, #e040fb 60%, transparent);
    border-radius: var(--r-xl) var(--r-xl) 0 0;
}
.admin-welcome-icon { font-size: 60px; margin-bottom: 16px; filter: drop-shadow(0 0 20px rgba(180,100,255,0.5)); animation: float-icon 6s ease-in-out infinite; display: block; }
.admin-welcome-eyebrow { font-family: 'DM Mono', monospace; font-size: 11px; color: rgba(180,100,255,0.7); letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 12px; }
.admin-welcome-title { font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800; color: white; letter-spacing: -1.5px; margin-bottom: 10px; line-height: 1.1; }
.admin-welcome-title em { font-style: normal; color: #d090ff; text-shadow: 0 0 20px rgba(180,100,255,0.4); }
.admin-welcome-sub { font-size: 15px; color: rgba(255,255,255,0.55); font-weight: 300; }
.admin-stat-row { display: flex; gap: 14px; margin-bottom: 24px; flex-wrap: wrap; }
.admin-stat-pill {
    background: rgba(255,255,255,0.9);
    border: 1px solid rgba(26,108,240,0.14);
    border-radius: 14px;
    padding: 14px 22px;
    flex: 1; min-width: 110px;
    box-shadow: var(--sh-sm);
    backdrop-filter: blur(8px);
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
    text-align: center;
}
.admin-stat-pill:hover { transform: translateY(-5px); box-shadow: var(--sh-md); border-color: var(--blue); }
.admin-stat-lbl { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--muted-lt); letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 6px; }
.admin-stat-val { font-family: 'Syne', sans-serif; font-size: 22px; font-weight: 800; color: var(--blue); letter-spacing: -0.5px; }
.admin-db-header {
    background: linear-gradient(135deg, #1a0533, #2d0a5e);
    border-radius: var(--r-lg) var(--r-lg) 0 0;
    padding: 20px 28px;
    display: flex; align-items: center; justify-content: space-between;
}
.admin-db-title { font-family: 'Syne', sans-serif; font-size: 17px; font-weight: 700; color: white; display: flex; align-items: center; gap: 10px; }
.admin-db-count { font-family: 'DM Mono', monospace; font-size: 12px; color: rgba(180,100,255,0.85); background: rgba(180,100,255,0.15); border: 1px solid rgba(180,100,255,0.3); border-radius: 12px; padding: 4px 14px; }
.admin-db-wrap { background: white; border-radius: 0 0 var(--r-lg) var(--r-lg); border: 1px solid rgba(26,108,240,0.12); border-top: none; box-shadow: var(--sh-md); }

/* Patient Portal Welcome Card */
.patient-welcome {
    background: linear-gradient(135deg, #003d2e 0%, #005c4b 40%, #006b6b 100%);
    border-radius: var(--r-xl);
    padding: 48px 52px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--sh-lg), 0 0 0 1px rgba(0,212,180,0.2);
    text-align: center;
    animation: reveal-up 0.7s cubic-bezier(0.16,1,0.3,1);
}
.patient-welcome::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 380px; height: 380px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,212,180,0.1) 0%, transparent 65%);
    animation: orb-float 10s ease-in-out infinite;
}
.patient-welcome-border {
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #00d4b4 30%, #00ffcc 60%, transparent);
    border-radius: var(--r-xl) var(--r-xl) 0 0;
}
.patient-welcome-icon { font-size: 60px; margin-bottom: 16px; filter: drop-shadow(0 0 20px rgba(0,212,180,0.5)); animation: float-icon 6s ease-in-out infinite; display: block; }
.patient-welcome-eyebrow { font-family: 'DM Mono', monospace; font-size: 11px; color: rgba(0,212,180,0.8); letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 12px; }
.patient-welcome-title { font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800; color: white; letter-spacing: -1.5px; margin-bottom: 10px; line-height: 1.1; }
.patient-welcome-title em { font-style: normal; color: #00ffcc; text-shadow: 0 0 20px rgba(0,255,204,0.4); }
.patient-welcome-sub { font-size: 15px; color: rgba(255,255,255,0.55); font-weight: 300; }

.chat-fab-pulse {
    position: fixed;
    bottom: 28px; right: 28px;
    z-index: 9998;
    width: 60px; height: 60px;
    border-radius: 50%;
    background: rgba(26,108,240,0.3);
    animation: fab-pulse 2.5s ease-out infinite;
}
@keyframes fab-pulse {
    0%   { transform: scale(1); opacity: 0.7; }
    100% { transform: scale(2.2); opacity: 0; }
}
.chat-badge {
    position: fixed;
    bottom: 76px; right: 22px;
    z-index: 9999;
    background: linear-gradient(135deg, #060e2e, #0d2260);
    color: white;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 20px;
    white-space: nowrap;
    box-shadow: 0 4px 16px rgba(6,14,46,0.35);
    border: 1px solid rgba(0,212,255,0.2);
    animation: badge-float 3s ease-in-out infinite, reveal-up 0.6s 1.2s both;
    font-family: 'DM Sans', sans-serif;
}
@keyframes badge-float {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-4px); }
}

.chat-panel {
    position: fixed;
    bottom: 100px; right: 28px;
    z-index: 9997;
    width: 380px;
    background: rgba(255,255,255,0.97);
    backdrop-filter: blur(24px);
    border-radius: 24px;
    border: 1px solid rgba(26,108,240,0.18);
    box-shadow: 0 24px 80px rgba(10,20,60,0.22), 0 0 0 1px rgba(0,212,255,0.1);
    overflow: hidden;
    display: flex; flex-direction: column;
    max-height: 520px;
    animation: panel-open 0.45s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes panel-open {
    from { opacity: 0; transform: translateY(20px) scale(0.9); transform-origin: bottom right; }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}
.chat-header {
    background: linear-gradient(135deg, #060e2e, #0d2260, #0a5a8a);
    padding: 18px 20px;
    display: flex; align-items: center; gap: 12px;
    position: relative; overflow: hidden;
}
.chat-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #00d4ff, transparent);
}
.chat-avatar {
    width: 40px; height: 40px;
    border-radius: 50%;
    background: rgba(0,212,255,0.15);
    border: 2px solid rgba(0,212,255,0.35);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    animation: float-icon 4s ease-in-out infinite;
    box-shadow: 0 0 16px rgba(0,212,255,0.25);
}
.chat-header-info { flex: 1; }
.chat-header-name { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 15px; color: white; }
.chat-header-status { font-size: 11px; color: rgba(77,255,204,0.9); display: flex; align-items: center; gap: 5px; margin-top: 2px; }
.chat-header-status::before { content: ''; display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #4dffcc; box-shadow: 0 0 6px #4dffcc; animation: pulse-dot 2s infinite; }
.chat-messages { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; scroll-behavior: smooth; }
.chat-messages::-webkit-scrollbar { width: 4px; }
.chat-messages::-webkit-scrollbar-track { background: transparent; }
.chat-messages::-webkit-scrollbar-thumb { background: rgba(26,108,240,0.2); border-radius: 4px; }
.msg-bot { display: flex; gap: 8px; align-items: flex-end; animation: msg-in 0.35s cubic-bezier(0.16,1,0.3,1); }
.msg-user { display: flex; gap: 8px; align-items: flex-end; flex-direction: row-reverse; animation: msg-in 0.35s cubic-bezier(0.16,1,0.3,1); }
@keyframes msg-in { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.msg-bot-icon { width: 28px; height: 28px; border-radius: 50%; background: linear-gradient(135deg, #1a6cf0, #00b8d4); display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0; }
.msg-bubble-bot { background: var(--surface-2); border: 1px solid rgba(26,108,240,0.12); border-radius: 18px 18px 18px 4px; padding: 12px 16px; font-size: 13.5px; color: var(--ink-2); line-height: 1.65; max-width: 88%; }
.msg-bubble-user { background: linear-gradient(135deg, #1a6cf0, #0f4db8); border-radius: 18px 18px 4px 18px; padding: 12px 16px; font-size: 13.5px; color: white; line-height: 1.65; max-width: 88%; }
.chat-quick-btns { display: flex; flex-wrap: wrap; gap: 6px; padding: 0 16px 12px; }
.quick-btn {
    background: var(--blue-lt);
    border: 1px solid rgba(26,108,240,0.2);
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
    color: var(--blue);
    cursor: pointer;
    font-family: 'DM Sans', sans-serif;
    transition: all 0.2s;
    white-space: nowrap;
}
.quick-btn:hover { background: var(--blue); color: white; transform: translateY(-2px); }
.chat-input-row {
    display: flex; gap: 8px;
    padding: 12px 14px;
    border-top: 1px solid rgba(26,108,240,0.1);
    background: rgba(240,245,255,0.6);
}
.chat-input-row input {
    flex: 1;
    border: 1.5px solid rgba(26,108,240,0.18) !important;
    border-radius: 20px !important;
    padding: 10px 16px !important;
    font-size: 13px !important;
    font-family: 'DM Sans', sans-serif !important;
    background: white !important;
    outline: none !important;
    transition: all 0.2s !important;
}
.chat-input-row input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(26,108,240,0.1) !important;
}
.chat-send-btn {
    width: 38px; height: 38px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1a6cf0, #0f4db8);
    border: none;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    transition: all 0.25s;
    box-shadow: 0 4px 12px rgba(26,108,240,0.35);
    flex-shrink: 0;
}
.chat-send-btn:hover { transform: scale(1.12) rotate(10deg); box-shadow: 0 6px 20px rgba(26,108,240,0.5); }
.typing-dots { display: flex; gap: 4px; padding: 4px 2px; }
.typing-dots span { width: 7px; height: 7px; border-radius: 50%; background: var(--muted-lt); animation: typing 1.4s infinite; }
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing { 0%,60%,100% { transform: translateY(0); opacity: 0.4; } 30% { transform: translateY(-8px); opacity: 1; } }

.stAlert { border-radius: var(--r-md) !important; }

/* ── APPOINTMENT CARD ── */
.appt-card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(12px);
    border-radius: var(--r-lg);
    padding: 28px 30px;
    border: 1px solid rgba(26,108,240,0.12);
    box-shadow: var(--sh-sm);
    margin-bottom: 20px;
    transition: box-shadow 0.3s;
}
.appt-card:hover { box-shadow: var(--sh-md); }
.appt-confirm {
    background: linear-gradient(135deg, #003d2e, #005c4b);
    border-radius: var(--r-lg);
    padding: 28px 32px;
    position: relative; overflow: hidden;
    box-shadow: var(--sh-lg), 0 0 0 1px rgba(0,212,180,0.2);
    animation: reveal-scale 0.6s cubic-bezier(0.34,1.56,0.64,1);
    margin-bottom: 20px;
}
.appt-confirm::after {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #00d4b4, transparent);
}
.appt-confirm-icon { font-size: 42px; display: block; margin-bottom: 10px; }
.appt-confirm-title { font-family: 'Syne', sans-serif; font-size: 22px; font-weight: 800; color: white; letter-spacing: -0.5px; margin-bottom: 6px; }
.appt-confirm-sub { font-size: 14px; color: rgba(255,255,255,0.65); margin-bottom: 16px; }
.appt-detail-row { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 14px; }
.appt-pill {
    background: rgba(0,212,180,0.12);
    border: 1px solid rgba(0,212,180,0.25);
    border-radius: 12px;
    padding: 10px 18px;
    display: flex; flex-direction: column; gap: 2px;
}
.appt-pill-lbl { font-family: 'DM Mono', monospace; font-size: 9px; color: rgba(0,212,180,0.7); letter-spacing: 1.5px; text-transform: uppercase; }
.appt-pill-val { font-size: 13px; color: white; font-weight: 600; }

/* ── VOICE BUTTON ── */
.voice-btn {
    width: 38px; height: 38px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #ec4899);
    border: none; cursor: pointer;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 16px;
    transition: all 0.25s;
    box-shadow: 0 4px 12px rgba(124,58,237,0.4);
    flex-shrink: 0; vertical-align: middle;
}
.voice-btn:hover { transform: scale(1.15); box-shadow: 0 6px 20px rgba(124,58,237,0.6); }
.voice-btn.recording {
    background: linear-gradient(135deg, #c02020, #ff4444);
    animation: voice-pulse 0.8s ease-in-out infinite;
    box-shadow: 0 4px 20px rgba(192,32,32,0.6);
}
@keyframes voice-pulse {
    0%,100% { transform: scale(1);   box-shadow: 0 4px 20px rgba(192,32,32,0.5); }
    50%      { transform: scale(1.2); box-shadow: 0 8px 32px rgba(192,32,32,0.9); }
}
.voice-status {
    font-family: 'DM Mono', monospace; font-size: 11px;
    color: var(--muted); letter-spacing: 1px;
    padding: 4px 10px;
    background: var(--surface-2);
    border-radius: 12px;
    border: 1px solid rgba(26,108,240,0.12);
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# ── ADMIN CREDENTIALS ──
ADMIN_USERNAME = st.secrets["ADMIN_USERNAME"]
ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]

DATA_PATH = "healthcare_dataset.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

if "df" not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)")
c.execute("""CREATE TABLE IF NOT EXISTS appointments(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id  TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    dept        TEXT NOT NULL,
    appt_date   TEXT NOT NULL,
    time_slot   TEXT NOT NULL,
    reason      TEXT,
    status      TEXT DEFAULT 'Confirmed',
    booked_on   TEXT NOT NULL
)""")
conn.commit()

def signup_user(u, p):
    c.execute("INSERT INTO users VALUES (?,?)", (u, p))
    conn.commit()

def login_user(u, p):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    return c.fetchone()

def is_slot_booked(doctor, date, slot):
    """Returns True if that doctor-date-slot is already taken."""
    c.execute("SELECT COUNT(*) FROM appointments WHERE doctor_name=? AND appt_date=? AND time_slot=? AND status='Confirmed'",
              (doctor, date, slot))
    return c.fetchone()[0] > 0

def get_booked_slots(doctor, date):
    """Returns list of time slots already booked for a doctor on a date."""
    c.execute("SELECT time_slot FROM appointments WHERE doctor_name=? AND appt_date=? AND status='Confirmed'",
              (doctor, date))
    return [row[0] for row in c.fetchall()]

def book_appointment(patient_id, doctor, dept, date, slot, reason):
    """Books appointment only if slot is free. Returns True on success, False if slot taken."""
    from datetime import datetime
    if is_slot_booked(doctor, date, slot):
        return False
    c.execute("INSERT INTO appointments(patient_id,doctor_name,dept,appt_date,time_slot,reason,status,booked_on) VALUES(?,?,?,?,?,?,?,?)",
              (patient_id, doctor, dept, date, slot, reason, "Confirmed", datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    return True

def get_all_appointments():
    return pd.read_sql_query("SELECT * FROM appointments ORDER BY appt_date DESC, time_slot", conn)

def get_patient_appointments(pid):
    return pd.read_sql_query("SELECT * FROM appointments WHERE patient_id=? ORDER BY appt_date DESC", conn, params=(pid,))

# ── Build nested dict: Hospital → Condition → Doctors ──
def build_hospital_doctors(dataframe):
    """Returns { hospital: { condition: [doctors] } }"""
    needed = {"Hospital", "Medical Condition", "Doctor"}
    if not needed.issubset(dataframe.columns):
        return {}
    result = {}
    for hosp, h_grp in dataframe.groupby("Hospital"):
        result[hosp] = {}
        for cond, c_grp in h_grp.groupby("Medical Condition"):
            docs = sorted(c_grp["Doctor"].dropna().unique().tolist())
            if docs:
                result[hosp][cond] = docs
    return result

HOSPITAL_DOCTORS = build_hospital_doctors(st.session_state.df)
HOSPITALS        = sorted(HOSPITAL_DOCTORS.keys())

# Fallback flat DOCTORS dict (used elsewhere if needed)
def build_doctors_dict(dataframe):
    if "Doctor" not in dataframe.columns or "Medical Condition" not in dataframe.columns:
        return {"General": sorted(dataframe["Doctor"].dropna().unique().tolist()) if "Doctor" in dataframe.columns else ["Dr. House"]}
    doctors_map = {}
    for cond, grp in dataframe.groupby("Medical Condition"):
        docs = sorted(grp["Doctor"].dropna().unique().tolist())
        if docs:
            doctors_map[cond] = docs
    return doctors_map

DOCTORS = build_doctors_dict(st.session_state.df)
TIME_SLOTS = [
    "09:00 AM","09:30 AM","10:00 AM","10:30 AM","11:00 AM","11:30 AM",
    "02:00 PM","02:30 PM","03:00 PM","03:30 PM","04:00 PM","04:30 PM",
]

billing_model = joblib.load("billing_model.pkl")
risk_model    = joblib.load("risk_model.pkl")

# ── SESSION STATE ──
for k, v in [("login", False), ("page", "Home"), ("is_admin", False), ("admin_view", "welcome"),
             ("chat_open", False), ("chat_history", []), ("chat_input", ""),
             ("patient_mode", False), ("patient_pid", ""),
             ("voice_text", ""), ("appt_booked", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

ENC_CONDITION = {"Diabetes":1,"Hypertension":3,"Asthma":0,"Cancer":2,"Obesity":5,"Arthritis":4}
ENC_ADMISSION = {"Emergency":1,"Elective":0,"Urgent":2}
ENC_TEST      = {"Normal":2,"Abnormal":0,"Inconclusive":1}
ENC_GENDER    = {"Male":1,"Female":0,"Non-binary":2,"Other":3}
ENC_BLOOD     = {"A+":0,"A-":1,"B+":2,"B-":3,"O+":4,"O-":5,"AB+":6,"AB-":7}
ENC_INSURANCE = {"Medicare":3,"UnitedHealthCare":2,"Aetna":0,"Cigna":1}
RISK_LABELS   = ["Low","Medium","High"]
RISK_PCT      = {"Low":88,"Medium":73,"High":91}

def encode_gender(g): return ENC_GENDER.get(g, 0)

# ════════════════════════════════════════════════
#  PDF REPORT GENERATOR
# ════════════════════════════════════════════════
def generate_medicore_pdf(patient_data: dict) -> bytes:
    buffer = io.BytesIO()
    W, H   = A4
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=15*mm,   bottomMargin=20*mm)

    BLUE      = colors.HexColor("#1a6cf0")
    DARK_BLUE = colors.HexColor("#0d2260")
    CYAN      = colors.HexColor("#00b8d4")
    INK       = colors.HexColor("#0a0f1e")
    MUTED     = colors.HexColor("#6b7fa0")
    SURFACE   = colors.HexColor("#f0f5ff")
    GREEN     = colors.HexColor("#0d7a55");  GREEN_BG  = colors.HexColor("#e0faf0")
    AMBER     = colors.HexColor("#b85a00");  AMBER_BG  = colors.HexColor("#fef4d9")
    RED       = colors.HexColor("#c02020");  RED_BG    = colors.HexColor("#fde4e4")
    BILL_BLUE = colors.HexColor("#1a50c8");  BILL_BG   = colors.HexColor("#dce8ff")

    risk      = patient_data.get("risk_label", "Low")
    RISK_C    = {"Low": GREEN,    "Medium": AMBER,    "High": RED   }[risk]
    RISK_BG   = {"Low": GREEN_BG, "Medium": AMBER_BG, "High": RED_BG}[risk]
    RISK_TEXT = {"Low": "LOW RISK", "Medium": "MEDIUM RISK", "High": "HIGH RISK"}[risk]

    ss = getSampleStyleSheet()
    def S(name, **kw): return ParagraphStyle(name, parent=ss["Normal"], **kw)

    s_title     = S("t",  fontName="Helvetica-Bold",    fontSize=26, textColor=colors.white,     alignment=TA_LEFT, leading=30)
    s_sub       = S("s",  fontName="Helvetica",         fontSize=11, textColor=colors.HexColor("#a0c8ff"), alignment=TA_LEFT, leading=14)
    s_sec       = S("sc", fontName="Helvetica-Bold",    fontSize=10, textColor=MUTED,             alignment=TA_LEFT, spaceBefore=14, spaceAfter=6, leading=12)
    s_lbl       = S("l",  fontName="Helvetica",         fontSize=8,  textColor=MUTED,             leading=10)
    s_val       = S("v",  fontName="Helvetica-Bold",    fontSize=10, textColor=INK,               leading=13)
    s_risk_lbl  = S("rl", fontName="Helvetica",         fontSize=9,  textColor=MUTED,             alignment=TA_CENTER, leading=11)
    s_risk_val  = S("rv", fontName="Helvetica-Bold",    fontSize=26, textColor=RISK_C,            alignment=TA_CENTER, leading=30)
    s_risk_conf = S("rc", fontName="Helvetica",         fontSize=10, textColor=RISK_C,            alignment=TA_CENTER, leading=13)
    s_bill_lbl  = S("bl", fontName="Helvetica",         fontSize=9,  textColor=MUTED,             alignment=TA_CENTER, leading=11)
    s_bill_val  = S("bv", fontName="Helvetica-Bold",    fontSize=24, textColor=BILL_BLUE,         alignment=TA_CENTER, leading=28)
    s_prec_h    = S("ph", fontName="Helvetica-Bold",    fontSize=11, textColor=INK,               leading=14, spaceBefore=4)
    s_prec_i    = S("pi", fontName="Helvetica",         fontSize=10, textColor=colors.HexColor("#3a4d6e"), leading=15, leftIndent=8)
    s_foot      = S("ft", fontName="Helvetica",         fontSize=8,  textColor=MUTED,             alignment=TA_CENTER, leading=10)
    s_disc      = S("di", fontName="Helvetica-Oblique", fontSize=8,  textColor=MUTED,             alignment=TA_CENTER, leading=11)
    s_note_c    = S("nc", fontName="Helvetica",         fontSize=9,  textColor=MUTED,             alignment=TA_CENTER, leading=11)

    story = []

    # ── HEADER BANNER ──
    hdr = Table([[Paragraph("MediCore", s_title), Paragraph("Healthcare Patient Report", s_sub)]],
                colWidths=[80*mm, 90*mm])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), DARK_BLUE),
        ("TOPPADDING",    (0,0),(-1,-1), 14), ("BOTTOMPADDING",(0,0),(-1,-1), 14),
        ("LEFTPADDING",   (0,0),(-1,-1), 14), ("RIGHTPADDING", (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(hdr)
    story.append(HRFlowable(width="100%", thickness=3, color=CYAN, spaceAfter=10))

    # ── PATIENT DETAILS ──
    story.append(Paragraph("PATIENT DETAILS", s_sec))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#deeaff"), spaceAfter=8))

    def dcell(lbl, val):
        return [Paragraph(lbl, s_lbl), Paragraph(str(val), s_val)]

    fields = [
        dcell("PATIENT ID",         patient_data.get("pid", "—")),
        dcell("AGE",                 f"{patient_data.get('age','—')} years"),
        dcell("GENDER",              patient_data.get("gender", "—")),
        dcell("BLOOD TYPE",          patient_data.get("blood", "—")),
        dcell("MEDICAL CONDITION",   patient_data.get("condition", "—")),
        dcell("ADMISSION TYPE",      patient_data.get("admission", "—")),
        dcell("TEST RESULTS",        patient_data.get("test", "—")),
        dcell("INSURANCE PROVIDER",  patient_data.get("insurance", "—")),
        dcell("DATE OF ADMISSION",   patient_data.get("admitted", "—")),
        dcell("DISCHARGE DATE",      patient_data.get("discharged", "—")),
        dcell("MEDICATION",          patient_data.get("medication", "—")),
    ]
    cw = (W - 40*mm) / 3
    rows = []
    for i in range(0, len(fields), 3):
        chunk = fields[i:i+3]
        while len(chunk) < 3:
            chunk.append([Paragraph("", s_lbl), Paragraph("", s_val)])
        rows.append([chunk[0][0], chunk[1][0], chunk[2][0]])
        rows.append([chunk[0][1], chunk[1][1], chunk[2][1]])

    det = Table(rows, colWidths=[cw]*3)
    det.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SURFACE),
        ("TOPPADDING",    (0,0),(-1,-1), 4), ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),("RIGHTPADDING", (0,0),(-1,-1), 10),
        ("BOX",           (0,0),(-1,-1), 0.5, colors.HexColor("#deeaff")),
        ("INNERGRID",     (0,0),(-1,-1), 0.3, colors.HexColor("#e8eeff")),
    ]))
    story.append(det)
    story.append(Spacer(1, 12))

    # ── RESULTS: Risk + Billing ──
    story.append(Paragraph("ASSESSMENT RESULTS", s_sec))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#deeaff"), spaceAfter=8))

    rw = (W - 40*mm) / 2 - 4

    risk_tbl = Table([
        [Paragraph("HEALTH RISK LEVEL",                                  s_risk_lbl)],
        [Paragraph(RISK_TEXT,                                            s_risk_val)],
        [Paragraph(f"Confidence: {patient_data.get('risk_pct',88)}%",   s_risk_conf)],
        [Paragraph("Based on age, condition, admission type & results",  s_risk_lbl)],
    ], colWidths=[rw])
    risk_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), RISK_BG),
        ("BOX",           (0,0),(-1,-1), 1.5, RISK_C),
        ("TOPPADDING",    (0,0),(-1,-1), 10), ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("LEFTPADDING",   (0,0),(-1,-1), 10), ("RIGHTPADDING", (0,0),(-1,-1), 10),
        ("ALIGN",         (0,0),(-1,-1), "CENTER"),
    ]))

    bill_est = patient_data.get("bill_estimate", 0)
    bill_tbl = Table([
        [Paragraph("ESTIMATED TREATMENT COST",                           s_bill_lbl)],
        [Paragraph(f"Rs.{round(bill_est, 2):,}",                        s_bill_val)],
        [Paragraph("Predictive Model Estimate",                          s_note_c)],
        [Paragraph("Based on condition, insurance & admission type",     s_bill_lbl)],
    ], colWidths=[rw])
    bill_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), BILL_BG),
        ("BOX",           (0,0),(-1,-1), 1.5, BILL_BLUE),
        ("TOPPADDING",    (0,0),(-1,-1), 10), ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("LEFTPADDING",   (0,0),(-1,-1), 10), ("RIGHTPADDING", (0,0),(-1,-1), 10),
        ("ALIGN",         (0,0),(-1,-1), "CENTER"),
    ]))

    row2 = Table([[risk_tbl, bill_tbl]], colWidths=[(W-40*mm)/2]*2)
    row2.setStyle(TableStyle([
        ("LEFTPADDING",(0,0),(-1,-1),0), ("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING", (0,0),(-1,-1),0), ("BOTTOMPADDING",(0,0),(-1,-1),0),
    ]))
    story.append(row2)
    story.append(Spacer(1, 12))

    # ── HEALTH GUIDANCE ──
    story.append(Paragraph("PERSONALISED HEALTH GUIDANCE", s_sec))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#deeaff"), spaceAfter=8))

    prec_title = {"Low": "Maintain a Healthy Lifestyle",
                  "Medium": "Monitor Your Health Closely",
                  "High": "Immediate Medical Attention Required"}[risk]
    story.append(Paragraph(prec_title, s_prec_h))
    story.append(Spacer(1, 6))

    prec_rows = [[Paragraph(f"->  {item}", s_prec_i)] for item in patient_data.get("precautions", [])]
    prec_tbl = Table(prec_rows, colWidths=[W - 40*mm])
    prec_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), RISK_BG),
        ("BOX",           (0,0),(-1,-1), 0.8, RISK_C),
        ("INNERGRID",     (0,0),(-1,-1), 0.3, colors.HexColor("#e8eeff")),
        ("TOPPADDING",    (0,0),(-1,-1), 5), ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),("RIGHTPADDING", (0,0),(-1,-1), 12),
    ]))
    story.append(prec_tbl)
    story.append(Spacer(1, 18))

    # ── FOOTER ──
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#deeaff"), spaceAfter=8))
    story.append(Paragraph("MediCore Healthcare System  |  Confidential Patient Report", s_foot))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "DISCLAIMER: This report is generated by an automated system for informational purposes only. "
        "It does not constitute a medical diagnosis or treatment recommendation. "
        "Always consult a qualified healthcare professional for medical advice.",
        s_disc))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()

PRECAUTIONS = {
    "Low": {"title":"Maintain a Healthy Lifestyle","icon":"✅","cls":"low","items":["Eat balanced meals — fruits, vegetables, and whole grains daily","Exercise regularly (at least 30 minutes, 5 days a week)","Get 7–8 hours of quality sleep every night","Manage stress through meditation, reading, or hobbies","Schedule routine check-ups every 6–12 months","Stay hydrated; limit sugar, salt, and processed foods"]},
    "Medium": {"title":"Monitor Your Health Closely","icon":"⚠️","cls":"med","items":["Consult your doctor soon to review your current condition","Log symptoms daily and report any changes immediately","Follow prescribed medication or supplement schedules strictly","Avoid smoking, alcohol, and unhealthy dietary patterns","Incorporate moderate exercise; avoid extreme physical strain","Practice mindfulness, yoga, or controlled breathing exercises","Keep vaccinations and diagnostic tests up to date"]},
    "High": {"title":"Immediate Medical Attention Required","icon":"🛑","cls":"hi","items":["Visit your healthcare provider or hospital immediately","Follow all medical advice strictly — medications, diet, rest","Avoid any strenuous activity or stressful situations","Keep family members informed; arrange support at home","Monitor vital signs regularly (BP, blood sugar, temperature)","Attend all scheduled appointments and diagnostic tests","Keep emergency contacts and hospital details easily accessible"]}
}

def render_prec(label):
    p = PRECAUTIONS[label]
    items_html = "".join(f"<li>{i}</li>" for i in p["items"])
    st.markdown(f'<div class="prec-card {p["cls"]}"><div class="prec-header">{p["icon"]} &nbsp;{p["title"]}</div><ul class="prec-list">{items_html}</ul></div>', unsafe_allow_html=True)

def sec_label(txt):
    st.markdown(f'<div class="sec-label"><div class="sec-label-line rev"></div><div class="sec-label-txt">{txt}</div><div class="sec-label-line"></div></div>', unsafe_allow_html=True)

def det_grid(fields):
    items = "".join(f'<div class="det-item"><div class="det-lbl">{l}</div><div class="det-val">{v}</div></div>' for l,v in fields)
    st.markdown(f'<div class="det-grid">{items}</div>', unsafe_allow_html=True)

def generate_patient_id(dataframe):
    existing = dataframe["Patient ID"].dropna().tolist()
    nums = []
    for pid in existing:
        try: nums.append(int(str(pid).replace("ID-","").strip()))
        except: pass
    return f"ID-{(max(nums)+1) if nums else 1000}"

def save_new_patient(dataframe, data_path, patient_data):
    new_id  = generate_patient_id(dataframe)
    new_row = {col:"" for col in dataframe.columns}
    new_row.update(patient_data)
    new_row["Patient ID"] = new_id
    updated_df = pd.concat([dataframe, pd.DataFrame([new_row])], ignore_index=True)
    updated_df.to_csv(data_path, index=False)
    return new_id, updated_df

# ════════════════════════════════════════════════
#  AI CHATBOT FUNCTION
# ════════════════════════════════════════════════
def get_ai_response(user_msg, history):
    system_prompt = """You are MediBot, an expert AI health assistant for MediCore Healthcare System.
Provide helpful, accurate, compassionate health information 24/7.
- Answer health tips, wellness, diet, exercise, sleep, stress, common conditions
- Keep responses concise with emojis
- Recommend doctor for diagnosis/treatment  
- For emergencies: call 108
- If user writes Tamil, reply in Tamil"""

    messages = [{"role": "system", "content": system_prompt}]
    for h in history[-8:]:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": user_msg})

    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
           headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.7
            },
            timeout=20
        )
        data = resp.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        return f"DEBUG: {json.dumps(data, indent=2)[:500]}"
    except Exception as e:
        return f"Error: {str(e)}"

# ════════════════════════════════════════════════
#  FLOATING CHATBOT WIDGET  (with Voice Input)
# ════════════════════════════════════════════════
def render_chatbot():
    if not st.session_state.login:
        return

    st.markdown('<div class="chat-fab-pulse"></div>', unsafe_allow_html=True)

    col_dummy, col_fab = st.columns([10, 1])
    with col_fab:
        fab_label = "✕" if st.session_state.chat_open else "💬"
        if st.button(fab_label, key="chat_fab_btn"):
            st.session_state.chat_open = not st.session_state.chat_open
            if st.session_state.chat_open and not st.session_state.chat_history:
                st.session_state.chat_history = [{
                    "role": "assistant",
                    "content": "👋 Hi! I'm **MediBot**, your 24/7 health assistant.\n\nI can help you with health tips, symptom information, wellness advice, and more. How can I assist you today?"
                }]
            st.rerun()

    if not st.session_state.chat_open:
        return

    st.markdown('<div class="chat-panel">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chat-header">
        <div class="chat-avatar">🤖</div>
        <div class="chat-header-info">
            <div class="chat-header-name">MediBot AI</div>
            <div class="chat-header-status">Online · Available 24/7 · Voice Enabled 🎙️</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    messages_html = '<div class="chat-messages" id="chat-scroll">'
    for msg in st.session_state.chat_history:
        if msg["role"] == "assistant":
            content = msg["content"].replace("\n","<br>").replace("**","<b>").replace("**","</b>")
            messages_html += f'<div class="msg-bot"><div class="msg-bot-icon">🤖</div><div class="msg-bubble-bot">{content}</div></div>'
        else:
            messages_html += f'<div class="msg-user"><div class="msg-bubble-user">{msg["content"]}</div></div>'
    messages_html += '</div>'
    st.markdown(messages_html, unsafe_allow_html=True)

    st.markdown("""
    <div class="chat-quick-btns">
        <span class="quick-btn">💊 Diabetes tips</span>
        <span class="quick-btn">❤️ Heart health</span>
        <span class="quick-btn">😴 Sleep advice</span>
        <span class="quick-btn">🏃 Exercise guide</span>
    </div>
    """, unsafe_allow_html=True)

    # ── VOICE INPUT via streamlit-mic-recorder (most reliable method) ──
    # Uses st.text_input with pre-filled voice text via session_state
    if "voice_pending" not in st.session_state:
        st.session_state.voice_pending = ""

    voice_html = """
    <div id="voiceWrap" style="padding:6px 14px 10px;background:rgba(240,245,255,0.5);border-top:1px solid rgba(26,108,240,0.08);">
        <div style="display:flex;align-items:center;gap:8px;">
            <button id="voiceBtn" onclick="toggleVoice()" title="Click to speak"
                style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#7c3aed,#ec4899);
                border:none;cursor:pointer;font-size:16px;color:white;display:flex;align-items:center;
                justify-content:center;box-shadow:0 4px 12px rgba(124,58,237,0.4);transition:all 0.3s;flex-shrink:0;">
                🎙️
            </button>
            <span id="voiceStatus" style="font-family:'DM Sans',sans-serif;font-size:12px;color:#6b7fa0;
                padding:3px 10px;background:#f0f5ff;border-radius:10px;border:1px solid rgba(26,108,240,0.12);">
                🎙️ Click mic and speak — text will appear in chat box
            </span>
        </div>
        <div id="voicePreview" style="font-size:12px;color:#3a4d6e;margin-top:6px;min-height:16px;
            font-style:italic;padding:0 4px;display:none;"></div>
    </div>
    <script>
    (function() {
        let recog = null;
        let active = false;

        function getEl(id) { return document.getElementById(id); }

        function resetBtn() {
            active = false;
            getEl('voiceBtn').style.background = 'linear-gradient(135deg,#7c3aed,#ec4899)';
            getEl('voiceBtn').style.boxShadow  = '0 4px 12px rgba(124,58,237,0.4)';
            getEl('voiceBtn').innerHTML = '🎙️';
        }

        window.toggleVoice = function() {
            const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SR) {
                getEl('voiceStatus').innerText = '❌ Use Chrome or Edge browser for voice input.';
                return;
            }
            if (active) { recog && recog.stop(); return; }

            recog  = new SR();
            recog.lang            = 'en-IN';
            recog.interimResults  = true;
            recog.maxAlternatives = 1;
            recog.continuous      = false;

            recog.onstart = () => {
                active = true;
                getEl('voiceBtn').style.background = 'linear-gradient(135deg,#c02020,#ff4444)';
                getEl('voiceBtn').style.boxShadow  = '0 4px 20px rgba(192,32,32,0.5)';
                getEl('voiceBtn').innerHTML = '⏹️';
                getEl('voiceStatus').innerText = '🔴 Listening... speak now';
                getEl('voicePreview').style.display = 'none';
            };

            recog.onresult = (e) => {
                let interim = '', final_t = '';
                for (let i = e.resultIndex; i < e.results.length; i++) {
                    if (e.results[i].isFinal) final_t += e.results[i][0].transcript;
                    else interim += e.results[i][0].transcript;
                }
                const shown = final_t || interim;
                getEl('voicePreview').style.display = 'block';
                getEl('voicePreview').innerText = '💬 ' + shown;
                if (final_t) {
                    getEl('voiceStatus').innerText = '✅ Got it! Filling chat box...';
                    // Inject into Streamlit text input using key "voice_chat_input"
                    setTimeout(() => {
                        // Find the text input inside Streamlit iframe parent
                        const inputs = window.parent.document.querySelectorAll('input[type="text"]');
                        let filled = false;
                        inputs.forEach(inp => {
                            const label = inp.closest('[data-testid="stTextInput"]');
                            if (label || inp.placeholder.includes('Type') || inp.placeholder.includes('mic')) {
                                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.parent.HTMLInputElement.prototype, 'value').set;
                                nativeInputValueSetter.call(inp, final_t.trim());
                                inp.dispatchEvent(new Event('input', { bubbles: true }));
                                filled = true;
                            }
                        });
                        if (!filled) {
                            // fallback: use streamlit query param
                            const u = new URL(window.parent.location.href);
                            u.searchParams.set('vmsg', encodeURIComponent(final_t.trim()));
                            window.parent.history.replaceState({}, '', u.toString());
                        }
                        getEl('voiceStatus').innerText = '🎙️ Click mic and speak — text will appear in chat box';
                        getEl('voicePreview').style.display = 'none';
                        resetBtn();
                    }, 400);
                }
            };

            recog.onerror = (e) => {
                getEl('voiceStatus').innerText = '❌ ' + e.error + ' — try again';
                resetBtn();
            };
            recog.onend = () => { resetBtn(); };
            recog.start();
        };
    })();
    </script>
    """
    st.components.v1.html(voice_html, height=75, scrolling=False)

    # ── Check query param fallback for voice ──
    vmsg = st.query_params.get("vmsg", "")
    if vmsg and vmsg != st.session_state.get("_last_vmsg", ""):
        st.session_state["_last_vmsg"]   = vmsg
        st.session_state.voice_pending   = vmsg
        st.query_params.clear()
        st.rerun()

    # ── Text input row ──
    prefill = st.session_state.pop("voice_pending", "") if st.session_state.get("voice_pending") else ""
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "message",
            value=prefill,
            placeholder="Type your message or use mic 🎙️ above...",
            label_visibility="collapsed",
            key="chat_msg_input"
        )
        submitted = st.form_submit_button("Send ➤", width='content')
        if submitted and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
            with st.spinner("MediBot is thinking..."):
                reply = get_ai_response(user_input.strip(), st.session_state.chat_history[:-1])
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
#  LOGIN / SIGNUP
# ════════════════════════════════════════════════
if not st.session_state.login:
    st.markdown('<div class="login-bg-orb-1"></div><div class="login-bg-orb-2"></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 1.1, 1])
    with col_m:
        st.markdown("""
        <div class="login-brand-wrap">
            <span class="login-icon">⚕️</span>
            <div class="login-brand-title">Medi<em>Core</em></div>
            <div class="login-brand-sub">Patient Management &amp; Health Analytics System</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        # ── 4 TABS NOW ──
        tab1, tab2, tab3, tab4 = st.tabs(["🔐  Sign In", "📝  Create Account", "🛡️  Admin", "🏥  Patient"])

        with tab1:
            user = st.text_input("Username", placeholder="Enter your username", key="li_user")
            pwd  = st.text_input("Password", type="password", placeholder="Enter your password", key="li_pwd")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In  →", key="login_btn", width='stretch'):
                if login_user(user, pwd):
                    st.session_state.login        = True
                    st.session_state.is_admin     = False
                    st.session_state.patient_mode = False
                    st.session_state.page         = "Home"
                    st.success("Welcome back! Redirecting…"); st.rerun()
                else:
                    st.error("Incorrect username or password.")

        with tab2:
            nu  = st.text_input("Choose a Username", placeholder="Pick a unique username", key="su_user")
            np_ = st.text_input("Choose a Password", type="password", placeholder="Create a strong password", key="su_pwd")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account  →", key="signup_btn", width='stretch'):
                if nu.strip() == ADMIN_USERNAME:
                    st.error("That username is reserved.")
                else:
                    try:
                        signup_user(nu, np_); st.success("Account created! Please sign in.")
                    except:
                        st.error("Username already exists.")

        with tab3:
            st.markdown("""<div style="text-align:center;margin-bottom:18px;"><div style="font-size:32px;margin-bottom:8px;">🛡️</div><div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:#3a4d6e;margin-bottom:4px;">Admin Access Only</div><div style="font-size:13px;color:#9aabc4;">Restricted to authorised personnel</div></div>""", unsafe_allow_html=True)
            adm_user = st.text_input("Admin Username", placeholder="Enter admin username", key="adm_user")
            adm_pwd  = st.text_input("Admin Password", type="password", placeholder="Enter admin password", key="adm_pwd")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Access Admin Panel  →", key="admin_btn", width='stretch'):
                if adm_user == ADMIN_USERNAME and adm_pwd == ADMIN_PASSWORD:
                    st.session_state.login        = True
                    st.session_state.is_admin     = True
                    st.session_state.patient_mode = False
                    st.session_state.admin_view   = "welcome"
                    st.session_state.page         = "Admin"
                    st.success("Welcome, Admin!"); st.rerun()
                else:
                    st.error("Invalid admin credentials.")

        # ── NEW: PATIENT LOGIN TAB ──
        with tab4:
            st.markdown("""
            <div style="text-align:center;margin-bottom:18px;">
                <div style="font-size:32px;margin-bottom:8px;">🏥</div>
                <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:#3a4d6e;margin-bottom:4px;">Patient Portal</div>
                <div style="font-size:13px;color:#9aabc4;">Login with your Patient ID to view your health records</div>
            </div>
            """, unsafe_allow_html=True)
            pat_id  = st.text_input("Patient ID", placeholder="Enter your Patient ID e.g. ID-1001", key="pat_id")
            pat_dob = st.text_input("Date of Admission", placeholder="Enter Date of Admission e.g. 2024-01-15", key="pat_dob")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Access My Records  →", key="patient_btn", width='stretch'):
                df_check = load_data()
                match = df_check[df_check["Patient ID"] == pat_id]
                if match.empty:
                    st.error("Patient ID not found. Please check and try again.")
                elif str(match["Date of Admission"].values[0]).strip() != pat_dob.strip():
                    st.error("Date of Admission does not match. Please try again.")
                else:
                    st.session_state.login        = True
                    st.session_state.is_admin     = False
                    st.session_state.patient_mode = True
                    st.session_state.patient_pid  = pat_id
                    st.session_state.page         = "PatientPortal"
                    st.success("Welcome! Loading your records..."); st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div class="login-footer">🔒 Secure &nbsp;·&nbsp; Private &nbsp;·&nbsp; HIPAA-Friendly</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════
#  ADMIN PANEL
# ════════════════════════════════════════════════
elif st.session_state.login and st.session_state.is_admin:
    st.markdown("""
    <div class="mc-header">
        <div class="mc-header-glow"></div>
        <div class="mc-logo-wrap"><div class="mc-logo-icon">⚕️</div><div class="mc-logo-text">Medi<span>Core</span></div></div>
        <div class="mc-divider"></div>
        <div class="mc-subtitle">Patient Management &amp; Analytics</div>
        <div class="mc-admin-badge">🛡️ Admin Panel</div>
        <div class="mc-status" style="margin-left:auto;"><div class="mc-status-dot"></div>System Online</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
    df = st.session_state.df

    if st.session_state.admin_view == "welcome":
        st.markdown("""
        <div class="admin-welcome">
            <div class="admin-welcome-border"></div>
            <span class="admin-welcome-icon">🛡️</span>
            <div class="admin-welcome-eyebrow">Restricted Access · Admin Dashboard</div>
            <div class="admin-welcome-title">Welcome, <em>Admin</em></div>
            <div class="admin-welcome-sub">You have full access to the patient database. Use the buttons below to proceed.</div>
        </div>
        """, unsafe_allow_html=True)
        col_l, col_db, col_gap, col_so, col_r = st.columns([1.5, 1.2, 0.3, 1.2, 1.5])
        with col_db:
            if st.button("🗄️  Database", key="goto_db", width='stretch'):
                st.session_state.admin_view = "database"; st.rerun()
        with col_so:
            if st.button("↩  Sign Out", key="admin_signout_welcome", width='stretch'):
                st.session_state.login        = False
                st.session_state.is_admin     = False
                st.session_state.admin_view   = "welcome"; st.rerun()
    else:
        total_patients   = len(df)
        unique_hospitals = df["Hospital"].nunique() if "Hospital" in df.columns else "N/A"
        unique_conds     = df["Medical Condition"].nunique() if "Medical Condition" in df.columns else "N/A"
        avg_billing      = f"₹{pd.to_numeric(df['Billing Amount'],errors='coerce').mean():,.0f}" if "Billing Amount" in df.columns else "N/A"

        sec_label("DATABASE OVERVIEW")
        st.markdown(f"""
        <div class="admin-stat-row">
            <div class="admin-stat-pill"><div class="admin-stat-lbl">Total Patients</div><div class="admin-stat-val">{total_patients:,}</div></div>
            <div class="admin-stat-pill"><div class="admin-stat-lbl">Hospitals</div><div class="admin-stat-val">{unique_hospitals}</div></div>
            <div class="admin-stat-pill"><div class="admin-stat-lbl">Conditions</div><div class="admin-stat-val">{unique_conds}</div></div>
            <div class="admin-stat-pill"><div class="admin-stat-lbl">Avg Billing</div><div class="admin-stat-val" style="font-size:16px;">{avg_billing}</div></div>
        </div>""", unsafe_allow_html=True)

        nb1, nb2, _sp = st.columns([0.8, 0.8, 3])
        with nb1:
            if st.button("← Back", key="back_to_welcome"):
                st.session_state.admin_view = "welcome"; st.rerun()
        with nb2:
            if st.button("↩ Sign Out", key="admin_signout_db"):
                st.session_state.login        = False
                st.session_state.is_admin     = False
                st.session_state.admin_view   = "welcome"; st.rerun()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        sec_label("SEARCH & FILTER")
        fa, fb, fc = st.columns(3)
        search_q    = fa.text_input("🔍 Name / Patient ID", placeholder="e.g. ID-1001 or John")
        cond_opts   = ["All"] + (sorted(df["Medical Condition"].dropna().unique().tolist()) if "Medical Condition" in df.columns else [])
        cond_filter = fb.selectbox("Filter by Condition", cond_opts)
        adm_opts    = ["All"] + (sorted(df["Admission Type"].dropna().unique().tolist()) if "Admission Type" in df.columns else [])
        adm_filter  = fc.selectbox("Filter by Admission Type", adm_opts)

        filtered = df.copy()
        if search_q:
            mask = pd.Series([False]*len(filtered), index=filtered.index)
            for col_chk in ["Name","Patient ID"]:
                if col_chk in filtered.columns:
                    mask |= filtered[col_chk].astype(str).str.contains(search_q, case=False, na=False)
            filtered = filtered[mask]
        if cond_filter != "All" and "Medical Condition" in filtered.columns:
            filtered = filtered[filtered["Medical Condition"] == cond_filter]
        if adm_filter != "All" and "Admission Type" in filtered.columns:
            filtered = filtered[filtered["Admission Type"] == adm_filter]

        st.markdown(f'<div class="admin-db-header"><div class="admin-db-title">📋 Patient Records</div><div class="admin-db-count">{len(filtered):,} records</div></div><div class="admin-db-wrap">', unsafe_allow_html=True)
        st.dataframe(filtered.reset_index(drop=True), width='stretch', height=500)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        sec_label("EXPORT")
        st.download_button("⬇️  Download as CSV", filtered.to_csv(index=False).encode("utf-8"), "medicore_patients_export.csv", "text/csv", width='stretch')

        # ── APPOINTMENTS VIEW ──
        st.markdown("<br>", unsafe_allow_html=True)
        sec_label("ALL APPOINTMENTS")
        appts_df = get_all_appointments()
        if appts_df.empty:
            st.info("No appointments booked yet.")
        else:
            # Search/filter
            ap1, ap2 = st.columns(2)
            appt_search = ap1.text_input("🔍 Search by Patient ID / Doctor", key="appt_search_admin")
            appt_status = ap2.selectbox("Filter by Status", ["All","Confirmed","Cancelled","Completed"], key="appt_status_admin")
            fa2 = appts_df.copy()
            if appt_search:
                mask2 = fa2["patient_id"].astype(str).str.contains(appt_search, case=False, na=False) |                         fa2["doctor_name"].astype(str).str.contains(appt_search, case=False, na=False)
                fa2 = fa2[mask2]
            if appt_status != "All":
                fa2 = fa2[fa2["status"] == appt_status]
            st.markdown(f'<div class="admin-db-header"><div class="admin-db-title">📅 Appointments</div><div class="admin-db-count">{len(fa2):,} records</div></div><div class="admin-db-wrap">', unsafe_allow_html=True)
            st.dataframe(fa2.rename(columns={
                "id":"#","patient_id":"Patient ID","doctor_name":"Doctor","dept":"Department",
                "appt_date":"Date","time_slot":"Time","reason":"Reason","status":"Status","booked_on":"Booked On"
            }).reset_index(drop=True), width='stretch', height=320)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button("⬇️  Download Appointments CSV", fa2.to_csv(index=False).encode("utf-8"),
                               "medicore_appointments_export.csv", "text/csv", width='stretch')

    render_chatbot()

# ════════════════════════════════════════════════
#  PATIENT PORTAL
# ════════════════════════════════════════════════
elif st.session_state.login and st.session_state.patient_mode:
    pid = st.session_state.patient_pid
    df  = st.session_state.df
    row = df[df["Patient ID"] == pid]

    st.markdown(f"""
    <div class="mc-header">
        <div class="mc-header-glow"></div>
        <div class="mc-logo-wrap"><div class="mc-logo-icon">⚕️</div><div class="mc-logo-text">Medi<span>Core</span></div></div>
        <div class="mc-divider"></div>
        <div class="mc-subtitle">Patient Management &amp; Analytics</div>
        <div class="mc-patient-badge">🏥 Patient Portal · {pid}</div>
        <div class="mc-status" style="margin-left:auto;"><div class="mc-status-dot"></div>System Online</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="patient-welcome">
        <div class="patient-welcome-border"></div>
        <span class="patient-welcome-icon">🏥</span>
        <div class="patient-welcome-eyebrow">Patient Portal · Personal Health Dashboard</div>
        <div class="patient-welcome-title">Welcome, <em>Patient</em></div>
        <div class="patient-welcome-sub">Your personal health summary, risk level, and billing estimate are shown below.</div>
    </div>
    """, unsafe_allow_html=True)

    if not row.empty:
        age    = row["Age"].values[0]
        gender = row["Gender"].values[0]
        blood  = row["Blood Type"].values[0]
        cond   = row["Medical Condition"].values[0]
        adm    = row["Admission Type"].values[0]
        test   = row["Test Results"].values[0]
        ins    = row["Insurance Provider"].values[0]
        adtd   = row["Date of Admission"].values[0]
        dchd   = row["Discharge Date"].values[0]
        med    = row["Medication"].values[0] if "Medication" in row.columns else "N/A"
        billing= row["Billing Amount"].values[0] if "Billing Amount" in row.columns else "N/A"

        # ── PATIENT DETAILS ──
        sec_label("YOUR PATIENT DETAILS")
        det_grid([
            ("Patient ID", pid),
            ("Age", f"{age} yrs"),
            ("Gender", gender),
            ("Blood Type", blood),
            ("Condition", cond),
            ("Admission Type", adm),
            ("Test Results", test),
            ("Insurance", ins),
            ("Admitted", adtd),
            ("Discharged", dchd),
            ("Medication", med),
            ("Billing Amount", f"₹{float(billing):,.2f}" if billing and billing != "" else "N/A")
        ])

        st.markdown("<br>", unsafe_allow_html=True)

        # ── HEALTH RISK ──
        sec_label("YOUR HEALTH RISK")
        X     = pd.DataFrame([[int(age), ENC_CONDITION[cond], ENC_ADMISSION[adm], ENC_TEST[test]]],
                              columns=["Age","Medical Condition","Admission Type","Test Results"])
        res   = risk_model.predict(X)[0]
        label = RISK_LABELS[res]
        pct   = RISK_PCT[label]
        cls   = {"Low":"risk-low","Medium":"risk-med","High":"risk-hi"}[label]
        col   = {"Low":"#0d7a55","Medium":"#b85a00","High":"#c02020"}[label]
        icon  = {"Low":"🟢","Medium":"🟡","High":"🔴"}[label]

        rc1, rc2 = st.columns([1, 1.6])
        with rc1:
            st.markdown(f'''
            <div class="res-card {cls}">
                <div class="res-eyebrow">Your Health Risk Level</div>
                <div class="res-value" style="color:{col};">{icon} {label}</div>
                <div class="res-confidence">Confidence: {pct}%</div>
                <div class="res-note">Based on your clinical data</div>
            </div>''', unsafe_allow_html=True)
        with rc2:
            render_prec(label)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── BILLING ESTIMATE ──
        sec_label("YOUR ESTIMATED BILLING")
        Xb = pd.DataFrame([[int(age), encode_gender(gender), ENC_BLOOD[blood],
                            ENC_CONDITION[cond], ENC_ADMISSION[adm],
                            ENC_INSURANCE[ins], ENC_TEST[test]]],
                          columns=["Age","Gender","Blood Type","Medical Condition",
                                   "Admission Type","Insurance Provider","Test Results"])
        bill_res = billing_model.predict(Xb)[0]

        bc1, bc2 = st.columns([1, 1.4])
        with bc1:
            st.markdown(f'''
            <div class="res-card bill">
                <div class="res-eyebrow">Estimated Treatment Cost</div>
                <div class="res-value" style="color:#1a50c8;font-size:38px;">₹{round(bill_res,2):,}</div>
                <div class="res-confidence">Cost Estimate</div>
                <div class="res-note">Based on your condition &amp; insurance</div>
            </div>''', unsafe_allow_html=True)
        with bc2:
            st.markdown(f'''
            <div class="form-card">
                <div class="howto-title" style="margin-bottom:14px;">📊 Cost Breakdown Factors</div>
                <div class="det-grid" style="grid-template-columns:1fr 1fr;">
                    <div class="det-item"><div class="det-lbl">Condition</div><div class="det-val">{cond}</div></div>
                    <div class="det-item"><div class="det-lbl">Admission</div><div class="det-val">{adm}</div></div>
                    <div class="det-item"><div class="det-lbl">Insurance</div><div class="det-val">{ins}</div></div>
                    <div class="det-item"><div class="det-lbl">Test Result</div><div class="det-val">{test}</div></div>
                </div>
                <div style="margin-top:14px;font-size:13px;color:#6b7fa0;padding:10px 14px;background:#f0f5ff;border-radius:8px;border:1px dashed rgba(26,108,240,0.2);">
                    📅 &nbsp;Treatment period: &nbsp;<b>{adtd}</b> &nbsp;→&nbsp; <b>{dchd}</b>
                </div>
            </div>''', unsafe_allow_html=True)

    else:
        st.error("Patient record not found. Please contact hospital staff.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PDF DOWNLOAD ──
    if not row.empty:
        sec_label("DOWNLOAD YOUR REPORT")
        pdf_portal = generate_medicore_pdf({
            "pid": pid, "age": age, "gender": gender, "blood": blood,
            "condition": cond, "admission": adm, "test": test,
            "insurance": ins, "admitted": adtd, "discharged": dchd,
            "medication": med,
            "risk_label": label, "risk_pct": pct,
            "bill_estimate": bill_res,
            "precautions": PRECAUTIONS[label]["items"],
        })
        dl1, dl2, dl3 = st.columns([1, 2, 1])
        with dl2:
            st.download_button(
                label="⬇️  Download My Health Report (PDF)",
                data=pdf_portal,
                file_name=f"MediCore_MyReport_{pid}.pdf",
                mime="application/pdf",
                width='stretch',
            )

    # ── MY APPOINTMENTS (patient portal) ──
    st.markdown("<br>", unsafe_allow_html=True)
    sec_label("MY APPOINTMENTS")
    my_appts = get_patient_appointments(pid)
    if my_appts.empty:
        st.info("You have no appointments booked yet. Use the main menu to book one.")
    else:
        show_c = ["appt_date","time_slot","doctor_name","dept","reason","status"]
        show_c = [c for c in show_c if c in my_appts.columns]
        st.dataframe(my_appts[show_c].rename(columns={
            "appt_date":"Date","time_slot":"Time","doctor_name":"Doctor",
            "dept":"Department","reason":"Reason","status":"Status"
        }), hide_index=True, width='stretch')

    st.markdown("<br>", unsafe_allow_html=True)
    _, so_col, _ = st.columns([2, 1, 2])
    with so_col:
        if st.button("↩ Sign Out", key="patient_signout", width='stretch'):
            st.session_state.login        = False
            st.session_state.patient_mode = False
            st.session_state.patient_pid  = ""
            st.session_state.page         = "Home"
            st.rerun()

    render_chatbot()

# ════════════════════════════════════════════════
#  MAIN APP
# ════════════════════════════════════════════════
else:
    st.markdown("""
    <div class="mc-header">
        <div class="mc-header-glow"></div>
        <div class="mc-logo-wrap"><div class="mc-logo-icon">⚕️</div><div class="mc-logo-text">Medi<span>Core</span></div></div>
        <div class="mc-divider"></div>
        <div class="mc-subtitle">Patient Management &amp; Analytics</div>
        <div class="mc-status"><div class="mc-status-dot"></div>System Online</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    n1, n2, n3, n4, n5, n6 = st.columns(6)
    if n1.button("🏠  Home",             width='stretch'): st.session_state.page = "Home"
    if n2.button("🩺  Risk Check",       width='stretch'): st.session_state.page = "Risk"
    if n3.button("💰  Billing",          width='stretch'): st.session_state.page = "Billing"
    if n4.button("🆕  New Patient",      width='stretch'): st.session_state.page = "NewPatient"
    if n5.button("📅  Appointment",      width='stretch'): st.session_state.page = "Appointment"
    if n6.button("↩  Sign Out",          width='stretch'):
        st.session_state.login        = False
        st.session_state.is_admin     = False
        st.session_state.patient_mode = False
        st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    df = st.session_state.df

    # ── HOME ──
    if st.session_state.page == "Home":
        st.markdown("""
        <div class="hero-wrap">
            <div class="hero-border-top"></div>
            <div class="hero-icon-wrap">⚕️</div>
            <div class="hero-eyebrow">v2.0  ·  HEALTHCARE ANALYTICS PLATFORM</div>
            <div class="hero-title">Smart Patient Care,<br><em>Smarter Decisions</em></div>
            <div class="hero-desc">Assess health risks, estimate treatment costs, and provide personalised care guidance — all from a single, unified platform designed for modern healthcare professionals.</div>
            <div class="hero-badge-row">
                <div class="hero-badge">🩺 Risk Assessment</div>
                <div class="hero-badge">💰 Billing Prediction</div>
                <div class="hero-badge">🆕 Patient Registry</div>
                <div class="hero-badge">📅 Appointment Booking</div>
                <div class="hero-badge">🤖 MediBot AI</div>
                <div class="hero-badge">📄 PDF Reports</div>
                <div class="hero-badge">🔒 Secure &amp; Private</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        total_p = len(df)
        avg_age = int(pd.to_numeric(df["Age"], errors="coerce").mean()) if "Age" in df.columns else "--"
        conds   = df["Medical Condition"].nunique() if "Medical Condition" in df.columns else "--"
        hosps   = df["Hospital"].nunique() if "Hospital" in df.columns else "--"

        total_appts = len(get_all_appointments())
        docs_count  = df["Doctor"].nunique() if "Doctor" in df.columns else "--"
        st.markdown(f"""
        <div class="stats-bar anim-up d2" style="grid-template-columns:repeat(5,1fr);">
            <div class="stat-card"><span class="stat-card-icon">👥</span><div class="stat-card-value">{total_p:,}</div><div class="stat-card-label">Total Patients</div></div>
            <div class="stat-card"><span class="stat-card-icon">🏥</span><div class="stat-card-value">{hosps}</div><div class="stat-card-label">Hospitals</div></div>
            <div class="stat-card"><span class="stat-card-icon">🦠</span><div class="stat-card-value">{conds}</div><div class="stat-card-label">Conditions</div></div>
            <div class="stat-card"><span class="stat-card-icon">👨‍⚕️</span><div class="stat-card-value">{docs_count}</div><div class="stat-card-label">Doctors</div></div>
            <div class="stat-card"><span class="stat-card-icon">📅</span><div class="stat-card-value">{total_appts}</div><div class="stat-card-label">Appointments</div></div>
        </div>
        """, unsafe_allow_html=True)

        sec_label("CORE FEATURES")
        # Row 1 — 3 cards
        r1c1, r1c2, r1c3 = st.columns(3)
        row1 = [
            (r1c1, "blue",   "🩺", "#deeaff", "Health Risk Assessment",
             "Evaluate vitals, test results and medical history to determine <b>Low</b>, <b>Medium</b>, or <b>High</b> risk levels instantly.",
             "Start Assessment →"),
            (r1c2, "teal",   "💰", "#e0f2ef", "Billing Estimation",
             "Predict treatment costs based on condition, insurance, admission type, and clinical parameters — in one click.",
             "Estimate Cost →"),
            (r1c3, "amber",  "🆕", "#fff4e0", "New Patient Registration",
             "Register patients, auto-generate a unique Patient ID, and get instant risk + billing results in one single step.",
             "Register Patient →"),
        ]
        for col, cls, icon, bg, title, body, link in row1:
            with col:
                st.markdown(f'<div class="feat-card {cls} anim-up"><div class="feat-icon-wrap" style="background:{bg};">{icon}</div><div class="feat-title">{title}</div><div class="feat-body">{body}</div><div class="feat-link">{link}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Row 2 — 3 cards
        r2c1, r2c2, r2c3 = st.columns(3)
        row2 = [
            (r2c1, "purple", "📅", "#f0e8ff", "Doctor Appointment Booking",
             "Book appointments with real doctors from the dataset. Live slot availability check — no double bookings allowed.",
             "Book Appointment →"),
            (r2c2, "blue",   "🤖", "#deeaff", "MediBot AI Assistant",
             "24/7 bilingual AI health assistant (English &amp; Tamil). Ask health questions by typing or using the 🎙️ voice input feature.",
             "Chat Now →"),
            (r2c3, "teal",   "📄", "#e0f2ef", "PDF Report Generation",
             "Download a professional health report with patient details, risk level, billing estimate, and health guidance — instantly.",
             "Download Report →"),
        ]
        for col, cls, icon, bg, title, body, link in row2:
            with col:
                st.markdown(f'<div class="feat-card {cls} anim-up d2"><div class="feat-icon-wrap" style="background:{bg};">{icon}</div><div class="feat-title">{title}</div><div class="feat-body">{body}</div><div class="feat-link">{link}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        sec_label("HOW TO USE")
        st.markdown("""
        <div class="howto-card anim-up d3">
            <div class="howto-title">📋 Quick Start Guide</div>
            <div class="howto-step"><div class="howto-num">1</div><div class="howto-text"><b>New Patient?</b> — Click <b>New Patient</b>, fill in all details and hit Submit. A unique Patient ID (e.g. <code style="background:#deeaff;padding:1px 6px;border-radius:4px;font-size:12px;color:#1a6cf0;">ID-2621</code>) is auto-generated and saved to the dataset.</div></div>
            <div class="howto-step"><div class="howto-num">2</div><div class="howto-text"><b>Risk Check</b> — Enter Patient ID to instantly get a <b>Low / Medium / High</b> health risk classification with personalised health guidance and a downloadable PDF report.</div></div>
            <div class="howto-step"><div class="howto-num">3</div><div class="howto-text"><b>Billing Estimation</b> — Enter Patient ID to predict the estimated treatment cost based on condition, insurance provider, and admission type. Download the billing PDF report.</div></div>
            <div class="howto-step"><div class="howto-num">4</div><div class="howto-text"><b>Book Appointment</b> — Enter Patient ID, select department, doctor, date, and time. System shows <span style="color:#0d7a55;font-weight:600;">✅ Available</span> and <span style="color:#c02020;font-weight:600;">❌ Booked</span> slots in real time — no double bookings allowed.</div></div>
            <div class="howto-step"><div class="howto-num">5</div><div class="howto-text"><b>MediBot AI</b> — Click the 💬 button (bottom-right) to chat with MediBot. Ask health questions by typing or click 🎙️ to use voice input (Chrome/Edge required).</div></div>
            <div class="howto-step"><div class="howto-num">6</div><div class="howto-text"><b>Patient Login</b> — Patients can login separately using their Patient ID + Date of Admission to view their own risk result, billing, appointments, and download their health report.</div></div>
        </div>
        """, unsafe_allow_html=True)

    # ── RISK CHECK ──
    elif st.session_state.page == "Risk":
        st.markdown('<div class="page-title-area"><div class="page-title">🩺 Health Risk Assessment</div><div class="page-subtitle">Enter a Patient ID to load their profile and generate a health risk evaluation.</div></div>', unsafe_allow_html=True)
        pid = st.text_input("Patient ID", placeholder="e.g.  ID-2621", key="risk_pid")
        if pid:
            row = df[df["Patient ID"] == pid]
            if row.empty:
                st.markdown('<span class="badge badge-err"><span class="badge-dot"></span> Patient ID not found — register via New Patient tab first</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge badge-ok"><span class="badge-dot"></span> Patient record loaded successfully</span>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                age = int(row["Age"].values[0]); condition = row["Medical Condition"].values[0]
                admission = row["Admission Type"].values[0]; test = row["Test Results"].values[0]
                sec_label("PATIENT PROFILE")
                det_grid([("Patient ID", pid), ("Age", f"{age} yrs"), ("Medical Condition", condition), ("Admission Type", admission), ("Test Result", test)])
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Run Risk Assessment  →", key="risk_btn"):
                    X = pd.DataFrame([[age, ENC_CONDITION[condition], ENC_ADMISSION[admission], ENC_TEST[test]]], columns=["Age","Medical Condition","Admission Type","Test Results"])
                    res = risk_model.predict(X)[0]; label = RISK_LABELS[res]; pct = RISK_PCT[label]
                    cls = {"Low":"risk-low","Medium":"risk-med","High":"risk-hi"}[label]
                    col = {"Low":"#0d7a55","Medium":"#b85a00","High":"#c02020"}[label]
                    icon = {"Low":"🟢","Medium":"🟡","High":"🔴"}[label]
                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                    sec_label("ASSESSMENT RESULT")
                    rc1, rc2 = st.columns([1, 1.6])
                    with rc1:
                        st.markdown(f'<div class="res-card {cls}"><div class="res-eyebrow">Health Risk Level</div><div class="res-value" style="color:{col};">{icon} {label}</div><div class="res-confidence">Confidence: {pct}%</div><div class="res-note">Based on age, condition,<br>admission type &amp; test results</div></div>', unsafe_allow_html=True)
                    with rc2:
                        render_prec(label)
                    # ── PDF DOWNLOAD ──
                    st.markdown("<br>", unsafe_allow_html=True)
                    sec_label("DOWNLOAD REPORT")
                    pdf_data = generate_medicore_pdf({
                        "pid": pid, "age": age, "gender": row["Gender"].values[0],
                        "blood": row["Blood Type"].values[0], "condition": condition,
                        "admission": admission, "test": test,
                        "insurance": row["Insurance Provider"].values[0],
                        "admitted": row["Date of Admission"].values[0],
                        "discharged": row["Discharge Date"].values[0],
                        "medication": row["Medication"].values[0] if "Medication" in row.columns else "N/A",
                        "risk_label": label, "risk_pct": pct,
                        "bill_estimate": 0,
                        "precautions": PRECAUTIONS[label]["items"],
                    })
                    st.download_button(
                        label="⬇️  Download Health Risk Report (PDF)",
                        data=pdf_data,
                        file_name=f"MediCore_Risk_Report_{pid}.pdf",
                        mime="application/pdf",
                        width='stretch',
                    )

    # ── BILLING ──
    elif st.session_state.page == "Billing":
        st.markdown('<div class="page-title-area"><div class="page-title">💰 Treatment Billing Estimation</div><div class="page-subtitle">Enter a Patient ID to load their complete profile and generate an estimated treatment cost.</div></div>', unsafe_allow_html=True)
        pid = st.text_input("Patient ID", placeholder="e.g.  ID-2621", key="bill_pid")
        if pid:
            row = df[df["Patient ID"] == pid]
            if row.empty:
                st.markdown('<span class="badge badge-err"><span class="badge-dot"></span> Patient ID not found — register via New Patient tab first</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge badge-ok"><span class="badge-dot"></span> Patient record loaded successfully</span>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                age=int(row["Age"].values[0]); gender=row["Gender"].values[0]; blood=row["Blood Type"].values[0]
                cond=row["Medical Condition"].values[0]; adm=row["Admission Type"].values[0]; ins=row["Insurance Provider"].values[0]
                test=row["Test Results"].values[0]; hosp=row["Hospital"].values[0]; doc=row["Doctor"].values[0]
                adtd=row["Date of Admission"].values[0]; dchd=row["Discharge Date"].values[0]; med=row["Medication"].values[0]
                sec_label("FULL PATIENT DETAILS")
                det_grid([("Patient ID",pid),("Age",f"{age} yrs"),("Gender",gender),("Blood Type",blood),("Condition",cond),("Admission",adm),("Insurance",ins),("Test Result",test),("Hospital",hosp),("Doctor",doc),("Admitted",adtd),("Discharged",dchd),("Medication",med)])
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Calculate Treatment Cost  →", key="billing_btn"):
                    X = pd.DataFrame([[age, encode_gender(gender), ENC_BLOOD[blood], ENC_CONDITION[cond], ENC_ADMISSION[adm], ENC_INSURANCE[ins], ENC_TEST[test]]], columns=["Age","Gender","Blood Type","Medical Condition","Admission Type","Insurance Provider","Test Results"])
                    res = billing_model.predict(X)[0]
                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                    sec_label("BILLING RESULT")
                    bc1, bc2 = st.columns([1, 1.4])
                    with bc1:
                        st.markdown(f'<div class="res-card bill"><div class="res-eyebrow">Estimated Treatment Cost</div><div class="res-value" style="color:#1a50c8;">₹{round(res,2):,}</div><div class="res-confidence">Model Estimate</div><div class="res-note">Based on condition, insurance,<br>and admission type</div></div>', unsafe_allow_html=True)
                    with bc2:
                        st.markdown(f'<div class="form-card"><div class="howto-title" style="margin-bottom:14px;">📊 Cost Breakdown Factors</div><div class="det-grid" style="grid-template-columns:1fr 1fr;"><div class="det-item"><div class="det-lbl">Condition</div><div class="det-val">{cond}</div></div><div class="det-item"><div class="det-lbl">Admission</div><div class="det-val">{adm}</div></div><div class="det-item"><div class="det-lbl">Insurance</div><div class="det-val">{ins}</div></div><div class="det-item"><div class="det-lbl">Test Result</div><div class="det-val">{test}</div></div></div><div style="margin-top:14px;font-size:13px;color:#6b7fa0;padding:10px 14px;background:#f0f5ff;border-radius:8px;border:1px dashed rgba(26,108,240,0.2);">📅 &nbsp;Treatment period: &nbsp;<b>{adtd}</b> &nbsp;→&nbsp; <b>{dchd}</b></div></div>', unsafe_allow_html=True)
                    # ── PDF DOWNLOAD ──
                    st.markdown("<br>", unsafe_allow_html=True)
                    sec_label("DOWNLOAD REPORT")
                    # compute risk for billing report
                    Xr_b = pd.DataFrame([[age, ENC_CONDITION[cond], ENC_ADMISSION[adm], ENC_TEST[test]]],
                                         columns=["Age","Medical Condition","Admission Type","Test Results"])
                    r_for_bill  = risk_model.predict(Xr_b)[0]
                    lbl_for_bill = RISK_LABELS[r_for_bill]
                    pct_for_bill = RISK_PCT[lbl_for_bill]
                    pdf_data_b = generate_medicore_pdf({
                        "pid": pid, "age": age, "gender": gender, "blood": blood,
                        "condition": cond, "admission": adm, "test": test,
                        "insurance": ins, "admitted": adtd, "discharged": dchd,
                        "medication": med,
                        "risk_label": lbl_for_bill, "risk_pct": pct_for_bill,
                        "bill_estimate": res,
                        "precautions": PRECAUTIONS[lbl_for_bill]["items"],
                    })
                    st.download_button(
                        label="⬇️  Download Billing Report (PDF)",
                        data=pdf_data_b,
                        file_name=f"MediCore_Billing_Report_{pid}.pdf",
                        mime="application/pdf",
                        width='stretch',
                    )

    # ── NEW PATIENT ──
    elif st.session_state.page == "NewPatient":
        st.markdown('<div class="page-title-area"><div class="page-title">🆕 New Patient Registration</div><div class="page-subtitle">Fill in patient details to receive an instant risk assessment, treatment cost estimate, and a unique Patient ID.</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        sec_label("PATIENT DEMOGRAPHICS")
        r1a, r1b, r1c = st.columns(3)
        age    = r1a.number_input("Age", min_value=1, max_value=120, value=30, step=1)
        gender = r1b.selectbox("Gender", list(ENC_GENDER.keys()))
        blood  = r1c.selectbox("Blood Type", list(ENC_BLOOD.keys()))
        st.markdown("<br>", unsafe_allow_html=True)
        sec_label("CLINICAL INFORMATION")
        r2a, r2b, r2c = st.columns(3)
        cond = r2a.selectbox("Medical Condition", list(ENC_CONDITION.keys()))
        adm  = r2b.selectbox("Admission Type", list(ENC_ADMISSION.keys()))
        test = r2c.selectbox("Test Results", list(ENC_TEST.keys()))
        st.markdown("<br>", unsafe_allow_html=True)
        sec_label("ADMINISTRATIVE DETAILS")
        r3a, r3b = st.columns(2)
        ins  = r3a.selectbox("Insurance Provider", list(ENC_INSURANCE.keys()))
        adtd = r3b.date_input("Date of Admission")
        r4a, r4b = st.columns(2)
        dchd = r4a.date_input("Discharge Date")
        med  = r4b.text_input("Medication (optional)", placeholder="e.g. Ibuprofen, Metformin")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("✦  Submit & Get Results  →", key="np_btn", width='stretch'):
            Xr = pd.DataFrame([[age, ENC_CONDITION[cond], ENC_ADMISSION[adm], ENC_TEST[test]]], columns=["Age","Medical Condition","Admission Type","Test Results"])
            r_res = risk_model.predict(Xr)[0]; label = RISK_LABELS[r_res]; pct = RISK_PCT[label]
            Xb = pd.DataFrame([[age, encode_gender(gender), ENC_BLOOD[blood], ENC_CONDITION[cond], ENC_ADMISSION[adm], ENC_INSURANCE[ins], ENC_TEST[test]]], columns=["Age","Gender","Blood Type","Medical Condition","Admission Type","Insurance Provider","Test Results"])
            b_res = billing_model.predict(Xb)[0]
            patient_data = {"Age":age,"Gender":gender,"Blood Type":blood,"Medical Condition":cond,"Admission Type":adm,"Test Results":test,"Insurance Provider":ins,"Date of Admission":str(adtd),"Discharge Date":str(dchd),"Medication":med if med else "","Billing Amount":round(b_res,2),"Name":"","Doctor":"","Hospital":"","Room Number":""}
            new_pid, updated_df = save_new_patient(df, DATA_PATH, patient_data)
            st.session_state.df = updated_df; df = updated_df
            cls = {"Low":"risk-low","Medium":"risk-med","High":"risk-hi"}[label]
            col = {"Low":"#0d7a55","Medium":"#b85a00","High":"#c02020"}[label]
            icon = {"Low":"🟢","Medium":"🟡","High":"🔴"}[label]
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="pid-banner"><div><div class="pid-label">✅ Patient Registered Successfully</div><div class="pid-sub">Your unique Patient ID has been generated &amp; saved</div><div class="pid-value">{new_pid}</div></div><div class="pid-hint"><div class="pid-hint-lbl">USE THIS ID IN</div><div class="pid-hint-val">🩺 Risk Check &nbsp;·&nbsp; 💰 Billing</div></div></div>', unsafe_allow_html=True)
            sec_label("ANALYSIS RESULTS")
            res1, res2 = st.columns(2)
            with res1:
                st.markdown(f'<div class="res-card {cls}"><div class="res-eyebrow">Health Risk Level</div><div class="res-value" style="color:{col};">{icon} {label}</div><div class="res-confidence">Confidence: {pct}%</div><div class="res-note">Based on clinical assessment</div></div>', unsafe_allow_html=True)
            with res2:
                st.markdown(f'<div class="res-card bill"><div class="res-eyebrow">Estimated Treatment Cost</div><div class="res-value" style="color:#1a50c8;font-size:38px;">₹{round(b_res,2):,}</div><div class="res-confidence">Cost Estimate</div><div class="res-note">Based on all entered parameters</div></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            sec_label("PERSONALISED HEALTH GUIDANCE")
            render_prec(label)
            st.markdown("<br>", unsafe_allow_html=True)
            sec_label("PATIENT SUMMARY")
            summary_df = pd.DataFrame({"Field":["Patient ID","Age","Gender","Blood Type","Medical Condition","Admission Type","Test Results","Insurance Provider","Admission Date","Discharge Date","Medication","Est. Billing"],"Value":[new_pid,f"{age} yrs",gender,blood,cond,adm,test,ins,str(adtd),str(dchd),med if med else "Not specified",f"₹{round(b_res,2):,}"]})
            st.dataframe(summary_df, hide_index=True, width="stretch")
            # ── PDF DOWNLOAD ──
            st.markdown("<br>", unsafe_allow_html=True)
            sec_label("DOWNLOAD REPORT")
            pdf_np = generate_medicore_pdf({
                "pid": new_pid, "age": age, "gender": gender, "blood": blood,
                "condition": cond, "admission": adm, "test": test,
                "insurance": ins, "admitted": str(adtd), "discharged": str(dchd),
                "medication": med if med else "Not specified",
                "risk_label": label, "risk_pct": pct,
                "bill_estimate": b_res,
                "precautions": PRECAUTIONS[label]["items"],
            })
            st.download_button(
                label="⬇️  Download Full Patient Report (PDF)",
                data=pdf_np,
                file_name=f"MediCore_Report_{new_pid}.pdf",
                mime="application/pdf",
                width='stretch',
            )

    # ── BOOK APPOINTMENT ──
    elif st.session_state.page == "Appointment":
        st.markdown('''<div class="page-title-area">
            <div class="page-title">📅 Doctor Appointment Booking</div>
            <div class="page-subtitle">Enter your Patient ID and select a doctor, date, and time slot to book an appointment.</div>
        </div>''', unsafe_allow_html=True)

        from datetime import date as dt_date, timedelta

        # ── Step 1: Patient ID lookup ──
        pid_appt = st.text_input("Patient ID", placeholder="e.g. ID-2621", key="appt_pid")
        row_appt = df[df["Patient ID"] == pid_appt] if pid_appt else None

        if pid_appt and (row_appt is None or row_appt.empty):
            st.markdown('<span class="badge badge-err"><span class="badge-dot"></span> Patient ID not found</span>', unsafe_allow_html=True)
        elif pid_appt and not row_appt.empty:
            st.markdown('<span class="badge badge-ok"><span class="badge-dot"></span> Patient verified successfully</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            pat_name = row_appt["Name"].values[0] if "Name" in row_appt.columns and str(row_appt["Name"].values[0]).strip() else "Patient"
            pat_cond = row_appt["Medical Condition"].values[0]

            sec_label("BOOK YOUR APPOINTMENT")
            st.markdown('<div class="appt-card">', unsafe_allow_html=True)

            # ── Row 1: Hospital + Department ──
            col_h, col_a = st.columns(2)
            hosp_sel = col_h.selectbox("🏥 Hospital", HOSPITALS, key="appt_hosp")

            # Departments available in selected hospital
            dept_options = sorted(HOSPITAL_DOCTORS.get(hosp_sel, {}).keys())
            if not dept_options:
                dept_options = list(DOCTORS.keys())
            dept_sel = col_a.selectbox("🩺 Department", dept_options, key="appt_dept")

            # ── Row 2: Doctor + Date ──
            col_b, col_c = st.columns(2)
            doc_options = HOSPITAL_DOCTORS.get(hosp_sel, {}).get(dept_sel, [])
            if not doc_options:
                doc_options = DOCTORS.get(dept_sel, ["No doctors available"])
            doctor_sel = col_b.selectbox("👨‍⚕️ Select Doctor", doc_options, key="appt_doc")

            # Show hospital info badge
            st.markdown(f"""
            <div style="background:rgba(26,108,240,0.06);border:1px solid rgba(26,108,240,0.15);
                border-radius:10px;padding:8px 16px;margin:4px 0 8px 0;font-size:12.5px;color:#3a4d6e;">
                🏥 <b>{hosp_sel}</b> &nbsp;·&nbsp; 🩺 <b>{dept_sel}</b> &nbsp;·&nbsp; 👨‍⚕️ <b>{doctor_sel}</b>
            </div>
            """, unsafe_allow_html=True)

            col_d, col_e = st.columns(2)
            min_date  = dt_date.today() + timedelta(days=1)
            max_date  = dt_date.today() + timedelta(days=60)
            appt_date = col_d.date_input("📅 Appointment Date", value=min_date, min_value=min_date, max_value=max_date, key="appt_date")

            # ── Show available vs booked slots ──
            booked_slots = get_booked_slots(doctor_sel, str(appt_date))
            available    = [s for s in TIME_SLOTS if s not in booked_slots]

            if available:
                # Build slot options with availability labels
                slot_options = []
                for s in TIME_SLOTS:
                    if s in booked_slots:
                        slot_options.append(f"{s}  ❌ Booked")
                    else:
                        slot_options.append(f"{s}  ✅ Available")

                slot_display = col_e.selectbox("⏰ Time Slot", slot_options, key="appt_time_display")
                # Extract actual time from selected option
                time_sel = slot_display.split("  ")[0]
                slot_is_free = "✅" in slot_display

                # Show slot availability summary
                st.markdown(f"""
                <div style="background:rgba(240,245,255,0.8);border:1px solid rgba(26,108,240,0.15);
                    border-radius:10px;padding:10px 16px;margin:8px 0;font-size:13px;color:#3a4d6e;">
                    📊 &nbsp;<b>{doctor_sel}</b> on <b>{appt_date}</b> —
                    <span style="color:#0d7a55;font-weight:600;">{len(available)} slots available</span>
                    &nbsp;·&nbsp;
                    <span style="color:#c02020;font-weight:600;">{len(booked_slots)} slots booked</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                col_e.selectbox("⏰ Time Slot", ["No slots available"], key="appt_time_display", disabled=True)
                time_sel     = None
                slot_is_free = False
                st.markdown("""
                <div style="background:#fde4e4;border:1.5px solid #f5a0a0;border-radius:10px;
                    padding:12px 18px;margin:8px 0;font-size:13px;color:#c02020;font-weight:600;">
                    🔴 Dr. {doc} is fully booked on this date. Please choose a different date or doctor.
                </div>
                """.replace("{doc}", doctor_sel), unsafe_allow_html=True)

            reason = st.text_input("Reason for Visit (optional)", placeholder="e.g. Routine checkup, Chest pain, Follow-up...", key="appt_reason")
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            # ── FIX: guard against double booking using session state flag ──
            booking_key = f"booked_{pid_appt}_{doctor_sel}_{appt_date}_{time_sel}"
            already_submitted = st.session_state.get("booking_key_done") == booking_key

            if slot_is_free and not already_submitted:
                if st.button("✦  Confirm Appointment  →", key="appt_confirm_btn", width='stretch'):
                    success = book_appointment(pid_appt, doctor_sel, dept_sel, str(appt_date), time_sel, reason)
                    if success:
                        st.session_state.appt_booked   = True
                        st.session_state.booking_key_done = booking_key
                        st.session_state["last_appt"]  = {
                            "pid": pid_appt, "hospital": hosp_sel,
                            "doctor": doctor_sel, "dept": dept_sel,
                            "date": str(appt_date), "slot": time_sel,
                            "reason": reason or "General Consultation"
                        }
                    else:
                        st.error("⚠️ This slot was just booked by someone else. Please select a different time.")
                    st.rerun()
            elif already_submitted:
                st.success("✅ Appointment already confirmed! Select a new slot to book another.")
            elif not slot_is_free and time_sel:
                st.warning("⚠️ Selected slot is already booked. Please choose an available slot (✅).")

            # ── My Past Appointments ──
            past = get_patient_appointments(pid_appt)
            if not past.empty:
                st.markdown("<br>", unsafe_allow_html=True)
                sec_label("YOUR APPOINTMENTS")
                show_cols = ["appt_date","time_slot","doctor_name","dept","reason","status","booked_on"]
                show_cols = [c for c in show_cols if c in past.columns]
                st.dataframe(past[show_cols].rename(columns={
                    "appt_date":"Date","time_slot":"Time","doctor_name":"Doctor",
                    "dept":"Department","reason":"Reason","status":"Status","booked_on":"Booked On"
                }), hide_index=True, width='stretch')

        # ── Confirmation Banner ──
        if st.session_state.get("appt_booked") and st.session_state.get("last_appt"):
            a = st.session_state["last_appt"]
            st.markdown(f"""
            <div class="appt-confirm">
                <span class="appt-confirm-icon">✅</span>
                <div class="appt-confirm-title">Appointment Confirmed!</div>
                <div class="appt-confirm-sub">Your appointment has been successfully booked and saved.</div>
                <div class="appt-detail-row">
                    <div class="appt-pill"><div class="appt-pill-lbl">Patient ID</div><div class="appt-pill-val">{a["pid"]}</div></div>
                    <div class="appt-pill"><div class="appt-pill-lbl">Hospital</div><div class="appt-pill-val">{a.get("hospital","—")}</div></div>
                    <div class="appt-pill"><div class="appt-pill-lbl">Doctor</div><div class="appt-pill-val">{a["doctor"]}</div></div>
                    <div class="appt-pill"><div class="appt-pill-lbl">Department</div><div class="appt-pill-val">{a["dept"]}</div></div>
                    <div class="appt-pill"><div class="appt-pill-lbl">Date</div><div class="appt-pill-val">{a["date"]}</div></div>
                    <div class="appt-pill"><div class="appt-pill-lbl">Time</div><div class="appt-pill-val">{a["slot"]}</div></div>
                    <div class="appt-pill"><div class="appt-pill-lbl">Reason</div><div class="appt-pill-val">{a["reason"]}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.appt_booked = False

    # ── RENDER CHATBOT ──
    render_chatbot()

    if not st.session_state.chat_open:
        st.markdown("""
        <div class="chat-badge">💬 MediBot · Ask health questions</div>
        <div class="chat-fab-pulse"></div>
        """, unsafe_allow_html=True)
