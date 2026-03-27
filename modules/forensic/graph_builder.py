import os
import networkx as nx
from pyvis.network import Network

# =====================================================================
# CONFIGURATION & PATHS
# =====================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "graphs")
GRAPH_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "suspect_graph.html")

def ensure_output_dir():
    """Ensure the outputs/graphs directory exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_node_color(node_type):
    """Assigns specific colors based on the entity type to fit the forensic theme."""
    node_type = str(node_type).lower()
    if "person" in node_type or "suspect" in node_type:
        return "#ff4b4b"  # Red
    elif "ip" in node_type or "network" in node_type:
        return "#4b4bff"  # Blue
    elif "organization" in node_type or "company" in node_type:
        return "#4bff4b"  # Green
    elif "malware" in node_type or "exploit" in node_type:
        return "#ffb04b"  # Orange
    elif "device" in node_type or "hardware" in node_type:
        return "#b04bff"  # Purple
    elif "location" in node_type:
        return "#4bffb0"  # Teal
    else:
        return "#cccccc"  # Light Grey fallback

def build_interactive_graph(graph_data):
    """
    Takes a dictionary containing 'nodes' and 'edges' and generates 
    an interactive PyVis HTML file.
    """
    ensure_output_dir()
    
    print("[*] Initializing network graph builder...")
    
    # 1. Initialize PyVis Network (Dark Mode)
    # Using 100% width/height so it fits perfectly inside Streamlit's iframe
    net = Network(
        height="600px", 
        width="100%", 
        bgcolor="#111111", 
        font_color="white", 
        directed=True
    )
    
    # 2. Add Nodes
    nodes = graph_data.get("nodes", [])
    if not nodes:
        print("[-] No nodes found in graph data.")
        return None
        
    for node in nodes:
        node_id = node.get("id")
        label = node.get("label", node_id)
        n_type = node.get("type", "Unknown")
        
        # Add node with styling
        net.add_node(
            node_id, 
            label=label, 
            title=f"Type: {n_type}", # Hover tooltip
            color=get_node_color(n_type),
            size=25,
            borderWidth=2,
            borderWidthSelected=4
        )
        
    # 3. Add Edges
    edges = graph_data.get("edges", [])
    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        label = edge.get("label", "")
        
        # Ensure both source and target exist in our nodes list to prevent PyVis errors
        node_ids = [n.get("id") for n in nodes]
        if source in node_ids and target in node_ids:
            net.add_edge(
                source, 
                target, 
                title=label, # Hover tooltip
                label=label, # Text on the line
                color="#555555",
                arrows="to"
            )
            
    # 4. Configure Physics (Makes it bouncy and dynamic)
    net.set_options("""
    var options = {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -100,
          "centralGravity": 0.01,
          "springLength": 200,
          "springConstant": 0.08
        },
        "maxVelocity": 50,
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": {"iterations": 150}
      },
      "edges": {
        "smooth": {
          "type": "dynamic"
        },
        "font": {
          "color": "#aaaaaa",
          "size": 12,
          "background": "none"
        }
      }
    }
    """)
    
    # 5. Export to HTML
    try:
        net.save_graph(GRAPH_OUTPUT_PATH)
        print(f"[+] Interactive graph successfully saved to: {GRAPH_OUTPUT_PATH}")
        return GRAPH_OUTPUT_PATH
    except Exception as e:
        print(f"[-] Failed to save graph: {e}")
        return None

if __name__ == "__main__":
    # Test script with dummy data
    print("=== Sherlock-AI Graph Builder Test ===")
    dummy_data = {
        "nodes": [
            {"id": "Philip", "label": "Philip Menon", "type": "Person"},
            {"id": "102.45.19.221", "label": "102.45.19.221", "type": "IP"},
            {"id": "Graham", "label": "Graham Blue", "type": "Person"}
        ],
        "edges": [
            {"source": "Philip", "target": "102.45.19.221", "label": "uses VPN"},
            {"source": "Graham", "target": "Philip", "label": "gave credentials to"}
        ]
    }
    build_interactive_graph(dummy_data)