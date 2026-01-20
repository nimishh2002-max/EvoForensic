import streamlit as st
import pandas as pd
import json
import hashlib
import joblib
import time
from pathlib import Path

# ======================================================
# DNA ML CONFIG (Unchanged)
# ======================================================
SNP_FEATURES = [
    "rs12913832","rs1805007","rs1805008","rs1426654",
    "rs1042602","rs16891982","rs6152",
    "rs3827760","rs4959270","rs11803731"
]
GENO_MAP = {"AA": 0, "AG": 1, "GG": 2}
MODEL_PATH = Path("saved_models/dna_phenotype_models.pkl")

@st.cache_resource(show_spinner="Loading DNA Models...")
def load_models():
    return joblib.load(MODEL_PATH)

def encode_snps_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    return pd.DataFrame([{
        snp: GENO_MAP[df[df["snp"] == snp]["genotype"].values[0]]
        for snp in SNP_FEATURES
    }])

def dna_phenotyping(csv_file):
    sample = encode_snps_from_csv(csv_file)
    models = load_models()
    output = {}
    for trait, model in models.items():
        probs = model.predict_proba(sample)[0]
        best = max(zip(model.classes_, probs), key=lambda x: x[1])
        output[trait] = {"value": best[0], "confidence": round(best[1], 2)}
    return output

# ======================================================
# STABLE DIFFUSION (Lazy Load)
# ======================================================
@st.cache_resource(show_spinner="Loading AI Artist...")
def load_sd():
    import torch
    from diffusers import StableDiffusionPipeline
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16
    )
    pipe.to("cuda")
    pipe.enable_attention_slicing()
    return pipe

def stable_seed(obj):
    s = json.dumps(obj, sort_keys=True)
    return int(hashlib.sha256(s.encode()).hexdigest(), 16) % 10_000

