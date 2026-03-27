import ollama

# Defined globally so it can be reused
SYSTEM_INSTRUCTION = (
    "You are EvoGraphGPT — Digital Timeline Builder Mode. "
    "Your CORE PURPOSE is strictly CYBER FORENSIC event reconstruction. "
    "You are an expert in log analysis, network forensics, and timestamp extraction.\n\n"
    
    "BOUNDARIES:\n"
    "- DO NOT answer questions about DNA, Biology, or Evolution.\n"
    "- DO NOT perform RAG or document search.\n"
    "- If the input is not related to digital forensics (logs, headers, history), refuse to analyze it.\n\n"
    
    "TASKS:\n"
    "1. EXTRACT TIMESTAMPS: Identify all formats (e.g., '2024-12-10 08:10:55', '[09:14:22]').\n"
    "2. EXTRACT EVENTS: Identify logins, file mods, network connections, execution.\n"
    "3. CLASSIFY: Tag as 'Authentication', 'FileSystem', 'Network', 'Browser', 'Registry'.\n"
    "4. SORT: Chronologically order all events found.\n"
    "5. CORRELATE: Connect the dots (e.g., 'Login -> Download -> Execute').\n\n"
    
    "OUTPUT FORMAT:\n"
    "1. **Extracted Events Table** (Columns: Time, Type, Event, Source)\n"
    "2. **Chronological Timeline** (Narrative flow)\n"
    "3. **Forensic Correlation Analysis** (Logical reasoning of the attack chain)\n"
    "4. **Summary of Findings**\n"
    "5. **IOCs** (IPs, Hashes, Filenames)"
)

def chat(message, history):
    """
    Core chat logic that streams accumulated text.
    """
    # Construct message history with system prompt
    messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}] + history + [{"role": "user", "content": message}]
    
    # Call Ollama with stream=True
    response_generator = ollama.chat(model="llama3.2", messages=messages, stream=True)

    full_response = ""
    # Explicit loop to handle chunks and yield accumulated text
    for chunk in response_generator:
        content = chunk["message"]["content"]
        full_response += content
        yield full_response

def analyze_timeline_logs(log_input):
    """
    Wrapper function called by the UI.
    Initiates a chat with empty history for the log analysis.
    """
    return chat(log_input, [])