🕵️‍♂️ Sherlock-AI: Forensic Intelligence Suite

A Multi-Modal Forensic Analysis System utilizing Generative AI, DNA Phenotyping, and Digital Forensics.

📜 Abstract

Modern forensic investigations are often hindered by data fragmentation, where biological evidence, digital logs, and case files exist in isolated silos. Sherlock-AI is a comprehensive, privacy-centric forensic intelligence suite designed to unify these domains through advanced Artificial Intelligence.

The core innovation lies in its Bio-Forensic Module, which introduces a novel pipeline for Predictive DNA Phenotyping. By utilizing alignment-invariant motif scanning algorithms and Machine Learning classifiers, the system extracts phenotypic traits (eye color, hair color, ancestry) from raw genomic sequences. These biological insights are fused with witness testimonies using a Large Language Model (Llama 3.2) to construct a comprehensive suspect profile. This profile drives a Latent Diffusion Model (Stable Diffusion), generating high-fidelity forensic composite sketches—effectively translating raw DNA code into visual suspect identification.

Furthermore, the system integrates a Retrieval-Augmented Generation (RAG) engine for Document Intelligence and a Digital Timeline Module for cyber-forensic log reconstruction.

🚀 Key Features

🧬 Bio-Forensic Mode

Predictive Phenotyping: Predicts Hair Color, Eye Color, and Ancestry from raw DNA sequences (.csv/FASTA).

Evidence Fusion: Uses LLMs to cross-reference "Biological Truth" (DNA) against "Witness Testimony" to detect disguises (wigs, contacts).

Generative Sketching: Uses Stable Diffusion to generate two distinct suspect composites:

Natural Biological Appearance (DNA-based)

Observed Appearance (Witness-based)

📄 Research Mode (RAG)

Document Intelligence: Upload Case Files (PDF) and query them using natural language.

Context-Aware Safety: Distinguishes between academic forensic analysis (allowed) and real-world harmful queries (blocked).

🕰️ Digital Timeline Mode

Log Reconstruction: Parses fragmented server logs and firewall data.

Event Correlation: Automatically sorts events chronologically to reconstruct cyber-attack chains.

🔐 Secure Architecture

Dual-State UI: Cinematic "Gateway" interface for login vs. Professional "Dark Mode" workspace for analysis.

RBAC: Role-Based Access Control (Student, Police, Scientist) backed by SQLite.

🛠️ Installation & Setup

Prerequisites

Python 3.10+

NVIDIA GPU (Recommended for Image Generation) with CUDA support.

Ollama installed and running locally with llama3.2 model.

1. Clone the Repository

git clone [https://github.com/yourusername/sherlock-ai.git](https://github.com/yourusername/sherlock-ai.git)
cd sherlock-ai


2. Install Dependencies

pip install -r requirements.txt


3. Setup Models

Ollama: Ensure Ollama is running (ollama serve).

Stable Diffusion: The system will auto-download runwayml/stable-diffusion-v1-5 on first run (approx 4GB).

DNA Models: Ensure saved_models/dna_phenotype_models.pkl is present in the directory.

4. Run the Application

Launch the main gateway:

streamlit run ui.py


📂 Project Structure

Sherlock-AI/
├── modules/               # Forensic Logic Cores
│   ├── ForensicMode.py    # DNA & Sketch Generation
│   ├── ResearchMode.py    # RAG & PDF Analysis
│   └── DigitalTimelineMode.py
├── saved_models/          # ML Classifiers
│   └── dna_phenotype_models.pkl
├── ui.py                  # Main Launcher & Auth Gateway
├── Main.py                # Dashboard Controller
├── forensic.db            # SQLite Database (Auto-generated)
└── requirements.txt       # Python Libraries


🤖 Tech Stack

Frontend: Streamlit (Custom CSS/HTML Components)

LLM Engine: Ollama (Llama 3.2)

Image Generation: PyTorch, Diffusers (Stable Diffusion v1.5)

RAG Engine: LangChain, ChromaDB

Database: SQLite3

© 2025 EvoForensic Team | For Academic & Major Project Use Only