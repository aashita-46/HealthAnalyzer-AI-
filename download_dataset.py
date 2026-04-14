import kagglehub
import os
import shutil

print("📥 Downloading annotations...")
ann_path = kagglehub.dataset_download("thedatasith/sku110k-annotations")

print("📥 Downloading images...")
img_path = kagglehub.dataset_download("thedatasith/shelf-images-dataset")

print("Annotations at:", ann_path)
print("Images at:", img_path)

# Create your dataset folder
os.makedirs("dataset/images", exist_ok=True)
os.makedirs("dataset/annotations", exist_ok=True)

# Copy images (limit for speed)
img_files = os.listdir(img_path)[:300]   # 🔥 limit to 300 images
for f in img_files:
    src = os.path.join(img_path, f)
    dst = os.path.join("dataset/images", f)
    shutil.copy(src, dst)

# Copy annotations
for f in os.listdir(ann_path):
    src = os.path.join(ann_path, f)
    dst = os.path.join("dataset/annotations", f)
    shutil.copy(src, dst)

print("✅ Dataset ready inside /dataset")