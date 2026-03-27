import os
import pickle
from deepface import DeepFace
from scipy.spatial.distance import cosine

# =====================================================================
# CONFIGURATION
# =====================================================================
# Automatically resolve the absolute path to the MainProject root directory
# __file__ is .../MainProject/modules/forensic/vector.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SUSPECTS_DIR = os.path.join(BASE_DIR, "data", "suspects")
DB_PATH = os.path.join(BASE_DIR, "data", "vector_db", "suspect_embeddings.pkl")

MODEL_NAME = "Facenet512"  # Highly accurate forensic model
MATCH_THRESHOLD = 0.30     # Strict cosine distance threshold (lower is stricter)

def build_vector_db():
    """
    Scans the suspects directory, extracts DeepFace embeddings, 
    and saves them to a pickle dictionary.
    """
    print(f"[*] Building Vector Database from {SUSPECTS_DIR}...")
    
    # Ensure directories exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(SUSPECTS_DIR, exist_ok=True)
    
    embeddings_db = {}
    
    # Check if there are images
    valid_extensions = ('.png', '.jpg', '.jpeg')
    image_files = [f for f in os.listdir(SUSPECTS_DIR) if f.lower().endswith(valid_extensions)]
    
    if not image_files:
        print(f"[!] No images found in {SUSPECTS_DIR}. Please add suspect images.")
        return

    for filename in image_files:
        img_path = os.path.join(SUSPECTS_DIR, filename)
        # Extract suspect ID without extension (e.g., 'alexander.jpg' -> 'alexander')
        suspect_id = os.path.splitext(filename)[0].lower()
        
        print(f"[*] Extracting biometric vectors for: {filename}...")
        try:
            # Extract embedding (enforce_detection ensures it finds a face)
            embedding_objs = DeepFace.represent(
                img_path=img_path, 
                model_name=MODEL_NAME, 
                enforce_detection=True
            )
            # Take the embedding of the first detected face
            embedding = embedding_objs[0]["embedding"]
            embeddings_db[suspect_id] = embedding
            print(f"[+] Successfully indexed: {suspect_id}")
            
        except ValueError as e:
            print(f"[-] No face detected in {filename}: {e}")
        except Exception as e:
            print(f"[-] Error processing {filename}: {e}")

    # Save dictionary to persistent Pickle file
    with open(DB_PATH, 'wb') as f:
        pickle.dump(embeddings_db, f)
        
    print(f"\n[🚀] Vector DB successfully saved to {DB_PATH}")
    print(f"[*] Total indexed suspects: {len(embeddings_db)}")


def find_match(target_img_path, threshold=MATCH_THRESHOLD):
    """
    Reads a new image and compares it against the saved embeddings database.
    Returns: (matched_suspect_id, distance_score) or (None, distance_score)
    """
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Vector DB not found at {DB_PATH}. Please run build_vector_db() first.")
        
    # Load database
    with open(DB_PATH, 'rb') as f:
        embeddings_db = pickle.load(f)
        
    try:
        print("[*] Extracting features from uploaded target image...")
        target_objs = DeepFace.represent(
            img_path=target_img_path, 
            model_name=MODEL_NAME, 
            enforce_detection=True
        )
        target_embedding = target_objs[0]["embedding"]
    except ValueError:
        print("[-] Error: No face could be detected in the uploaded image.")
        return None, 1.0
    except Exception as e:
        print(f"[-] Unexpected error during feature extraction: {e}")
        return None, 1.0
        
    best_match = None
    best_score = float('inf')  # For cosine distance, lower is closer
    
    # Iterate through saved suspects and find the closest vector
    for suspect_id, stored_embedding in embeddings_db.items():
        distance = cosine(target_embedding, stored_embedding)
        
        if distance < best_score:
            best_score = distance
            best_match = suspect_id
            
    # Determine if it passes the strict threshold
    if best_score <= threshold:
        print(f"[+] VERIFIED MATCH: {best_match.upper()} (Distance: {best_score:.4f})")
        return best_match, best_score
    else:
        print(f"[-] NO MATCH. Closest was {best_match} (Distance: {best_score:.4f} > {threshold})")
        return None, best_score


if __name__ == "__main__":
    # When you run `python modules/forensic/vector.py` from the terminal, 
    # it will build the database from your local suspects folder.
    print("=== Sherlock-AI Biometric Database Initializer ===")
    build_vector_db()