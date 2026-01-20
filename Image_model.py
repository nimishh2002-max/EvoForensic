import torch
from diffusers import StableDiffusionPipeline
from pathlib import Path

# =========================
# CONFIG
# =========================
MODEL_ID = "runwayml/stable-diffusion-v1-5"
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("Torch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("Using device:", DEVICE)

# =========================
# LOAD MODEL
# =========================
print("Loading Stable Diffusion model...")

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16
)

pipe = pipe.to(DEVICE)

# Memory optimizations for 6GB VRAM
pipe.enable_attention_slicing()
pipe.enable_vae_slicing()

print("Model loaded successfully!")

# =========================
# PROMPT (FORENSIC STYLE)
# =========================
prompt = (
    "forensic suspect face sketch, "
    "male, age 30, medium brown skin, "
    "short black hair, sharp jawline, "
    "thin mustache, serious expression, "
    "police forensic sketch, pencil drawing, white background"
)

negative_prompt = (
    "blurry, low quality, cartoon, anime, unrealistic, deformed face"
)

# =========================
# GENERATE IMAGE
# =========================
print("Generating image...")

image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    height=512,
    width=512,
    num_inference_steps=30,
    guidance_scale=7.5
).images[0]

# =========================
# SAVE OUTPUT
# =========================
output_path = OUTPUT_DIR / "forensic_suspect.png"
image.save(output_path)

print(f"Image saved at: {output_path.resolve()}")
