import streamlit as st
import os
import sys

# Ensure modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import YOUR custom RAG Logic
try:
    from modules import ResearchMode
except ImportError as e:
    st.error(f"⚠️ Missing Module: Ensure 'modules/ResearchMode.py' exists. Error: {e}")

# ---------------------------------------------------------
# 1. PROFESSIONAL CYBER-INTEL THEME (CSS OVERRIDES)
# ---------------------------------------------------------
def inject_professional_theme():
    st.markdown("""
    <style>
        /* Modern Dark Slate Background */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0A0E17 !important;
            color: #E5E7EB !important;
            font-family: 'Inter', 'Segoe UI', sans-serif !important;
        }

        /* Seamless Sidebar */
        [data-testid="stSidebar"], [data-testid="stSidebarHeader"] {
            background-color: #0B0F19 !important;
            border-right: 1px solid #1F2937 !important;
        }

        h1, h2, h3, h4, p, label, span, .stMarkdown p { color: #F9FAFB !important; }

        .intel-heading {
            color: #00D2FF !important;
            font-family: 'Courier New', monospace;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 0px;
            font-size: 2.2rem;
        }

        .sub-heading {
            color: #9CA3AF !important;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 5px;
            margin-bottom: 30px;
        }

        /* Sleek File Uploader */
        div[data-testid="stFileUploader"] { background-color: transparent !important; }
        div[data-testid="stFileUploader"] > section, [data-testid="stFileUploadDropzone"] {
            background-color: #111827 !important;
            border: 1px dashed #374151 !important;
            border-radius: 6px !important;
            padding: 25px !important;
            transition: all 0.2s ease-in-out;
        }
        div[data-testid="stFileUploader"] > section:hover, [data-testid="stFileUploadDropzone"]:hover {
            border-color: #00D2FF !important; background-color: #1F2937 !important;
        }
        div[data-testid="stFileUploader"] small, div[data-testid="stFileUploader"] span, 
        div[data-testid="stFileUploader"] p, div[data-testid="stFileUploader"] div { color: #D1D5DB !important; }
        
        div[data-testid="stFileUploader"] button {
            background-color: #1F2937 !important; color: #00D2FF !important;
            border: 1px solid #00D2FF !important; font-weight: 600 !important;
            border-radius: 4px !important; padding: 4px 15px !important;
        }
        div[data-testid="stFileUploader"] button:hover { background-color: #00D2FF !important; color: #0A0E17 !important; }
        div[data-testid="stFileUploader"] svg { fill: #00D2FF !important; color: #00D2FF !important; }

        /* Chat Input Styling */
        div[data-testid="stChatInput"] { background-color: #111827 !important; border: 1px solid #374151 !important; border-radius: 6px !important; }
        div[data-testid="stChatInput"] div { background-color: transparent !important; }
        div[data-testid="stChatInput"] textarea {
            color: #FFFFFF !important; background-color: #111827 !important;
            -webkit-text-fill-color: #FFFFFF !important; caret-color: #00D2FF !important;
        }
        div[data-testid="stChatInput"] textarea::placeholder { color: #9CA3AF !important; -webkit-text-fill-color: #9CA3AF !important; }
        div[data-testid="stChatInput"] button { background-color: transparent !important; border: none !important; }
        div[data-testid="stChatInput"] button svg { fill: #00D2FF !important; color: #00D2FF !important; }
        div[data-testid="stChatInput"] button:hover svg { fill: #FFFFFF !important; }

        /* General Buttons */
        .stButton > button {
            background-color: #111827 !important; border: 1px solid #00D2FF !important;
            color: #00D2FF !important; border-radius: 4px !important;
            font-weight: 600; letter-spacing: 0.5px; transition: all 0.2s ease;
        }
        .stButton > button:hover { background-color: #00D2FF !important; color: #0A0E17 !important; }
        
        /* Chat Messages */
        div[data-testid="stChatMessage"] {
            background-color: #111827 !important; border: 1px solid #1F2937 !important;
            border-radius: 6px; padding: 15px; margin-bottom: 12px;
        }
        div[data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] p { color: #E5E7EB !important; line-height: 1.6; }
        
        /* Glass Panels */
        .glass-panel {
            background-color: rgba(17, 24, 39, 0.6); border: 1px solid #1F2937;
            border-radius: 6px; padding: 20px; margin-bottom: 15px;
        }
        .stAlert { background-color: #111827 !important; color: #D1D5DB !important; border: 1px solid #374151 !important; border-radius: 4px !important; }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. MAIN RESEARCH UI
# ---------------------------------------------------------
def show_research_ui():
    inject_professional_theme()
    
    col1, col2 = st.columns([0.5, 9.5])
    with col1:
        st.markdown("<div style='font-size: 2.2rem; margin-top: -5px;'>🛡️</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<h1 class='intel-heading'>Secure Document Terminal</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-heading'>Retrieval-Augmented Generation (R.A.G.) Analysis Engine</p>", unsafe_allow_html=True)

    st.markdown("---")

    col_upload, col_chat = st.columns([1.2, 2])

    # --- LEFT PANEL: UPLOAD & VECTORIZE ---
    with col_upload:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("### 📁 Evidence Ingestion")
        st.caption("Upload text records, logs, or case files. The system will vectorize the data into the secure ChromaDB enclave.")
        
        uploaded_file = st.file_uploader("Upload Secure Files", type=["txt", "csv", "json"], label_visibility="collapsed")
        
        if uploaded_file is not None:
            st.success(f"✔️ File Acquired: {uploaded_file.name}")
            
            if st.button("⚡ PROCESS EVIDENCE", use_container_width=True):
                with st.spinner("Extracting Metadata & Building Vector DB..."):
                    try:
                        # 1. Read the text from the uploaded file
                        text_content = uploaded_file.getvalue().decode("utf-8")
                        
                        # 2. Pass string to YOUR custom logic
                        num_docs, vectordb = ResearchMode.build_vectordb(text_content)
                        
                        # 3. Store the DB in Session State so it persists for the chat
                        st.session_state["doc_loaded"] = True
                        st.session_state["vectordb"] = vectordb
                        
                        st.success(f"Data successfully embedded ({num_docs} chunks). System ready for queries.")
                    except Exception as e:
                        st.error(f"Error processing document: {e}")
                        
        else:
            st.info("System Idle. Awaiting evidence files (e.g., case.txt).")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- RIGHT PANEL: RAG QUERY TERMINAL ---
    with col_chat:
        st.markdown("### 📡 Terminal Interrogation")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🕵️" if message["role"] == "user" else "🤖"):
                st.markdown(message["content"])

        prompt = st.chat_input("Query the evidence (e.g., 'Tell me about case file 14')...")
        
        if prompt:
            # Add user message to UI
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="🕵️"):
                st.markdown(prompt)

            # Generate AI Response
            with st.chat_message("assistant", avatar="🤖"):
                if not st.session_state.get("doc_loaded", False) or "vectordb" not in st.session_state:
                    response = "⚠️ **Access Denied.** No evidence loaded. Please ingest a document into the database first."
                    st.markdown(f"<span style='color: #F87171;'>{response}</span>", unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    # Format history for YOUR custom rag_answer function:
                    # Extract list of tuples: [("user", "hi"), ("assistant", "hello")]
                    history_tuples = [(m["role"], m["content"]) for m in st.session_state.messages[:-1]]
                    
                    # Fetch the database from session state
                    db_instance = st.session_state["vectordb"]
                    
                    # Call YOUR generator function
                    response_stream = ResearchMode.rag_answer(prompt, history_tuples, db_instance)
                    
                    # Streamlit's write_stream handles Python generators beautifully
                    full_response = st.write_stream(response_stream)
                    
                    # Save final output to history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    show_research_ui()