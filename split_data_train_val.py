import os
import random
import sys
import re
import argparse
import shutil
from collections import Counter
from tqdm import main, tqdm
from seisfacies import FIRST_INLINE_VAL, LAYERS_SEISFACE
from dict_synonyms import FULL_FACIES_NAMES

EXTRA_FOLDERS = ['jpg', 'npy']


def get_inline_num(image_name: str) -> int:
    match = re.search(r'_il_[0-9]+', image_name)
    if match:
        il_img = match[0] 
        il_number = int(il_img[4:])
        return il_number
    else:
        match = re.search(r'_x[0-9]+_[0-9]+', image_name)
        if match:
            il_img = match[0]
            il_number = int(il_img.split('_')[-1])
            # if 'sig' in image_name:
            #     print(il_number)
            return il_number
        else:
            print("Error. Invalid inline.")
            sys.exit(1)


def remove_n_images(face: str, number_to_remove: int, folder_images: str
                    ) -> None:
    images_names = os.listdir(folder_images)
    images_names_face = [
        filename for filename in images_names if face in filename
    ]
    random.shuffle(images_names_face)

    for i in range(number_to_remove):
        filepath = os.path.join(folder_images, images_names_face[i])
        os.remove(filepath)
        # shutil.rmtree(filepath)

def get_facies_samples(folder_images):
    images_names = os.listdir(folder_images)

    labels_facies = []

    for img_name in images_names:
        match = re.search(r's-([a-z]+)', img_name)
        if not match:
            continue
        label = FULL_FACIES_NAMES[match.group(1)[:3]]
        labels_facies.append(label)
    return labels_facies


def balance_folder(folder_images: str, min_samples=None):
    labels_facies = get_facies_samples(folder_images)

    class_count = Counter(labels_facies)

    if min_samples is None:
        min_samples = min(class_count.values())

    print("Balancing classes...")
    for face in tqdm(class_count):
        number_to_remove = class_count[face] - min_samples
        remove_n_images(face[:3], number_to_remove, folder_images)


def remove_extra_folders(folders_layers):

    for c in folders_layers:

        for extra_f in EXTRA_FOLDERS:
            folder_to_delete = os.path.join(
                input_folder, str(c), extra_f)

            shutil.rmtree(folder_to_delete, ignore_errors=True)
            print(folder_to_delete, "removed")


def get_idx_split(image_list, split_inline):
    idx_to_split = len(image_list)

    # Encontra o índice onde o conjunto de validação começa
    for i, img in enumerate(image_list):
        inline = get_inline_num(img)

        if inline >= split_inline:
            idx_to_split = i 
            break
    return idx_to_split


def split_train_val(image_list, split_inline):
    # Encontra o índice onde o conjunto de validação começa
    idx_to_split = get_idx_split(image_list, split_inline)

    # Remove o conjunto de validação e mantém só o treino
    images_train = image_list[:idx_to_split]

    images_val = image_list[idx_to_split:]

    return images_train, images_val


def copy_images(images_train, folder_src_layer, folder_dst_training):
    for img_name in tqdm(images_train):
        src_file = os.path.join(folder_src_layer, img_name)

        dst_file = os.path.join(folder_dst_training, img_name)

        shutil.copy(src_file, dst_file)


def count_instances(folder_train_val, count_file_name):
    count_file_path = os.path.join(args.output_folder, 'instance_count')
    os.makedirs(count_file_path, exist_ok=True)

    count_file_path = os.path.join(count_file_path, count_file_name)
    count_file = open(count_file_path, 'w')

    seismic_faces = [f[2:].split('_')[0]
                     for f in os.listdir(folder_train_val)]

    print("======== Number of instances =========\n", file=count_file)
    for current_face in set(seismic_faces):
        num_faces = seismic_faces.count(current_face)
        print(f"{current_face} instances: {num_faces}", file=count_file)

    count_file.close()
    print(count_file_path, "saved.")


def main(args):
    # folders_layers = sorted(list(layer_seisface.keys()))
    folders_layers = [
        filename for filename in os.listdir(args.input_folder)
         if os.path.isdir(os.path.join(args.input_folder, filename))
    ]

    remove_extra_folders(folders_layers)

    # Go through all layers
    for c in folders_layers:
        folder_src_layer = FOLDER_IMAGES.format(c)

        folder_dst_train = FOLDER_TRAINING
        folder_dst_val = FOLDER_VALIDATION

        os.makedirs(folder_dst_train, exist_ok=True)
        os.makedirs(folder_dst_val, exist_ok=True)

        images_layer = sorted(os.listdir(folder_src_layer),
                              key=get_inline_num)

        images_train, images_val = split_train_val(
            images_layer, first_inline_validation)

        print(f"Copying training images in layer {c}...")
        copy_images(images_train, folder_src_layer, folder_dst_train)

        print(f"Copying validation images in layer {c}...")
        copy_images(images_val, folder_src_layer, folder_dst_val)

    if args.balance or args.train_samples_num is not None:
        balance_folder(FOLDER_TRAINING, args.train_samples_num)
    if args.balance or args.val_samples_num is not None:
        balance_folder(FOLDER_VALIDATION, args.val_samples_num)

    count_instances(FOLDER_TRAINING, 'train_split.txt')
    count_instances(FOLDER_VALIDATION, 'validation_split.txt')


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Remove images from folder.')

    parser.add_argument('-i', '--input_folder', type=str, required=True,
                        help='Folder with images in layers.')
    parser.add_argument('-o', '--output_folder', type=str, required=True,
                        help='Folder with images split in training and test.')
    parser.add_argument('-c', '--current_cube', type=str, required=True,
                        help='Seismic cube name.')
    parser.add_argument('-b', '--balance', action='store_true',
                        help='Flag to indicate if data is balanced.')
    parser.add_argument('-t', '--train_samples_num', type=int, default=None,
                        help='Number of samples by class training.')
    parser.add_argument('-v', '--val_samples_num', type=int, default=None,
                        help='Number of samples by class validation.')
    args = parser.parse_args()
    assert args.current_cube in list(LAYERS_SEISFACE.keys()), \
        "Invalid seismic volume name."

    input_folder = args.input_folder
    output_folder = args.output_folder
    current_cube = args.current_cube

    FOLDER_IMAGES = os.path.join(input_folder, '{}/janelas/') # layer

    FOLDER_TRAINING = os.path.join(output_folder, 'training') # face

    FOLDER_VALIDATION = os.path.join(output_folder, 'validation') # face

    # PERCENTAGE_TRAIN = 0.8
    first_inline_validation = FIRST_INLINE_VAL[current_cube]

    layer_seisface = LAYERS_SEISFACE[current_cube]

    main(args)
