# organize_dataset.py
# Organizes downloaded PlantVillage dataset into correct structure

import os
import shutil
from pathlib import Path

print("🌱 PlantVillage Dataset Organizer")
print("="*60)

# CHANGE THIS to where you extracted the downloaded dataset
SOURCE_DIR = r"C:\Users\adity\Documents\Projects\plant-disease-AI"  # CHANGE THIS PATH!

# This is where we want the organized dataset
TARGET_DIR = "dataset"

print(f"\n📂 Source: {SOURCE_DIR}")
print(f"📁 Target: {TARGET_DIR}")

# Check if source exists
if not os.path.exists(SOURCE_DIR):
    print(f"\n❌ ERROR: Source directory not found!")
    print(f"   Please update SOURCE_DIR in the script to match where you extracted the dataset")
    exit(1)

# Create target directory
os.makedirs(TARGET_DIR, exist_ok=True)

print("\n🔍 Scanning source directory...")

# Find all image folders
# PlantVillage dataset usually has structure like:
# - color/Tomato___Early_blight/*.jpg
# - OR directly: Tomato___Early_blight/*.jpg

image_folders = []
image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}

# Method 1: Check if there's a 'color' subfolder
color_dir = os.path.join(SOURCE_DIR, 'color')
if os.path.exists(color_dir):
    print("✓ Found 'color' subdirectory")
    search_dir = color_dir
else:
    print("✓ Searching in main directory")
    search_dir = SOURCE_DIR

# Find all class folders
for item in os.listdir(search_dir):
    item_path = os.path.join(search_dir, item)
    if os.path.isdir(item_path):
        # Check if it contains images
        files = os.listdir(item_path)
        has_images = any(Path(f).suffix.lower() in image_extensions for f in files)
        if has_images:
            image_folders.append((item, item_path))

print(f"\n✓ Found {len(image_folders)} disease classes")

if len(image_folders) == 0:
    print("\n❌ No image folders found!")
    print("   Please check your SOURCE_DIR path")
    exit(1)

print("\n📋 Classes found:")
for i, (class_name, _) in enumerate(image_folders[:10], 1):
    print(f"  {i}. {class_name}")
if len(image_folders) > 10:
    print(f"  ... and {len(image_folders) - 10} more")

# Ask for confirmation
print(f"\n⚠️  This will copy images to: {TARGET_DIR}")
response = input("Continue? (yes/no): ").strip().lower()

if response != 'yes':
    print("❌ Cancelled")
    exit(0)

# Copy images to organized structure
print("\n📦 Copying images...")
total_images = 0

for class_name, source_path in image_folders:
    # Create target folder
    target_path = os.path.join(TARGET_DIR, class_name)
    os.makedirs(target_path, exist_ok=True)
    
    # Copy images
    image_files = [f for f in os.listdir(source_path) 
                   if Path(f).suffix.lower() in image_extensions]
    
    for img_file in image_files:
        src = os.path.join(source_path, img_file)
        dst = os.path.join(target_path, img_file)
        
        # Copy file (don't move, keep original)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
    
    total_images += len(image_files)
    print(f"  ✓ {class_name}: {len(image_files)} images")

print("\n" + "="*60)
print(f"✅ Organization complete!")
print(f"📊 Total images organized: {total_images}")
print(f"📁 Dataset location: {TARGET_DIR}")
print("\n💡 Next step: Run 'python train_model.py' to train the model!")
print("="*60)