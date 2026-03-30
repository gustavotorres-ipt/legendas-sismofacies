import os
import json
import shutil
import argparse
from caption_generator import CaptionGenerator, FaciesInfo

def extract_info_from_filename(filename: str) -> FaciesInfo:

    return FaciesInfo()


def generate_captions_for_imgs(path_images, path_captions):
    caption_generator = CaptionGenerator(0, path_captions)
    images = os.listdir(path_images)
    os.makedirs(path_captions, exist_ok=True)

    # generate_captions_for_face(images, path_captions, caption_generator, face_name)

    for img_filename in images:

        fullpath_caption = os.path.join(
            path_captions, f'{img_filename[:-4]}.json')

        captions = caption_generator.generate_captions_for_label(face_name)

        dict_captions = {
            'captions': captions,
            'label': face_name
        }
        with open(fullpath_caption, 'w') as fout:
            json.dump(dict_captions, fout, indent=4)
            print(fullpath_caption, "saved.")


def generate_captions_for_face(
        images_face, path_captions_face, caption_generator, face_name
):
    for img_filename in images_face:

        fullpath_caption = os.path.join(path_captions_face, f'{img_filename[:-4]}.json')

        captions = caption_generator.generate_captions_for_label(face_name)

        dict_captions = {
            'captions': captions,
            'label': face_name
        }
        with open(fullpath_caption, 'w') as fout:
            json.dump(dict_captions, fout, indent=4)
            print(fullpath_caption, "saved.")

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
