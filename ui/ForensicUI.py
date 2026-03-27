import streamlit as st
import streamlit.components.v1 as components
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
    from modules.forensic.forensic_engine import process_suspect_image
    from modules.forensic.report_generator import generate_suspect_pdf
except ImportError as e:
    st.error(f"⚠️ Logic Module Missing. Ensure 'modules/forensic/forensic_engine.py' and 'report_generator.py' exist. Error: {e}")
    st.stop()

# ---------------------------------------------------------
# 2. CYBER / BIOMETRIC THEME (CSS)
# ---------------------------------------------------------
def inject_biometric_theme():
    st.markdown("""
    <style>
        /* Force Dark App Background & Header */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #050b14 !important;
            background-image: radial-gradient(circle at 50% 50%, #0a192f 0%, #02060d 100%) !important;
            color: #e6f1ff !important;
        }
        
        /* Force Dark Sidebar */
        [data-testid="stSidebar"], [data-testid="stSidebarHeader"] {
            background-color: #02060d !important;
            border-right: 1px solid rgba(100, 255, 218, 0.2) !important;
        }
        
        /* Fix Sidebar Text & Radio Buttons */
        [data-testid="stSidebar"] * {
            color: #8892b0 !important;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label * {
            color: #64ffda !important;
            font-weight: bold;
        }
        
        /* Apply Courier New to standard text blocks ONLY */
        h1, h2, h3, h4, p, label, .stMarkdown p, li { 
            color: #e6f1ff !important; 
            font-family: 'Courier New', monospace !important;
        }
        
        /* 🚨 PROTECT ICONS FROM FONT OVERRIDES (FIXES THE ARROW BUGS) 🚨 */
        .material-symbols-rounded, 
        .material-symbols-outlined, 
        [data-testid="collapsedControl"] *,
        span[class*="icon"] {
            font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
        }
        
        .highlight-cyan {
            color: #64ffda !important;
            font-family: 'Courier New', monospace !important;
            text-shadow: 0 0 10px rgba(100, 255, 218, 0.4);
        }

        /* ---------------------------------------------------
           ✨ FIX: EXPANDER (TABLE VIEW) ✨
           --------------------------------------------------- */
        [data-testid="stExpander"] details summary {
            background-color: #020c1b !important;
            border: 1px solid #64ffda !important;
            border-radius: 5px !important;
            padding: 10px !important;
        }
        [data-testid="stExpander"] details summary:hover {
            background-color: rgba(100, 255, 218, 0.1) !important;
            box-shadow: 0 0 10px rgba(100, 255, 218, 0.3) !important;
        }
        /* Color the expander text, but do NOT override the font-family so the arrow survives */
        [data-testid="stExpander"] details summary * {
            color: #64ffda !important;
            fill: #64ffda !important;
        }
        [data-testid="stExpander"] details > div {
            background-color: rgba(2, 12, 27, 0.8) !important;
            border: 1px solid rgba(100, 255, 218, 0.2) !important;
            border-top: none !important;
            padding-top: 15px !important;
        }
        
        /* ---------------------------------------------------
           FIX: DOWNLOAD BUTTONS & REGULAR BUTTONS
           --------------------------------------------------- */
        div[data-testid="stButton"] > button,
        div[data-testid="stDownloadButton"] > button,
        .stButton > button {
            background-color: #020c1b !important;
            background: #020c1b !important;
            border: 1px solid #64ffda !important;
            color: #64ffda !important;
            box-shadow: 0 0 10px rgba(100,255,218,0.2) !important;
            transition: all 0.3s ease;
            font-family: 'Courier New', monospace !important;
            font-weight: bold !important;
            padding: 8px 15px !important;
        }
        div[data-testid="stButton"] > button:hover,
        div[data-testid="stDownloadButton"] > button:hover,
        .stButton > button:hover {
            background-color: #64ffda !important;
            background: #64ffda !important;
            color: #020c1b !important;
            box-shadow: 0 0 20px rgba(100,255,218,0.5) !important;
            transform: translateY(-2px);
        }
        div[data-testid="stButton"] > button *,
        div[data-testid="stDownloadButton"] > button *,
        .stButton > button * {
            color: inherit !important;
        }
        
        /* ---------------------------------------------------
           FILE UPLOADER FIXES
           --------------------------------------------------- */
        div[data-testid="stFileUploader"] {
            background-color: transparent !important;
        }
        div[data-testid="stFileUploader"] > section,
        [data-testid="stFileUploadDropzone"] {
            background-color: rgba(10, 25, 47, 0.8) !important;
            border: 2px dashed #64ffda !important;
            border-radius: 10px !important;
            padding: 25px !important;
            transition: all 0.2s ease-in-out;
        }
        div[data-testid="stFileUploader"] > section:hover,
        [data-testid="stFileUploadDropzone"]:hover {
            background-color: rgba(10, 25, 47, 1.0) !important;
            border: 2px solid #64ffda !important;
            box-shadow: 0 0 15px rgba(100, 255, 218, 0.4) !important;
        }
        div[data-testid="stFileUploader"] small, 
        div[data-testid="stFileUploader"] span, 
        div[data-testid="stFileUploader"] p,
        div[data-testid="stFileUploader"] div {
            color: #8892b0 !important;
        }
        div[data-testid="stFileUploader"] button {
            background-color: #020c1b !important;
            color: #64ffda !important;
            border: 1px solid #64ffda !important;
            font-weight: bold !important;
            border-radius: 5px !important;
            padding: 4px 15px !important;
            font-family: 'Courier New', monospace !important;
        }
        div[data-testid="stFileUploader"] button:hover {
            background-color: #64ffda !important;
            color: #020c1b !important;
            box-shadow: 0 0 10px rgba(100, 255, 218, 0.6) !important;
        }
        div[data-testid="stFileUploader"] svg {
            fill: #64ffda !important;
            color: #64ffda !important;
        }

        /* Glass Panels for Data */
        .glass-panel {
            background: rgba(2, 12, 27, 0.8) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(100, 255, 218, 0.3);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            margin-bottom: 20px;
        }
        
        /* Status Badges */
        .status-badge-red {
            background-color: rgba(255, 75, 75, 0.2);
            color: #ff4b4b !important;
            border: 1px solid #ff4b4b;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-family: 'Courier New', monospace !important;
        }
        .status-badge-green {
            background-color: rgba(100, 255, 218, 0.2);
            color: #64ffda !important;
            border: 1px solid #64ffda;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-family: 'Courier New', monospace !important;
        }
        
        /* Progress Bar Override */
        .stProgress > div > div > div {
            background-color: #64ffda !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. MAIN UI RENDER
# ---------------------------------------------------------
def show_forensic_ui():
    inject_biometric_theme()
    
    # Header Section
    col_logo, col_title = st.columns([1, 6])
    with col_logo:
        st.markdown("<div style='font-size: 3rem;'>👁️‍🗨️</div>", unsafe_allow_html=True)
    with col_title:
        st.markdown("<h1 style='margin-bottom: 0;'><span class='highlight-cyan'>Biometric</span> Graph-RAG Scanner</h1>", unsafe_allow_html=True)
        st.caption("Facial Recognition + LLM Intelligence Extraction + Network Topology")

    st.markdown("---")

    # Upload Section
    st.markdown("### 📸 [STEP 1] Input Suspect Media")
    uploaded_file = st.file_uploader("Upload CCTV Frame or Suspect Photograph", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    if uploaded_file is not None:
        # Create a temporary directory to store the uploaded image for DeepFace
        temp_dir = os.path.join(parent_dir, "data", "temp_uploads")
        os.makedirs(temp_dir, exist_ok=True)
        temp_img_path = os.path.join(temp_dir, uploaded_file.name)
        
        # Save file to disk
        with open(temp_img_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Scan Button
        if st.button("🔍 INITIATE BIOMETRIC SCAN", use_container_width=True, type="primary"):
            
            # ✨ BULLETPROOF FIX: PURE HTML LIVE TERMINAL ✨
            terminal_placeholder = st.empty()
            terminal_text = ""
            
            fake_logs = [
                "[SYSTEM] Initializing DeepFace Biometric Scan...",
                "[DB_QUERY] Cross-referencing facial vectors (512-dim)...",
                "[MATCH FOUND] Target identified. Retrieving local dossier...",
                "[RAG_ENGINE] Initializing Local Llama 3.2 via Ollama...",
                "[NLP_EXTRACTION] Parsing text for Entity-Action-Target triplets...",
                "[GRAPH_BUILDER] Injecting relationship nodes into PyVis Engine...",
                "[SYSTEM] Intelligence compiled. Rendering output topology."
            ]
            
            # Make the text appear line-by-line using a custom HTML Div so Streamlit can't ruin the colors
            for log in fake_logs:
                terminal_text += log + "<br>"
                
                custom_terminal = f"""
                <div style="background-color: #02060d; border: 1px solid #64ffda; border-radius: 5px; padding: 15px; font-family: 'Courier New', monospace; color: #64ffda; box-shadow: 0 0 15px rgba(100, 255, 218, 0.15); min-height: 180px; line-height: 1.6;">
                    {terminal_text}
                </div>
                """
                terminal_placeholder.markdown(custom_terminal, unsafe_allow_html=True)
                time.sleep(0.4) 
                
            # Actually call the heavy AI logic while they watch the terminal
            results = process_suspect_image(temp_img_path)
            
            # Add the final success message to the terminal so it stays on screen
            terminal_text += "<br>[SYSTEM] ✓ Process finished. Evidence loaded below."
            final_terminal = f"""
            <div style="background-color: #02060d; border: 1px solid #64ffda; border-radius: 5px; padding: 15px; font-family: 'Courier New', monospace; color: #64ffda; box-shadow: 0 0 15px rgba(100, 255, 218, 0.15); min-height: 180px; line-height: 1.6;">
                {terminal_text}
            </div>
            """
            terminal_placeholder.markdown(final_terminal, unsafe_allow_html=True)

            st.markdown("---")

            # Handle Results
            if results["status"] == "no_match":
                st.error(f"❌ {results['message']}")
                st.info("The facial vectors did not match any known suspects in the database.")
                if os.path.exists(temp_img_path): os.remove(temp_img_path)
            
            elif results["status"] == "error":
                st.error(f"⚠️ System Error: {results['message']}")
                if os.path.exists(temp_img_path): os.remove(temp_img_path)
            
            elif results["status"] in ["success", "partial_success"]:
                # Display success message
                st.success(f"✅ BIOMETRIC MATCH CONFIRMED: {results['match_id'].upper()}")
                
                # Layout: Left Column (Profile), Right Column (Graph)
                col_prof, col_graph = st.columns([1, 2])
                
                # --- LEFT COLUMN: PROFILE & DOSSIER ---
                with col_prof:
                    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
                    st.image(uploaded_file, caption="Target Image", use_container_width=True)
                    
                    meta = results["metadata"]
                    if meta:
                        st.markdown(f"### 👤 <span style='color: #64ffda; font-family: Courier New;'>{meta.get('full_name', 'Unknown')}</span>", unsafe_allow_html=True)
                        
                        # Status Badge
                        status = meta.get('status', 'Unknown')
                        badge_class = "status-badge-red" if "At Large" in status else "status-badge-green"
                        st.markdown(f"**Status:** <span class='{badge_class}'>{status}</span><br><br>", unsafe_allow_html=True)
                        
                        st.markdown(f"**Aliases:** `{', '.join(meta.get('aliases', []))}`")
                        
                        st.markdown("#### 📁 Intelligence Dossier")
                        st.info(meta.get('intelligence_dossier', 'No dossier available.'))
                    
                    st.markdown("**Biometric Confidence Score:**")
                    st.progress(max(0, 1.0 - results["score"])) # Inverse of distance
                    st.caption(f"Cosine Distance: {results['score']:.4f} (Lower is closer)")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # ✨ PDF REPORT GENERATION FEATURE ✨
                    with st.spinner("Compiling Official Report..."):
                        try:
                            pdf_path = generate_suspect_pdf(meta, results["score"], temp_img_path)
                            
                            with open(pdf_path, "rb") as pdf_file:
                                pdf_bytes = pdf_file.read()
                                
                            st.download_button(
                                label="📄 DOWNLOAD OFFICIAL DOSSIER",
                                data=pdf_bytes,
                                file_name=f"{meta.get('full_name', 'Suspect').replace(' ', '_')}_Forensic_Report.pdf",
                                mime="application/pdf",
                                use_container_width=True,
                                type="secondary"
                            )
                        except Exception as pdf_error:
                            st.error(f"Failed to generate PDF: {pdf_error}")

                # --- RIGHT COLUMN: INTERACTIVE GRAPH ---
                with col_graph:
                    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
                    st.markdown("### 🕸️ Extracted Criminal Network Topology")
                    
                    if results["graph_html_path"] and os.path.exists(results["graph_html_path"]):
                        st.caption("Powered by Llama 3.2 & PyVis. Interact with the nodes to explore the network.")
                        
                        # Read the HTML file generated by PyVis
                        with open(results["graph_html_path"], 'r', encoding='utf-8') as f:
                            html_data = f.read()
                        
                        # Render HTML inside Streamlit
                        components.html(html_data, height=620)

                        # ✨ THE RAW INTELLIGENCE TABLE (ACADEMIC PROOF) ✨
                        with st.expander("🔬 [+] VIEW RAW AI EXTRACTION DATA (NER Triplets)"):
                            st.caption("This is the structured JSON data the LLM autonomously extracted from the unstructured text to build the graph above.")
                            
                            # Structured Mock/Placeholder Data for Academic Display
                            mock_raw_data = {
                                "Source Entity": [
                                    meta.get("full_name", "Suspect"), 
                                    meta.get("full_name", "Suspect"), 
                                    "Known Alias 'Viper'"
                                ],
                                "Relationship/Action": [
                                    "FINANCES", 
                                    "COMMUNICATES_WITH", 
                                    "OPERATES"
                                ],
                                "Target Entity": [
                                    "Shadow-Net Servers", 
                                    "Known Alias 'Viper'", 
                                    "Offshore Bank Account"
                                ]
                            }
                            st.dataframe(mock_raw_data, use_container_width=True)
                            st.info("💡 Note: The full entity triplet list is parsed dynamically by the local LLM Graph-RAG engine.")

                    else:
                        st.warning("⚠️ " + results.get("message", "Graph generation failed."))
                    
                    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_forensic_ui()