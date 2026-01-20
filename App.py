import streamlit as st
import sqlite3
import time

# --- IMPORT YOUR MAIN PROJECT ---
import Main

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sherlock-AI Forensic System",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# -----------------------------------------------------------------------------
# 2. DATABASE LOGIC
# -----------------------------------------------------------------------------
DB_PATH = "data/forensic.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            full_name TEXT,
            badge_id TEXT,
            department TEXT,
            location TEXT,
            official_email TEXT,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == password:
        return True
    return False

def register_user(username, password, full_name, badge_id, department, location, official_email, phone):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO users 
            (username, password, full_name, badge_id, department, location, official_email, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, password, full_name, badge_id, department, location, official_email, phone))
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists."

# -----------------------------------------------------------------------------
# 3. SESSION STATE
# -----------------------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "auth_mode" not in st.session_state:
    st.session_state["auth_mode"] = False 

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE LOGIC
# -----------------------------------------------------------------------------
def main_interface():
    init_db()

    # =========================================================
    # STATE A: USER IS LOGGED IN (NORMAL WHITE MODE)
    # =========================================================
    if st.session_state["logged_in"]:
        # We inject a minimal style to RESET the fancy background back to white
        st.markdown("""
        <style>
            /* FORCE STANDARD WHITE BACKGROUND */
            .stApp {
                background-image: none !important;
                background-color: #ffffff !important; 
                font-family: "Source Sans Pro", sans-serif !important;
            }
            
            /* HIDE FANCY ELEMENTS IF THEY PERSIST */
            .dna-container { display: none !important; }
            .glass-card { display: none !important; }
        </style>
        """, unsafe_allow_html=True)

        # RUN THE MAIN APP (Standard Look)
        Main.main()
        
        # Logout Button
        st.sidebar.markdown("---")
        if st.sidebar.button("🔒 Secure Logout"):
            st.session_state["logged_in"] = False
            st.session_state["auth_mode"] = False
            st.rerun()
            
        return

    # =========================================================
    # STATE B: USER IS LOGGED OUT (FANCY NEON MODE)
    # =========================================================
    
    # 1. Inject FANCY CSS (Only visible here)
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
        
        .stApp {
            background-color: #050005;
            background-image: 
                radial-gradient(circle at 50% 50%, rgba(255, 0, 127, 0.1), transparent 60%),
                linear-gradient(0deg, rgba(0,0,0,0.9) 0%, rgba(20,0,10,0.8) 100%);
            background-attachment: fixed;
            font-family: 'Rajdhani', sans-serif;
        }
        
        /* NEON BUTTONS FOR LANDING PAGE */
        div.stButton > button {
            background: transparent !important; color: white !important;
            border: 2px solid #ff007f !important; padding: 10px 25px !important;
            font-family: 'Orbitron', sans-serif !important; border-radius: 50px !important;
            transition: all 0.3s ease !important; text-transform: uppercase; letter-spacing: 2px;
        }
        div.stButton > button:hover {
            background: #ff007f !important; box-shadow: 0 0 20px #ff007f !important; transform: scale(1.05);
        }

        .dna-container {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 300px; height: 600px; perspective: 1000px; z-index: 0; opacity: 0.5; pointer-events: none;
        }
        .dna-rotator {
            width: 100%; height: 100%; transform-style: preserve-3d; animation: rotateDNA 20s linear infinite;
        }
        .base-pair {
            position: absolute; left: 50%; width: 200px; height: 2px;
            background: linear-gradient(90deg, rgba(255,0,127,0) 0%, rgba(255,0,127,0.8) 50%, rgba(0,255,255,0) 100%);
            margin-left: -100px;
        }
        .base-pair::before, .base-pair::after {
            content: ''; position: absolute; width: 10px; height: 10px; border-radius: 50%; top: -4px;
        }
        .base-pair::before { left: 0; background: #00e5ff; box-shadow: 0 0 10px #00e5ff; }
        .base-pair::after { right: 0; background: #ff007f; box-shadow: 0 0 10px #ff007f; }
        
        @keyframes rotateDNA { 0% { transform: rotateY(0deg); } 100% { transform: rotateY(360deg); } }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 0, 127, 0.2); padding: 40px; border-radius: 15px;
            text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        /* IMPROVE LABEL VISIBILITY */
        .stTextInput label {
            color: #00e5ff !important;
            font-family: 'Rajdhani', sans-serif !important;
            font-weight: bold;
            font-size: 1.1rem;
            text-shadow: 0 0 5px rgba(0, 229, 255, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)

    # 2. Render DNA Animation (Procedural HTML)
    dna_strands = ""
    for i in range(30):
        rotation = i * 15
        top_pos = i * 20
        style = f"top: {top_pos}px; transform: rotateY({rotation}deg) translateZ(0px);"
        dna_strands += f'<div class="base-pair" style="{style}"></div>'
    st.markdown(f'<div class="dna-container"><div class="dna-rotator">{dna_strands}</div></div>', unsafe_allow_html=True)

    # 3. Render Landing/Auth UI
    c1, c2, c3 = st.columns([1, 8, 2])
    with c1:
        st.markdown("<div style='font-family:Orbitron; font-size:24px; color:white; padding-top:10px;'>🧬 EVO<span style='color:#ff007f'>FORENSIC</span></div>", unsafe_allow_html=True)
    with c3:
        if not st.session_state["auth_mode"]:
            if st.button("ACCESS SYSTEM"):
                st.session_state["auth_mode"] = True
                st.rerun()
        else:
            if st.button("⬅ BACK"):
                st.session_state["auth_mode"] = False
                st.rerun()

    st.write(""); st.write("")

    if not st.session_state["auth_mode"]:
        # LANDING MODE
        m1, m2, m3 = st.columns([1, 6, 1])
        with m2:
            st.markdown("""
                <div style="text-align: center; margin-top: 100px;">
                    <h1 style="font-family: 'Orbitron'; font-size: 4rem; margin-bottom: 0; text-shadow: 0 0 20px #ff007f;">FORENSIC INTELLIGENCE</h1>
                    <p style="font-family: 'Rajdhani'; font-size: 1.5rem; color: #00e5ff; letter-spacing: 3px;">ADVANCED BIO-DIGITAL ANALYSIS SUITE</p>
                </div>
            """, unsafe_allow_html=True)
            st.write(""); st.write("")
            k1, k2, k3 = st.columns(3)
            card_style = "background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; text-align:center; border:1px solid #333;"
            with k1: st.markdown(f"<div style='{card_style}'><h3 style='color:#00e5ff; margin:0'>DATABASE</h3><small>SECURE</small></div>", unsafe_allow_html=True)
            with k2: st.markdown(f"<div style='{card_style}'><h3 style='color:#ff007f; margin:0'>AI MODEL</h3><small>ONLINE</small></div>", unsafe_allow_html=True)
            with k3: st.markdown(f"<div style='{card_style}'><h3 style='color:#00e5ff; margin:0'>NETWORK</h3><small>ENCRYPTED</small></div>", unsafe_allow_html=True)

    else:
        # LOGIN FORM MODE
        l1, l2, l3 = st.columns([1, 2, 1])
        with l2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["INVESTIGATOR LOGIN", "REGISTER NEW"])
            
            with tab1:
                u = st.text_input("BADGE ID / USERNAME", key="user")
                p = st.text_input("PASSWORD", type="password", key="pass")
                if st.button("AUTHENTICATE", use_container_width=True):
                    if login_user(u, p):
                        st.success("IDENTITY VERIFIED.")
                        st.session_state["logged_in"] = True
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("ACCESS DENIED.")
            
            with tab2:
                # --- REGISTRATION ---
                c_reg1, c_reg2 = st.columns(2)
                
                with c_reg1:
                    fn = st.text_input("FULL NAME", key="fn")
                    badge = st.text_input("BADGE ID", key="badge")
                    dept = st.text_input("DEPARTMENT", key="dept")
                    
                with c_reg2:
                    email = st.text_input("OFFICIAL EMAIL", key="email")
                    phone = st.text_input("PHONE NUMBER", key="phone")
                    loc = st.text_input("LOCATION", key="loc")

                st.divider()
                
                c_creds1, c_creds2 = st.columns(2)
                with c_creds1:
                    nu = st.text_input("CREATE USERNAME", key="nu")
                    np = st.text_input("CREATE PASSWORD", type="password", key="np")
                with c_creds2:
                    cp = st.text_input("CONFIRM PASSWORD", type="password", key="cp")
                    ac = st.text_input("CLEARANCE CODE", type="password", key="ac") 

                if st.button("SUBMIT OFFICIAL RECORD", use_container_width=True):
                    allowed_domains = ["gov.in", "nic.in", "police.in", "forensicslab.gov", "gmail.com"] 
                    valid_email = any(email.endswith(domain) for domain in allowed_domains)

                    if not fn or not badge or not dept:
                         st.error("ALL IDENTITY FIELDS REQUIRED.")
                    elif not valid_email:
                         st.error("INVALID EMAIL DOMAIN (GOV/POLICE ONLY).")
                    elif ac != "EVOFOR2025":
                        st.error("INVALID CLEARANCE CODE.")
                    elif np != cp:
                        st.error("PASSWORDS DO NOT MATCH.")
                    else:
                        ok, msg = register_user(nu, np, fn, badge, dept, loc, email, phone)
                        if ok: 
                            st.success("RECORD CREATED. PLEASE LOGIN.")
                        else: 
                            st.error(msg)
                        
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main_interface()