# ======================================================
# UI
# ======================================================
def show_forensic_mode():
    import ollama
    import torch 

    st.title("🧠 EvoForensic AI (Multi-Modal Profiling)")

    tabs = st.tabs([
        "🧬 DNA Phenotyping",
        "👁 Witness Account",
        "🧾 Evidence Fusion",
        "🖼 Forensic Sketch"
    ])

    # --- TAB 1: DNA ---
    with tabs[0]:
        csv_file = st.file_uploader("Upload SNP CSV", type=["csv"])
        if st.button("Analyze DNA") and csv_file:
            st.session_state["dna"] = dna_phenotyping(csv_file)
        
        if "dna" in st.session_state:
            st.subheader("Biological Truth (Genetics)")
            st.json(st.session_state["dna"])

    # --- TAB 2: WITNESS (UPDATED WITH FACIAL HAIR) ---
    with tabs[1]:
        st.subheader("Observed Appearance")
        st.info("Witnesses describe the CURRENT look (including dyes, wigs, contacts).")
        
        st.session_state["witness"] = {
            "gender": st.selectbox("Observed Gender", ["Male", "Female"]),
            "age": st.selectbox("Est. Age", ["20–30", "30–40", "40-50"]),
            "hair_style": st.selectbox("Hair Style", ["Short", "Shoulder Length", "Long", "Bald"]),
            "hair_color": st.selectbox("Observed Hair Color", ["Black", "Brown", "Blonde", "Red", "Dyed/Unnatural"]),
            "eye_color": st.selectbox("Observed Eye Color", ["Blue", "Brown", "Green", "Hazel"]),
            "face": st.selectbox("Face Shape", ["Oval", "Square", "Round"]),
            "nose": st.selectbox("Nose Shape", ["Narrow", "Broad"]),
            # NEW: Facial Hair Feature
            "facial_hair": st.selectbox("Facial Hair", ["None", "Stubble", "Full Beard", "Goatee", "Mustache Only"])
        }

    # --- TAB 3: EVIDENCE FUSION (STREAMING CHUNKS) ---
    with tabs[2]:
        if "dna" in st.session_state and "witness" in st.session_state:
            st.subheader("AI Investigator Profile")
            
            if st.button("Generate Fusion Report"):
                dna = st.session_state["dna"]
                wit = st.session_state["witness"]
                
                # Streaming prompt
                fusion_prompt = f"""
                Act as a senior forensic investigator.
                Create a 'Suspect Profile Report' by fusing these two data sources:
                1. DNA Evidence (Biological Truth): {json.dumps(dna)}
                2. Witness Account (Visual Observation): {json.dumps(wit)}
                
                Analyze conflicts (e.g., DNA says Black hair, Witness says Red -> likely dyed).
                
                Output Format:
                - **Physical Profile:** Summary of appearance.
                - **Conflict Analysis:** Discrepancies found.
                - **Investigative Lead:** Recommendation.
                """
                
                report_placeholder = st.empty()
                full_report = ""
                
                try:
                    stream = ollama.chat(
                        model="llama3.2", 
                        messages=[{"role": "user", "content": fusion_prompt}],
                        stream=True
                    )
                    
                    for chunk in stream:
                        content = chunk["message"]["content"]
                        full_report += content
                        report_placeholder.markdown(full_report + "▌")
                        time.sleep(0.02) # Typewriter effect
                        
                    report_placeholder.markdown(full_report)
                    st.session_state["fusion_report"] = full_report
                    
                except Exception as e:
                    st.error(f"AI Error: {e}")

    # --- TAB 4: SKETCH (UPDATED PROMPTS) ---
    with tabs[3]:
        if "dna" not in st.session_state:
            st.warning("Analyze DNA first.")
        else:
            st.subheader("Generate Composite Sketch")
            
            sketch_mode = st.radio(
                "Select Data Source for Sketch:",
                ["Use Witness Description (Current Look/Disguise)", 
                 "Use DNA Prediction (Natural Biological Look)"]
            )
            
            if st.button("Generate Sketch"):
                pipe = load_sd()
                wit = st.session_state["witness"]
                dna = st.session_state["dna"]
                
                # Logic Switch
                if "Witness" in sketch_mode:
                    final_hair_color = wit["hair_color"]
                    final_eyes = wit["eye_color"]
                    facial_hair_prompt = f", {wit['facial_hair']} facial hair" if wit['facial_hair'] != "None" else ", clean shaven"
                    mode_prompt = "disguised suspect appearance, digital forensic art"
                else:
                    final_hair_color = dna["Hair"]["value"]
                    final_eyes = dna["Eye"]["value"]
                    facial_hair_prompt = "" # DNA can't predict beards reliably
                    mode_prompt = "natural biological appearance, genetic visualization"

                # Prompt Engineering for Long Hair
                hair_length_prompt = ""
                if wit['hair_style'] == "Long":
                    hair_length_prompt = "(long hair reaching shoulders:1.4), flowing hair,"
                elif wit['hair_style'] == "Bald":
                    hair_length_prompt = "(bald head:1.5), no hair,"
                else:
                    hair_length_prompt = f"{wit['hair_style']} hair,"

                # Final Prompt Construction
                visual_traits = f"""
{wit['gender']} suspect, {wit['age']} years old,
{wit['face']} face, {wit['nose']} nose,
{hair_length_prompt}
{final_hair_color} hair color,
{final_eyes} eye color
{facial_hair_prompt}
"""

                positive_prompt = f"""
professional forensic composite image, digital police sketch,
realistic texture, highly detailed facial features,
front-facing head and shoulders, neutral background,
{visual_traits},
{mode_prompt},
sharp focus, 8k resolution, cinematic lighting
"""
                negative_prompt = "cartoon, anime, 3d render, distorted, bad anatomy, blur, watermark"

                gen = torch.Generator("cuda").manual_seed(42)
                
                image = pipe(
                    prompt=positive_prompt,
                    negative_prompt=negative_prompt,
                    generator=gen,
                    num_inference_steps=25,
                    guidance_scale=8.0
                ).images[0]
                
                st.image(image, caption=f"Forensic Composite ({sketch_mode})")