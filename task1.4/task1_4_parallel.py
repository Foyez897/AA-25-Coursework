import os
import time
import face_recognition
import multiprocessing

# ✅ Define Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_FACE_PATH = os.path.join(BASE_DIR, "known_man.jpg")  # Path to known face image
IMAGESET_FOLDER = os.path.join(BASE_DIR, "imageset")  # Path to folder with unknown images

# ✅ Ensure required files exist
if not os.path.exists(KNOWN_FACE_PATH):
    raise FileNotFoundError(f"❌ Known face image not found: {KNOWN_FACE_PATH}")
if not os.path.exists(IMAGESET_FOLDER):
    raise FileNotFoundError(f"❌ Image folder not found: {IMAGESET_FOLDER}")

# ✅ Load known face encoding
print("🔄 Loading known face...")
known_image = face_recognition.load_image_file(KNOWN_FACE_PATH)
known_encodings = face_recognition.face_encodings(known_image)

# ❗ Ensure at least one face is detected in the known image
if len(known_encodings) == 0:
    raise ValueError("❌ No face found in the known image!")

known_encoding = known_encodings[0]  # Store the known face encoding

# ✅ Get list of images to process
image_files = [f for f in os.listdir(IMAGESET_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# 🎯 Function to process an image
def process_image(image_filename):
    """Checks if an image matches the known face."""
    image_path = os.path.join(IMAGESET_FOLDER, image_filename)

    try:
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image, model="hog")  # Faster face detection

        for encoding in encodings:
            if face_recognition.compare_faces([known_encoding], encoding, tolerance=0.35)[0]:
                return image_filename  # Return the matched image name

    except Exception:
        return None  # Ignore errors and move to the next image

    return None  # No match found

# 🚀 Run Parallel Processing
if __name__ == "__main__":
    start_time = time.time()

    with multiprocessing.Pool(processes=4) as pool:  # Use 4 cores for speed
        results = pool.map(process_image, image_files)

    # ✅ Get only matched images
    matched_images = [img for img in results if img]

    if matched_images:
        print(f"\n✅ Matched Image(s): {matched_images}")
    else:
        print("\n❌ No Match Found.")

    print(f"⏱ Execution Time: {round(time.time() - start_time, 2)} seconds")