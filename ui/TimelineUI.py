import streamlit as st
import sys
import os
import time

# ---------------------------------------------------------
# 1. IMPORT LOGIC FROM MODULES
# ---------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from modules.DigitalTimelineMode import analyze_timeline_logs
except ImportError:
    st.error("⚠️ Logic Module Missing. Ensure 'modules/DigitalTimelineMode.py' exists.")
    st.stop()

# ---------------------------------------------------------
# 2. CYBER-BLOOD THEME (CSS/JS)
# ---------------------------------------------------------
def inject_cyber_blood_theme():
    st.markdown("""
    <!-- TAILWIND CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <style>
        /* 1. DARK BACKGROUND */
        .stApp {
            background-color: #050505;
            background-image: 
                radial-gradient(circle at 50% 50%, rgba(50, 0, 0, 0.2), transparent 80%),
                linear-gradient(0deg, #000000 0%, #1a0505 100%);
            color: #e5e5e5;
        }

        /* 2. BLOOD SPRAY ANIMATION */
        .blood-particle {
            position: fixed;
            background: radial-gradient(circle, #8b0000 0%, #500000 100%);
            border-radius: 50%;
            opacity: 0.8;
            pointer-events: none;
            filter: blur(1px);
            animation: drip 8s infinite ease-in;
            z-index: 0;
        }
        
        .blood-splatter {
            position: fixed;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(139, 0, 0, 0.15) 0%, transparent 60%);
            filter: blur(20px);
            animation: pulse-red 5s infinite ease-in-out;
            pointer-events: none;
            z-index: 0;
        }

        @keyframes drip {
            0% { transform: translateY(-10vh) scale(1); opacity: 0; }
            20% { opacity: 0.8; }
            80% { opacity: 0.6; }
            100% { transform: translateY(110vh) scale(1.5); opacity: 0; }
        }
        
        @keyframes pulse-red {
            0%, 100% { transform: scale(1); opacity: 0.3; }
            50% { transform: scale(1.2); opacity: 0.6; }
        }

        /* 3. TERMINAL INPUT STYLE */
        .stTextArea textarea {
            background-color: #0a0a0a !important;
            color: #ff4444 !important;
            border: 1px solid #330000 !important;
            font-family: 'Courier New', monospace;
            box-shadow: 0 0 10px rgba(139, 0, 0, 0.2);
        }
        
        .stTextArea textarea:focus {
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.4);
            border-color: #ff0000 !important;
        }

        /* 4. BEAUTIFUL RED BUTTON */
        .stButton>button {
            background: linear-gradient(145deg, #8b0000, #b91c1c);
            color: white !important;
            border: 1px solid #ff0000;
            border-radius: 4px;
            padding: 12px 28px;
            font-family: 'Courier New', monospace;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 2px;
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stButton>button:hover {
            background: #ff0000;
            box-shadow: 0 0 30px rgba(255, 0, 0, 0.8), inset 0 0 10px white;
            text-shadow: 0 0 5px white;
            transform: translateY(-2px);
        }

        /* 5. TYPOGRAPHY & OUTPUT */
        h1, h2, h3 {
            color: #ff0000 !important;
            text-shadow: 0 0 10px rgba(139, 0, 0, 0.8);
            font-family: 'Impact', sans-serif;
            letter-spacing: 1px;
        }
        
        .report-box {
            background: rgba(0, 0, 0, 0.8);
            border-left: 4px solid #ff0000;
            padding: 20px;
            font-family: 'Courier New', monospace;
            color: #ffcccc;
            box-shadow: inset 0 0 20px rgba(50, 0, 0, 0.5);
            margin-top: 20px;
            border-radius: 0 10px 10px 0;
            /* Removed white-space: pre-wrap to allow Markdown tables to render */
        }
        
        /* Custom Labels */
        label {
            color: #ff4444 !important;
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }
    </style>
    
    <!-- BLOOD SPRAY ANIMATION -->
    <div class="blood-splatter" style="top: -50px; left: -50px;"></div>
    <div class="blood-splatter" style="bottom: -50px; right: -50px; animation-delay: 2s;"></div>
    
    <div class="blood-particle" style="left: 10%; width: 5px; height: 15px; animation-duration: 4s;"></div>
    <div class="blood-particle" style="left: 30%; width: 8px; height: 25px; animation-duration: 6s; animation-delay: 1s;"></div>
    <div class="blood-particle" style="left: 50%; width: 4px; height: 12px; animation-duration: 5s; animation-delay: 3s;"></div>
    <div class="blood-particle" style="left: 70%; width: 6px; height: 20px; animation-duration: 7s; animation-delay: 0.5s;"></div>
    <div class="blood-particle" style="left: 90%; width: 5px; height: 18px; animation-duration: 4.5s; animation-delay: 2s;"></div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. MAIN UI FUNCTION
# ---------------------------------------------------------
def show_timeline_ui():
    inject_cyber_blood_theme()
    
    st.markdown("""
    <div style="text-align:center; margin-bottom: 30px; padding-top: 20px;">
        <h1 style="font-size: 3.5rem; margin-bottom: 5px;">🩸 DIGITAL AUTOPSY</h1>
        <p style="color: #ff4444; font-family: 'Courier New', monospace; letter-spacing: 2px;">CYBER-FORENSIC TIMELINE RECONSTRUCTION</p>
    </div>
    """, unsafe_allow_html=True)

    # Layout: Input on left, Info on right
    col_main, col_info = st.columns([3, 1])

    with col_main:
        st.markdown("### 📥 INGEST SERVER LOGS")
        log_input = st.text_area(
            "Paste Raw Logs / Firewall Data:", 
            height=250, 
            placeholder="[2024-10-15 03:12:01] SSH Failed login from 192.168.1.5...",
            label_visibility="collapsed"
        )
        
        # Centered Action Button
        analyze_btn = st.button("🩸 INITIATE FORENSIC RECONSTRUCTION", use_container_width=True)

    with col_info:
        st.markdown("""
        <div style="background: #1a0505; border: 1px solid #500000; padding: 15px; border-radius: 5px; color: #ff8888; font-family: monospace; font-size: 0.8rem;">
            <strong style="color:red">MODE:</strong> STRICT<br>
            <strong style="color:red">SCAN:</strong> DEEP<br>
            <strong style="color:red">STATUS:</strong> WAITING<br><br>
            Analyzes raw logs to detect IP addresses, timestamps, and attack vectors.
        </div>
        """, unsafe_allow_html=True)

    # Analysis & Output
    if analyze_btn:
        if not log_input.strip():
            st.error("⚠️ NO DATA DETECTED. PLEASE INGEST LOGS.")
        else:
            st.markdown("### 💀 FORENSIC TIMELINE REPORT")
            report_container = st.empty()
            
            try:
                # Call Logic from Module (Streaming)
                stream = analyze_timeline_logs(log_input)
                
                # Streaming Loop
                for full_text in stream:
                    # FIX: Use safe string concatenation + explicit newlines for Markdown
                    # Avoids f-string brace errors with logs (e.g. JSON {})
                    # Newlines ensure content is parsed as Markdown inside the div
                    html_content = '<div class="report-box">\n\n' + full_text + '\n\n</div>'
                    report_container.markdown(html_content, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"SYSTEM FAILURE: {e}")


    