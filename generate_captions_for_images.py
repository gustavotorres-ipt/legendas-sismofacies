import os
import re
import json
import argparse
from tqdm import tqdm
from caption_generator import CaptionGenerator, FaciesInfo
from dataclasses import asdict
from dict_synonyms import FULL_FACIES_NAMES

def extract_flag(regex, img_name):
    match = re.search(regex, img_name)
    found_value = match.group(1) if match and match.group(1) else None

    if found_value is None:
        return None
    return 'low' if found_value =='L' else 'high'


def extract_info_from_filename(filename: str) -> FaciesInfo:
    match = re.search(r's-([a-z]+)', filename)
    if not match:
        return FaciesInfo('')
    label = FULL_FACIES_NAMES[match.group(1)]

    amplitude = extract_flag(r'ampl-([HL])', filename)
    freq      = extract_flag(r'freq-([HL])', filename)
    noise     = extract_flag(r'nois-([HL])', filename)
    return FaciesInfo(label, amplitude, freq, noise)


def generate_captions_for_imgs(path_images, path_captions):
    caption_generator = CaptionGenerator(0, path_captions)
    images = os.listdir(path_images)
    os.makedirs(path_captions, exist_ok=True)

    print(f'Generating captions in {path_captions}...')

    for img_filename in tqdm(images):

        fullpath_caption = os.path.join(
            path_captions, f'{img_filename[:-4]}.json')

        info_facies = extract_info_from_filename(img_filename)
        captions = caption_generator.generate_captions_for_label(info_facies)

        dict_captions = asdict(info_facies)
        dict_captions['captions'] = captions

        with open(fullpath_caption, 'w') as fout:
            json.dump(dict_captions, fout, indent=4)
            # print(fullpath_caption, "saved.")


def main():
    parser = argparse.ArgumentParser('Generate captions for images.')

    parser.add_argument('-i', '--images_folder', type=str, required=True,
                        help='Images folder.')
    parser.add_argument('-c', '--captions_folder', type=str, required=True,
                        help='Output folder with captions.')
    args = parser.parse_args()

    images_folder = os.path.normpath(args.images_folder)
    captions_folder = os.path.normpath(args.captions_folder)

    folder_imgs_train = os.path.join(images_folder, 'training')
    folder_captions_train = os.path.join(captions_folder, 'training')
    generate_captions_for_imgs(folder_imgs_train, folder_captions_train)

    folder_imgs_val = os.path.join(images_folder, 'validation')
    folder_captions_val = os.path.join(captions_folder, 'validation')
    generate_captions_for_imgs(folder_imgs_val, folder_captions_val)


if __name__ == "__main__":
    main()
