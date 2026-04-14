import os
import random
import shutil

# paths
image_dir = "dataset/images"
label_dir = "dataset/labels"

# create folders
for split in ["train", "valid"]:
    os.makedirs(f"{image_dir}/{split}", exist_ok=True)
    os.makedirs(f"{label_dir}/{split}", exist_ok=True)

# get files
images = [f for f in os.listdir(image_dir) if f.endswith(".jpg") or f.endswith(".png")]

random.shuffle(images)

split_idx = int(0.8 * len(images))  # 80% train

train_files = images[:split_idx]
val_files = images[split_idx:]

def move_files(files, split):
    for file in files:
        name = os.path.splitext(file)[0]

        # move image
        shutil.move(f"{image_dir}/{file}", f"{image_dir}/{split}/{file}")

        # move label
        label_file = f"{name}.txt"
        shutil.move(f"{label_dir}/{label_file}", f"{label_dir}/{split}/{label_file}")

move_files(train_files, "train")
move_files(val_files, "valid")

print("✅ Dataset split done!")