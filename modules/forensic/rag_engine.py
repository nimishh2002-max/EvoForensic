import os
import json
import ollama

# =====================================================================
# CONFIGURATION & PATHS
# =====================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_PATH = os.path.join(BASE_DIR, "data", "cases", "case_records.json")

def get_suspect_metadata(suspect_id):
    """Fetches the self-contained dossier and metadata for a given suspect."""
    if not os.path.exists(JSON_PATH):
        raise FileNotFoundError(f"Case records not found at {JSON_PATH}")
        
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        records = json.load(f)
        
    suspect_data = records.get(suspect_id.lower())
    if not suspect_data:
        raise ValueError(f"No records found for suspect ID: {suspect_id}")
        
    return suspect_data

def generate_graph_data(suspect_id):
    """
    Master function: Gets the self-contained dossier from JSON, 
    and uses Llama 3.2 to extract a structured JSON graph topology.
    """
    print(f"[*] Starting Graph Extraction for: {suspect_id.upper()}")
    
    # 1. Fetch Metadata & Dossier
    try:
        meta = get_suspect_metadata(suspect_id)
    except Exception as e:
        print(f"[-] {e}")
        return {"nodes": [], "edges": []}
        
    dossier_text = meta.get("intelligence_dossier", "")
    print(f"[*] Loaded isolated intelligence dossier ({len(dossier_text)} characters).")
    
    # 2. LLM Interrogation
    print("[*] Interrogating Llama 3.2 for Entity and Relationship extraction...")
    
    system_prompt = """
    You are an expert Cyber Forensic Data Extractor. Your task is to analyze a suspect's intelligence dossier and extract a network graph.
    You MUST output ONLY valid JSON. Do not include markdown formatting like ```json or any conversational text.
    
    Extract entities as "nodes" and relationships as "edges".
    Nodes should have: id (string), label (string), type (Person, IP, Location, Organization, Malware, Device)
    Edges should have: source (string: matching a node id), target (string: matching a node id), label (string: relationship description)
    
    Structure your output exactly like this:
    {
      "nodes": [
        {"id": "Philip", "label": "Philip Menon", "type": "Person"},
        {"id": "192.168.1.1", "label": "192.168.1.1", "type": "IP"}
      ],
      "edges": [
        {"source": "Philip", "target": "192.168.1.1", "label": "used IP"}
      ]
    }
    """
    
    user_prompt = f"""
    SUSPECT ALIASES: {meta.get('aliases')}
    CURRENT STATUS: {meta.get('status')}
    
    INTELLIGENCE DOSSIER:
    {dossier_text}
    
    Extract the network graph for this suspect based ONLY on the dossier text above. Ensure the suspect is the central node.
    """
    
    try:
        response = ollama.chat(model="llama3.2", messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        
        raw_output = response["message"]["content"].strip()
        
        # Clean up Markdown if Llama ignores instructions
        if raw_output.startswith("```json"):
            raw_output = raw_output[7:]
        if raw_output.startswith("```"):
            raw_output = raw_output[3:]
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3]
            
        graph_data = json.loads(raw_output.strip())
        print("[+] Graph structured data successfully extracted!")
        return graph_data
        
    except json.JSONDecodeError as e:
        print(f"[-] LLM Output Error: Did not return valid JSON. ({e})")
        print(f"Raw Output was: {raw_output}")
        return {"nodes": [], "edges": []}
    except Exception as e:
        print(f"[-] Extraction failed: {e}")
        return {"nodes": [], "edges": []}