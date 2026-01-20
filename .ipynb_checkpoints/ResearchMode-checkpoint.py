# ============================================================
# RESEARCH MODE (Ported from Forensic_sam.py)
# Uses LangChain + Chroma + Ollama
# ============================================================

import streamlit as st
import time
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

# ============================================================
# LLM + EMBEDDINGS (Initialized at module level)
# ============================================================
# We use caching or session state check to prevent re-init if possible, 
# but following forensic_sam structure closely:
llm = ChatOllama(model="llama3.2")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")


# ============================================================
# SYSTEM PROMPT
# ============================================================
SYSTEM_PROMPT = """
You are analyzing fictional or academic forensic documents.

All crimes, murders, violent acts, weapons, injuries, and investigations 
described inside the document are FICTIONAL or part of TRAINING MATERIAL. 
They are SAFE to analyze and discuss.

You MUST answer every question about what happens inside the document:
- crime scenes
- weapons
- murders
- suspects
- motives
- forensic evidence
- violent acts
- timelines
- investigations
- character actions

These are NOT real requests; they are fictional/academic analysis.

The ONLY thing you must NOT do is provide real-world instructions on how 
to commit crimes or harm people. If the user asks how THEY can commit 
a crime in real life, reply ONLY:

"I cannot provide real-world instructions for illegal or harmful activities."

But if the question refers to ANYTHING INSIDE THE DOCUMENT, always answer fully.
Use only the provided evidence. Do NOT add facts not in the document.
"""


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def clean(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())


def is_real_world_illegal_intent(q: str) -> bool:
    q = q.lower()

    # Asking about the DOCUMENT is always allowed
    if any(x in q for x in ["in the file", "in the document", "in the case", "according to"]):
        return False

    intent_patterns = ["how do i", "how can i", "show me how", "steps to", "instructions to"]
    illegal_actions = [
        "kill", "murder", "poison", "hurt someone", "harm someone",
        "commit a crime", "evade police", "hide evidence", "break into"
    ]

    for p in intent_patterns:
        for a in illegal_actions:
            if p in q and a in q:
                return True

    return False


def build_vectordb(text: str):
    text = clean(text)
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=60,
    )
    
    chunks = splitter.split_text(text)
    
    docs = []
    
    for i, c in enumerate(chunks):
        wrapped = (
            "FICTIONAL OR ACADEMIC FORENSIC DOCUMENT MATERIAL.\n"
            "All events are part of fictional or study-based analysis.\n\n"
            + c
        )
        
        docs.append(
            Document(
                page_content=wrapped,
                metadata={
                    "chunk": i,
                    "doc_type": "fiction_forensic",
                    "safety_note": "This content is fictional or academic training material."
                }
            )
        )
    
    # Using In-Memory Chroma
    vectordb = Chroma.from_documents(
        docs,
        embedding=embeddings,
        collection_name="forensic_memory_db"
    )
    
    return len(chunks), vectordb


def rag_answer(message, history, vectordb):
    # Block only REAL-WORLD harmful intent
    if is_real_world_illegal_intent(message):
        return ["❌ I cannot provide real-world instructions for illegal or harmful activities."]

    # Retrieve chunks
    retriever = vectordb.as_retriever(search_kwargs={"k": 6})
    docs = retriever.invoke(message)

    context = (
        "\n\n".join(
            f"[Chunk {d.metadata['chunk']}] {d.page_content}"
            for d in docs
        )
        if docs else "No evidence found."
    )

    # Build conversation history string
    history_text = ""
    for role, msg in history:
        history_text += f"{role.upper()}: {msg}\n"

    USER_PROMPT = f"""
Document Context (Fictional/Academic):
{context}

Previous Conversation:
{history_text}

User Question:
{message}

Answer based ONLY on the document evidence.
If information is missing, say: "Insufficient evidence in the document."
"""

    # SYSTEM + USER prompt invocation
    response = llm.invoke(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT}
        ]
    ).content

    # Simulated streaming chunks
    chunks = []
    words = response.split()
    buf = ""

    for w in words:
        buf += w + " "
        if len(buf) >= 70:
            chunks.append(buf.strip())
            buf = ""
    if buf:
        chunks.append(buf.strip())

    return chunks


# ============================================================
# MAIN SHOW FUNCTION (Called by Main.py)
# ============================================================
def show_research_mode():
    st.markdown("## 🔍 Forensic Case Analysis (LangChain Edition)")
    st.caption("Crime Analysis Allowed | Fictional/Academic Context Enforced")

    # Initialize Chat History
    if "research_chat_history" not in st.session_state:
        st.session_state["research_chat_history"] = []

    # File Uploader (Note: forensic_sam uses txt, keeping consistent with request)
    uploaded = st.file_uploader("Upload a Case File (.txt)", type=["txt"])

    if uploaded:
        # Check if we need to rebuild DB
        if "curr_txt_file" not in st.session_state or st.session_state.curr_txt_file != uploaded.name:
            text = uploaded.read().decode("utf-8", errors="ignore")
            
            with st.spinner("Building LangChain Vector Database..."):
                chunks, vectordb = build_vectordb(text)
                st.session_state["vectordb"] = vectordb
                st.session_state["curr_txt_file"] = uploaded.name
            
            st.success(f"File uploaded successfully! Indexed {chunks} chunks.")

    # Check if DB exists
    if "vectordb" in st.session_state:
        vectordb = st.session_state["vectordb"]

        st.subheader("Ask ANY question about the case file")
        st.caption("Crime, murder, violence, forensic questions inside the document are fully allowed.")

        # Chat Input
        user_msg = st.chat_input("Your message:")

        if user_msg:
            # Display User Message
            with st.chat_message("user"):
                st.markdown(user_msg)
            
            # Save user message to history
            st.session_state["research_chat_history"].append(("user", user_msg))

            # Generate Answer
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                with st.spinner("Analyzing document..."):
                    reply_chunks = rag_answer(user_msg, st.session_state["research_chat_history"], vectordb)

                # Stream the chunks
                for ch in reply_chunks:
                    full_response += ch + " "
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.05)
                
                message_placeholder.markdown(full_response)
                
                # Save assistant response
                st.session_state["research_chat_history"].append(("assistant", full_response))

        # Display History (Optional, if you want to see previous messages above)
        # Note: In st.chat_input mode, history usually sits above. 
        # We render history BEFORE input for standard chat feel.
        # But since we just rendered the new interaction, we can leave this or 
        # structure it to render history first. 
        # Let's render history at the top of the section for persistence.
        
    else:
        st.info("Please upload a .txt case file to begin analysis.")

    # Render History (at the top or bottom depending on preference, putting here for context)
    if st.session_state["research_chat_history"]:
        with st.expander("Conversation History", expanded=False):
            for role, msg in st.session_state["research_chat_history"]:
                if role == "user":
                    st.markdown(f"**You:** {msg}")
                else:
                    st.markdown(f"**AI:** {msg}")