import streamlit as st
import sys
import os

# --- PATH SETUP ---
# Ensures we can import from 'ui' and 'modules'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- IMPORT NEW UI MODULES ---
try:
    # We now import DashboardUI alongside the others
    from ui import DashboardUI, ForensicUI, ResearchUI, TimelineUI
except ImportError as e:
    st.error(f"CRITICAL ERROR: UI Modules Missing. Please check your 'ui/' folder. Details: {e}")
    st.stop()

def main():
    # --- SIDEBAR SETUP ---
    st.sidebar.title("🧬 EvoForensic")
    st.sidebar.caption("Forensic Intelligence Suite")
    st.sidebar.markdown("---")
    
    # NAVIGATION
    mode = st.sidebar.radio(
        "Select Module:", 
        [
            "🏠 Dashboard",
            "🧬 Forensic Mode (Bio-Evidence)", 
            "📄 Research Mode (Document Intel)", 
            "🕰️ Digital Timeline (Cyber Logs)"
        ]
    )
    
    st.sidebar.markdown("---")
   
    # --- ROUTING LOGIC ---
    if "Dashboard" in mode:
        # Launches the terrifying Crime Dashboard
        DashboardUI.show_dashboard_ui()
        
    elif "Forensic" in mode:
        # Launches Pink/Cyan Glass UI
        ForensicUI.show_forensic_ui()
        
    elif "Research" in mode:
        # Launches Terror/Hacking UI
        ResearchUI.show_research_ui()
        
    elif "Digital Timeline" in mode:
        # Launches Cyber/Blood UI
        TimelineUI.show_timeline_ui()

if __name__ == "__main__":
    main()