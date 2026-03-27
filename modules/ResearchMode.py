# ============================================================
# RESEARCH MODE (Logic Core)
# Uses LangChain + Chroma (In-Memory) + Ollama
# ============================================================

import time
import re
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

# Initialize Models
# increased context window for better answers
llm = ChatOllama(model="llama3.2", temperature=0.3) 
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

SYSTEM_PROMPT = """
You are a Forensic Research Assistant.
You have access to a specific set of Case Files (Training Material).

RULES:
1. Answer ONLY based on the provided CONTEXT.
2. If the user asks about a specific Case ID (e.g., "Case 12"), look for that ID in the context.
3. If the context contains the answer, summarize it professionally.
4. If the context is empty or irrelevant, say "Insufficient Evidence in the provided file."
"""

def build_vectordb(text: str):
    """
    Reads a file and builds a temporary in-memory Vector DB with Metadata.
    """
    # 1. Pre-Split by Case to ensure Case boundaries are respected
    # This regex splits the text whenever it sees "⭐ CASE FILE" but keeps the delimiter.
    case_blocks = re.split(r'(?=⭐\s*CASE FILE)', text)
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    
    docs = []
    global_chunk_index = 0
    
    for block in case_blocks:
        if not block.strip():
            continue
            
        # 2. Extract Case Number for Metadata
        # Matches "CASE FILE 18" or "CASE FILE 2" ignoring case
        match = re.search(r"CASE FILE\s+(\d+)", block, re.IGNORECASE)
        case_num = match.group(1) if match else "general"
        
        # 3. Sub-chunk this specific case block
        chunks = splitter.split_text(block)
        
        for c in chunks:
            # Store case number explicitly in metadata
            meta = {
                "chunk": global_chunk_index,
                "case_number": case_num
            }
            # We also prepend the Case ID to the content to help semantic search
            wrapped = f"CASE {case_num} EVIDENCE:\n{c}"
            
            docs.append(Document(page_content=wrapped, metadata=meta))
            global_chunk_index += 1
    
    # Create Ephemeral Chroma Instance
    vectordb = Chroma.from_documents(
        docs,
        embedding=embeddings,
        collection_name="temp_forensic_db"
    )
    return len(docs), vectordb

def rag_answer(message, history, vectordb):
    """
    Generator that streams the answer chunk-by-chunk.
    Uses Metadata Filtering if a specific case is requested.
    """
    # 1. Analyze User Query for Case Number
    # Looks for "case 18", "case file 18", "case #18"
    target_case = None
    case_query_match = re.search(r"case\s*(?:file|id|#)?\s*(\d+)", message, re.IGNORECASE)
    
    search_kwargs = {"k": 7}
    
    if case_query_match:
        target_case = case_query_match.group(1)
        # 2. Apply Strict Metadata Filter
        # This tells Chroma: "Only give me chunks where case_number == target_case"
        search_kwargs["filter"] = {"case_number": target_case}
    
    # 3. Retrieve
    retriever = vectordb.as_retriever(search_kwargs=search_kwargs)
    docs = retriever.invoke(message)
    
    if not docs:
        if target_case:
            yield f"⚠️ Case File {target_case} not found in the uploaded document."
        else:
            yield "⚠️ No relevant evidence found in the document."
        return

    # Combine retrieved docs into context
    context = "\n----------------\n".join([d.page_content for d in docs])
    
    # Construct Prompt
    # We limit history to last 3 turns to prevent context overflow
    recent_history = history[-3:] 
    history_text = "\n".join([f"{role.upper()}: {msg}" for role, msg in recent_history])
    
    user_prompt = f"""
    RETRIEVED CASE EVIDENCE:
    {context}
    
    CHAT HISTORY:
    {history_text}
    
    INVESTIGATOR QUESTION:
    {message}
    
    TASK: Analyze the 'RETRIEVED CASE EVIDENCE' above to answer the question. 
    If the case is found, provide a summary including the Case ID, Type, and Verdict.
    """
    
    # Stream Response
    stream = llm.stream([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ])
    
    # Yield content directly
    for chunk in stream:
        yield chunk.content