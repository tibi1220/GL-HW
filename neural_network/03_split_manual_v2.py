import os

IMAGES_DIR = "datasets/00_original"
LABELS_DIR = "datasets/03_manual_v2/correct/labels"

TRAIN_DIR = "datasets/03_manual_v2/train"
VAL_DIR = "datasets/03_manual_v2/val"

IMAGES_SUBDIR = "images"
LABELS_SUBDIR = "labels"

TRAIN_RATE = 0.8

def main():
    # Create train and val folders if they don't exist
    os.makedirs(TRAIN_DIR, exist_ok=True)
    os.makedirs(VAL_DIR, exist_ok=True)

    # Create images and labels folders inside train and val folders
    os.makedirs(os.path.join(TRAIN_DIR, IMAGES_SUBDIR), exist_ok=True)
    os.makedirs(os.path.join(TRAIN_DIR, LABELS_SUBDIR), exist_ok=True)
    os.makedirs(os.path.join(VAL_DIR, IMAGES_SUBDIR), exist_ok=True)
    os.makedirs(os.path.join(VAL_DIR, LABELS_SUBDIR), exist_ok=True)

    # Get the list of all files in the correct folder
    all_labels = os.listdir(LABELS_DIR)
    all_images = [f.replace(".txt", ".jpg") for f in all_labels]

    # Split the files into train and val sets
    num_train = int(len(all_images) * TRAIN_RATE)
    train_images = all_images[:num_train]
    val_images = all_images[num_train:]
    train_labels = all_labels[:num_train]
    val_labels = all_labels[num_train:]

    # Copy the images and labels to the train folder
    for image in train_images:
        src_image = os.path.join(IMAGES_DIR, image)
        dst_image = os.path.join(TRAIN_DIR, IMAGES_SUBDIR, image)
        os.system(f"cp {src_image} {dst_image}")

    for label in train_labels:
        src_label = os.path.join(LABELS_DIR, label)
        dst_label = os.path.join(TRAIN_DIR, LABELS_SUBDIR, label)
        os.system(f"cp {src_label} {dst_label}")

    # Copy the images and labels to the val folder
    for image in val_images:
        src_image = os.path.join(IMAGES_DIR, image)
        dst_image = os.path.join(VAL_DIR, IMAGES_SUBDIR, image)
        os.system(f"cp {src_image} {dst_image}")

    for label in val_labels:
        src_label = os.path.join(LABELS_DIR, label)
        dst_label = os.path.join(VAL_DIR, LABELS_SUBDIR, label)
        os.system(f"cp {src_label} {dst_label}")

if __name__ == "__main__":

    main()