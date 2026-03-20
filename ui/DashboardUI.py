import streamlit as st

def show_dashboard_ui():
    # ---------------------------------------------------------
    # 1. TERROR / CRIME THEME CSS (Bulletproof)
    # ---------------------------------------------------------
    st.markdown("""
    <style>
        /* Force Deep Dark Red/Black App Background */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #030000 !important;
            background-image: radial-gradient(circle at 50% 0%, #1a0000 0%, #030000 100%) !important;
            color: #d9d9d9 !important;
        }
        
        /* Force Sidebar to be Pitch Black with Red Borders */
        [data-testid="stSidebar"], [data-testid="stSidebarHeader"] {
            background-color: #050000 !important;
            border-right: 1px solid rgba(255, 0, 0, 0.3) !important;
        }
        
        /* Sidebar Text & Radio Buttons */
        [data-testid="stSidebar"] * {
            color: #a6a6a6 !important;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label * {
            color: #ff3333 !important;
            font-weight: bold;
            font-family: 'Courier New', monospace !important;
        }
        
        /* 🚨 FIX THE "KEYBOARD ARROW" BUG 🚨
           Forces Streamlit's icons to use their original font, preventing text bleed. */
        .material-symbols-rounded, 
        [data-testid="collapsedControl"] *,
        [data-testid="stSidebarCollapseButton"] * {
            font-family: "Material Symbols Rounded" !important;
            color: #ff3333 !important;
        }

        /* ---------------------------------------------------
           CRIME / TERROR DASHBOARD CUSTOM CSS 
           --------------------------------------------------- */
        
        /* Import a gritty, monospace font */
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

        .terror-dashboard {
            font-family: 'Share Tech Mono', monospace;
            position: relative;
            z-index: 1;
        }

        /* CRT Scanline Overlay Animation */
        .scanlines {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0,0,0,0.2) 50%, rgba(0,0,0,0.2));
            background-size: 100% 4px;
            pointer-events: none;
            z-index: 9999;
            opacity: 0.3;
        }

        /* Glitch Animation for Title */
        .glitch-title {
            color: #ff0000;
            font-size: 3.5rem;
            text-transform: uppercase;
            font-weight: bold;
            text-align: center;
            letter-spacing: 5px;
            text-shadow: 2px 2px 10px rgba(255, 0, 0, 0.7);
            position: relative;
            animation: pulse-red 2s infinite alternate;
            margin-top: 20px;
        }
        
        @keyframes pulse-red {
            0% { text-shadow: 0 0 10px #ff0000, 0 0 20px #8a0000; }
            100% { text-shadow: 0 0 20px #ff0000, 0 0 40px #ff3333, 0 0 60px #8a0000; }
        }

        .classified-banner {
            background-color: #ff0000;
            color: #000;
            text-align: center;
            font-weight: 900;
            padding: 5px;
            letter-spacing: 10px;
            margin-bottom: 30px;
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
            animation: flicker 4s infinite;
        }
        
        @keyframes flicker {
            0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% { opacity: 1; }
            20%, 24%, 55% { opacity: 0.4; }
        }

        .project-desc {
            background: rgba(10, 0, 0, 0.8);
            border-left: 5px solid #ff0000;
            padding: 20px;
            color: #cccccc;
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 40px;
            position: relative;
        }
        .project-desc::before {
            content: "SYSTEM LOG // DIRECTIVE 440";
            position: absolute;
            top: -10px;
            left: 10px;
            background: #030000;
            color: #ff3333;
            font-size: 0.8rem;
            padding: 0 5px;
        }

        /* Interactive "Suspect File" Cards */
        .card-container {
            display: flex;
            gap: 20px;
            justify-content: space-between;
            flex-wrap: wrap;
        }

        .crime-card {
            flex: 1;
            min-width: 250px;
            background: #0a0000;
            border: 1px solid #330000;
            border-top: 4px solid #4a0000;
            padding: 25px;
            border-radius: 4px;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }
        
        .crime-card::before {
            content: '';
            position: absolute;
            top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 0, 0, 0.1), transparent);
            transition: all 0.5s ease;
        }

        .crime-card:hover {
            border-color: #ff0000;
            border-top: 4px solid #ff0000;
            box-shadow: 0 10px 30px rgba(255, 0, 0, 0.3), inset 0 0 20px rgba(255, 0, 0, 0.1);
            transform: translateY(-10px);
        }
        
        .crime-card:hover::before {
            left: 100%;
        }

        .card-icon {
            font-size: 3rem;
            margin-bottom: 15px;
            filter: drop-shadow(0 0 5px red);
        }

        .card-title {
            color: #ffffff;
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 10px;
            border-bottom: 1px dashed #4a0000;
            padding-bottom: 10px;
        }

        .card-text {
            color: #a6a6a6;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        
        /* Animated SVG Graphic */
        .radar-container {
            text-align: center;
            margin-top: 40px;
            opacity: 0.7;
        }
        
        .spinning-radar {
            animation: spin 10s linear infinite;
            filter: drop-shadow(0 0 10px red);
        }
        
        @keyframes spin { 100% { transform: rotate(360deg); } }

    </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 2. HTML DASHBOARD INJECTION (Strictly Zero Indentation)
    # ---------------------------------------------------------
    st.markdown('<div class="scanlines"></div>', unsafe_allow_html=True)
    
    # DO NOT ADD SPACES TO THE BEGINNING OF THE LINES BELOW!
    # Streamlit will interpret spaces as Markdown code blocks.
    html_dashboard = """
<div class="terror-dashboard">
<div class="classified-banner">TOP SECRET // CLASSIFIED CLEARANCE REQUIRED</div>
<h1 class="glitch-title">EVO-FORENSIC DIRECTIVE</h1>
<br>
<div class="project-desc">
<strong>WARNING:</strong> You are accessing a highly sensitive law enforcement database.<br><br>
The <strong>Evo-Forensic Intelligence Suite</strong> is a next-generation investigative engine designed to dismantle sophisticated criminal syndicates. 
By integrating locally-hosted Large Language Models (LLMs), Biometric Facial Vectoring, and Graph-RAG (Retrieval-Augmented Generation) technology, 
this system autonomously bridges the gap between physical suspect media and their digital cyber-footprint.
<br><br>
<span style="color: #ff3333; font-weight: bold;">[ STATUS: 3 MODULES ONLINE. WAITING FOR DIRECTIVE... ]</span>
</div>
<div class="card-container">
<div class="crime-card">
<div class="card-icon">🩸</div>
<div class="card-title">FORENSIC MODE</div>
<div class="card-text">
<strong>BIO-EVIDENCE SCANNER</strong><br>
Upload degraded CCTV or suspect photographs. The system extracts 512-dimensional facial geometry, cross-references cold-case databases using Cosine Distance, and generates an interactive web of known criminal associates.
</div>
</div>
<div class="crime-card">
<div class="card-icon">🗄️</div>
<div class="card-title">RESEARCH MODE</div>
<div class="card-text">
<strong>DOSSIER INTERROGATION</strong><br>
Feed unstructured case files, bank records, and threat intel into the local ChromaDB vector space. Interrogate the evidence using Llama-3 to instantly pull hidden motives, timelines, and suspect connections.
</div>
</div>
<div class="crime-card">
<div class="card-icon">🌐</div>
<div class="card-title">CYBER TIMELINE</div>
<div class="card-text">
<strong>ATTACK SEQUENCE</strong><br>
Correlate server breach logs, dark-web chatter, and VPN exit nodes. This module rebuilds the exact chronological timeline of a cyber-attack to trace the perpetrator back to their physical location.
</div>
</div>
</div>
<div class="radar-container">
<svg class="spinning-radar" width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
<circle cx="50" cy="50" r="45" stroke="#ff0000" stroke-width="2" fill="none" stroke-dasharray="10 5" />
<circle cx="50" cy="50" r="30" stroke="#8a0000" stroke-width="1" fill="none" />
<circle cx="50" cy="50" r="15" stroke="#ff3333" stroke-width="2" fill="none" />
<line x1="50" y1="5" x2="50" y2="95" stroke="#ff0000" stroke-width="1" opacity="0.5"/>
<line x1="5" y1="50" x2="95" y2="50" stroke="#ff0000" stroke-width="1" opacity="0.5"/>
</svg>
<div style="color: #ff0000; font-size: 0.8rem; margin-top: 10px; letter-spacing: 2px; animation: flicker 2s infinite;">AWAITING UPLOAD...</div>
</div>
</div>
"""
    
    st.markdown(html_dashboard, unsafe_allow_html=True)