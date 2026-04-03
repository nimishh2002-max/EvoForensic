import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION (Must be first Streamlit command)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EvoForensic Intelligence System",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# -----------------------------------------------------------------------------
# 2. IMPORTS (Post Page Config)
# -----------------------------------------------------------------------------
import Main
from ui import auth_ui

# -----------------------------------------------------------------------------
# 3. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "auth_mode" not in st.session_state:
    st.session_state["auth_mode"] = False 

# -----------------------------------------------------------------------------
# 4. MASTER ROUTER LOGIC
# -----------------------------------------------------------------------------
if st.session_state["logged_in"]:
    # =========================================================
    # STATE A: USER IS LOGGED IN (Load Main Dashboard)
    # =========================================================
    
    # Inject minimal style to clear the auth neon theme
    st.markdown("""
    <style>
        .stApp {
            background-image: none !important;
            background-color: #ffffff !important; 
            font-family: "Source Sans Pro", sans-serif !important;
        }
        /* Hide auth animations if they persist */
        .dna-container { display: none !important; }
        .glass-card { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    # Run the existing dashboard
    Main.main()
    
    # Render global secure logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("🔒 Secure Logout", type="primary"):
        st.session_state["logged_in"] = False
        st.session_state["auth_mode"] = False
        st.rerun()

else:
    # =========================================================
    # STATE B: USER IS LOGGED OUT (Load Landing / Auth Form)
    # =========================================================
    auth_ui.show_landing_page()