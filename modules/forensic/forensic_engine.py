import os
from modules.forensic.vector_store import find_match
from modules.forensic.rag_engine import generate_graph_data, get_suspect_metadata
from modules.forensic.graph_builder import build_interactive_graph

def process_suspect_image(image_path):
    """
    Master Orchestrator for the Biometric Graph-RAG Pipeline.
    Takes an image path, runs the full forensic pipeline, and returns the results.
    """
    print(f"\n[🚀] FORENSIC ENGINE STARTED: Processing {os.path.basename(image_path)}")
    
    result_package = {
        "status": "error",
        "message": "Unknown error occurred.",
        "match_id": None,
        "score": None,
        "metadata": None,
        "graph_html_path": None
    }

    # ---------------------------------------------------------
    # STEP 1: Biometric Verification
    # ---------------------------------------------------------
    print("[*] Step 1: Initiating Biometric Scan...")
    matched_id, score = find_match(image_path)
    
    if not matched_id:
        result_package["status"] = "no_match"
        result_package["message"] = "Subject not found in the criminal database."
        result_package["score"] = score
        return result_package

    print(f"[+] Step 1 Complete: Subject verified as '{matched_id}'")
    result_package["match_id"] = matched_id
    result_package["score"] = score

    # ---------------------------------------------------------
    # STEP 2: Fetch Metadata
    # ---------------------------------------------------------
    print("[*] Step 2: Retrieving Suspect Dossier...")
    try:
        metadata = get_suspect_metadata(matched_id)
        result_package["metadata"] = metadata
    except Exception as e:
        result_package["status"] = "error"
        result_package["message"] = f"Failed to retrieve metadata: {e}"
        return result_package

    # ---------------------------------------------------------
    # STEP 3: Graph RAG Extraction (LLM)
    # ---------------------------------------------------------
    print("[*] Step 3: Extracting Interconnected Network Graph via LLM...")
    graph_data = generate_graph_data(matched_id)
    
    if not graph_data or not graph_data.get("nodes"):
        result_package["status"] = "partial_success"
        result_package["message"] = "Match found, but the LLM failed to extract network graph data."
        return result_package

    # ---------------------------------------------------------
    # STEP 4: Build Interactive Visualization
    # ---------------------------------------------------------
    print("[*] Step 4: Rendering PyVis HTML Graph...")
    html_path = build_interactive_graph(graph_data)
    
    if not html_path:
        result_package["status"] = "partial_success"
        result_package["message"] = "Match and graph extracted, but failed to render HTML."
        return result_package

    # ---------------------------------------------------------
    # SUCCESS
    # ---------------------------------------------------------
    print("[🚀] FORENSIC ENGINE COMPLETE: Output generated successfully.\n")
    result_package["status"] = "success"
    result_package["message"] = "Biometric match and graph generation successful."
    result_package["graph_html_path"] = html_path
    
    return result_package