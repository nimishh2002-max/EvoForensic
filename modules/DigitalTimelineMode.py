import streamlit as st
import ollama
import time

def show_timeline_mode():
    st.markdown("## 🕰️ Digital Timeline & Event Reconstruction")
    st.caption("Strict Cyber-Forensic Mode | Log Analysis | Correlation Engine")

    # --- 1. SYSTEM PROMPT CONFIGURATION ---
    system_instruction = (
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

    if "timeline_chat" not in st.session_state:
        st.session_state.timeline_chat = [{
            "role": "system", 
            "content": system_instruction
        }]

    # --- 2. INPUT INTERFACE ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("📋 **Paste Digital Artifacts** (Server Logs, Firewall Data, Browser History, Email Headers)")
        log_input = st.text_area("Raw Data Input:", height=300, placeholder="Dec 10 08:55:01 server sshd[123]: Failed password for root from 192.168.1.50...")
        
        analyze_btn = st.button("🔍 Reconstruct Incident Timeline", type="primary")

    with col2:
        st.markdown("### 🛑 Mode Rules")
        st.warning(
            "This mode is **ISOLATED**.\n\n"
            "❌ No DNA/Bio Analysis\n"
            "❌ No PDF/RAG Search\n"
            "✅ Log Forensics Only\n"
            "✅ Timestamp Sorting"
        )
        if st.button("🗑️ Clear Timeline Workspace"):
            st.session_state.timeline_chat = [{"role": "system", "content": system_instruction}]
            st.rerun()

    # --- 3. ANALYSIS LOGIC (STREAMING ENABLED) ---
    if analyze_btn and log_input:
        # User message wrapper
        user_prompt = f"Analyze these digital artifacts and build the timeline:\n\n{log_input}"
        
        # Add to history
        st.session_state.timeline_chat.append({"role": "user", "content": user_prompt})
        
        st.markdown("---")
        st.markdown("### 🕵️ Forensic Report")
        
        # Create a placeholder for the streaming output
        report_container = st.empty()
        full_response = ""
        
        try:
            # Call Ollama with stream=True
            stream = ollama.chat(
                model="llama3.2", 
                messages=st.session_state.timeline_chat,
                stream=True
            )
            
            # Loop through chunks and update UI in real-time
            for chunk in stream:
                content = chunk["message"]["content"]
                full_response += content
                report_container.markdown(full_response + "▌")
            
            # Final render without the cursor
            report_container.markdown(full_response)
            
            # Save final response to history
            st.session_state.timeline_chat.append({"role": "assistant", "content": full_response})
                
        except Exception as e:
            st.error(f"Analysis Failed: {str(e)}")
            st.info("Ensure Ollama is running locally.")

    # --- 4. CHAT HISTORY & FOLLOW-UP (STREAMING ENABLED) ---
    if len(st.session_state.timeline_chat) > 2:
        st.markdown("---")
        st.caption("Detailed Q&A on this Timeline")
        for msg in st.session_state.timeline_chat:
            if msg["role"] != "system":
                # Hide large input dumps
                if msg["role"] == "user" and "Analyze these digital artifacts" in msg["content"]:
                    continue 
                
                avatar = "🕵️" if msg["role"] == "assistant" else "👤"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])

        if follow_up := st.chat_input("Ask about specific events (e.g., 'Was the root login successful?')..."):
            st.session_state.timeline_chat.append({"role": "user", "content": follow_up})
            with st.chat_message("user", avatar="👤"):
                st.markdown(follow_up)
            
            with st.chat_message("assistant", avatar="🕵️"):
                message_placeholder = st.empty()
                full_ans = ""
                
                try:
                    stream_res = ollama.chat(
                        model="llama3.2", 
                        messages=st.session_state.timeline_chat,
                        stream=True
                    )
                    
                    for chunk in stream_res:
                        content = chunk["message"]["content"]
                        full_ans += content
                        message_placeholder.markdown(full_ans + "▌")
                    
                    message_placeholder.markdown(full_ans)
                    st.session_state.timeline_chat.append({"role": "assistant", "content": full_ans})
                    
                except Exception as e:
                    st.error(f"Ollama Error: {e}")