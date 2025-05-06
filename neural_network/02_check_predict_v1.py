#!/usr/bin/env python3
import os

def main():
    labels_dir = 'datasets/02_auto_predictions_v1/labels'
    images_dir = 'datasets/00_original'
    no_plate = []
    multiple = []

    # Make sure the labels folder exists
    if not os.path.isdir(labels_dir):
        print(f"❌ Labels directory not found: {labels_dir}")
        return
    
    # Make sure the images folder exists
    if not os.path.isdir(images_dir):
        print(f"❌ Images directory not found: {images_dir}")
        return

    for fname in os.listdir(images_dir):
        if not fname.endswith('.jpg'):
            continue

        label_filename = os.path.splitext(fname)[0] + '.txt'
        label_path = os.path.join(labels_dir, label_filename)

        if not os.path.isfile(label_path):
            no_plate.append(fname)
            continue

        with open(label_path, 'r') as f:
            lines = [l for l in f.read().splitlines() if l.strip()]

        if len(lines) > 1:
            multiple.append(fname)

    # No plates
    for fname in no_plate:
        # Copy the images yo the datasets/03_manual_v2/0_plate/images folder
        os.system(f'cp {os.path.join(images_dir, fname)} datasets/03_manual_v2/0_plate/images')
        print(f"❌ No plate found in: {fname}")

    # 2 plate
    for fname in multiple:
        # Copy the images yo the datasets/03_manual_v2/2_plate/images folder
        os.system(f'cp {os.path.join(images_dir, fname)} datasets/03_manual_v2/2_plate/images')
        # Copy the labels yo the datasets/03_manual_v2/2_plate/labels folder
        os.system(f'cp {os.path.join(labels_dir, os.path.splitext(fname)[0] + ".txt")} datasets/03_manual_v2/2_plate/labels')

if __name__ == '__main__':
    main()
