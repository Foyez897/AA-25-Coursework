import os
import csv
import time
import face_recognition
import multiprocessing
from tqdm import tqdm

# ✅ Ensure macOS/Linux compatibility
if __name__ == "__main__":
    try:
        multiprocessing.set_start_method("spawn")  # Avoid RuntimeError
    except RuntimeError:
        pass  

# 📂 Define Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_FACE_PATH = os.path.join(BASE_DIR, "known_man.jpg")
IMAGESET_FOLDER = os.path.join(BASE_DIR, "imageset")
CSV_RESULTS_FILE = os.path.join(BASE_DIR, "face_recognition_results.csv")
LOG_FILE = os.path.join(BASE_DIR, "face_recognition_log.txt")

# 🛠 Ensure known face and imageset exist
if not os.path.exists(KNOWN_FACE_PATH):
    raise FileNotFoundError(f"❌ Error: Known face image not found: {KNOWN_FACE_PATH}")
if not os.path.exists(IMAGESET_FOLDER):
    raise FileNotFoundError(f"❌ Error: Directory not found: {IMAGESET_FOLDER}")

# ✅ Load known face encoding once
print("🔄 Loading known face...")
known_image = face_recognition.load_image_file(KNOWN_FACE_PATH)
known_encoding = face_recognition.face_encodings(known_image)[0]

# 📸 Get list of image files
image_files = [f for f in os.listdir(IMAGESET_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

print(f"✅ {len(image_files)} images found for processing.")

# 🎯 Function to process each image
def process_image(image_filename, known_encoding):
    """Processes an image to check if it matches the known face (with stricter criteria)."""
    image_path = os.path.join(IMAGESET_FOLDER, image_filename)

    try:
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            return (image_filename, "No Face Detected", 0)

        # Use distance scoring instead of direct comparison
        face_distances = face_recognition.face_distance([known_encoding], encodings[0])

        # Set a more strict threshold (e.g., 0.4 instead of 0.6)
        if face_distances[0] < 0.4:
            return (image_filename, "Matched", round(face_distances[0], 3))
        else:
            return (image_filename, "No Match", round(face_distances[0], 3))

    except Exception as e:
        return (image_filename, f"Error: {str(e)}", 0)

# 🚀 **Run Parallel Processing**
if __name__ == "__main__":
    start_time = time.time()

    with multiprocessing.Pool() as pool:
        results = list(tqdm(pool.starmap(process_image, [(img, known_encoding) for img in image_files]), total=len(image_files), desc="Processing Images"))

    # ✅ Save results to CSV
    with open(CSV_RESULTS_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Image Name", "Match Status", "Processing Time (s)"])
        writer.writerows(results)

    # ✅ Log unmatched and no face detected images
    with open(LOG_FILE, "w", newline="") as log_file:
        writer = csv.writer(log_file)
        writer.writerow(["Status", "Image Name"])
        for image_name, status, _ in results:
            if status in ["No Face Detected", "No Match"]:
                writer.writerow([status, image_name])

    total_time = round(time.time() - start_time, 3)
    print(f"\n✅ Parallel Processing Complete in {total_time} seconds.")
    print(f"📁 Results saved to: {CSV_RESULTS_FILE}")
    print(f"📄 Log file created: {LOG_FILE}")