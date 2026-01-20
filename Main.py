import streamlit as st

# Import the independent operation modes
from modules import ForensicMode, ResearchMode, DigitalTimelineMode

def main():
    st.sidebar.title("🧬 Sherlock-AI")
    st.sidebar.caption("Forensic Intelligence Suite")
    st.sidebar.markdown("---")
    
    # NAVIGATION HUB
    # 1. Added "Dashboard" as the default (first) option
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
    st.sidebar.info(
        "**System Status:** 🟢 ONLINE\n\n"
        "**Encryption:** AES-256 Ready\n\n"
        "**AI Model:** Llama 3.2 (Local)"
    )
    
    # ROUTING LOGIC
    if "Dashboard" in mode:
        st.markdown("# 🕵️‍♂️ Sherlock-AI Dashboard")
        st.markdown("""
        ### Welcome, Investigator.
        
        You have successfully authenticated into the secure Forensic Intelligence System.
        
        **Select a module from the sidebar to begin:**
        
        * **🧬 Forensic Mode:** Analyze DNA sequences and decrypt physical evidence.
        * **📄 Research Mode:** Process case files (PDFs) using RAG AI.
        * **🕰️ Digital Timeline:** Correlate server logs and cyber events.
        """)
        
    elif "Forensic" in mode:
        ForensicMode.show_forensic_mode()
    elif "Research" in mode:
        ResearchMode.show_research_mode()
    elif "Digital Timeline" in mode:
        DigitalTimelineMode.show_timeline_mode()

# Note: No 'if __name__ == "__main__":' needed. 
# This is called by ui.py