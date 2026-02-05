import random
import os
import json
import argparse
from dataclasses import dataclass
from datetime import datetime

# Referência https://wiki.seg.org/wiki/Seismic_Facies_Classification
DICT_EVENTS = {
    'seismic': [
        'a seismic section', 'a seismic image', 'subsurface model', 'a slice',
        'a section', 'a 2D section', '2D subsurface model',
        'a subsurface representation', 'seismic model', 'a 2D seismic model',
    ],
    'casual': [
        'we see here', 'this image represents', 'we observe here',
        'this image demonstrates', 'this depicts', '',
    ],
    'sigmoid': [
        'a sigmoid', 'a clinoform', 'progradational geometry',
        'a sigmoidal clinoform set', 'an oblique clinoform pattern',
        'forward-prograding geometry',
    ],
    'shingled': [
        'overlapping geometry', 'superposed structure', 'shingled reflection',
        'imbricated reflection sets', 'shingled stratification',
        'layer-on-layer reflection geometry',
    ],
    'subparallel': [
        'nearly parallel reflection set', 'almost parallel reflectors',
        'weakly dipping layers', 'gently converging reflections',
        'subhorizontal bedding pattern', 'mildly inclined strata',
        'semi-parallel internal geometry', 'uniformly stratified reflections',
        'near-parallel lamination',
    ],
    'parallel': [
        'a parallel geometry', 'continuous horizontal reflections', 'a planar geometry',
        'an uniform layering pattern', 'a parallel-bedded strata',
        'concordant seismic layering', 'a tabular reflection pattern',
        'laterally uniform bedding', 'a parallel-laminated unit',
        'an horizontally layered sequence',
    ],
    'divergent': [
        'a divergent bedform geometry', 'a spreading stratigraphic unit',
        'diverging seismic pattern', 'flaring reflection geometry',
        'a fanning reflection geometry', 'thickening wedge pattern',
        'divergent foreset reflections', 'differentially dipping reflectors',
    ],
    'mounded': [
        'mounded geometry', 'domed structure', 'rounded pattern',
        'positive-relief geometry', 'convex-up reflection geometry',
        'mounded depositional body', 'positive-relief feature',
        'lenticular reflection pattern', 'dome-shaped seismic pattern',
    ],
    'deformed': [
        'disturbed reflection zone', 'folded reflector package',
        'distorted reflection set', 'structurally disturbed reflections',
        'a folded and faulted strata', 'deformation-related geometry',
        'a warped reflection package', 'deformed structure', 'distorted seismic face',
    ],
    'hummocky': [
        'a rugged reflector package', 'a corrugated seismic unit.',
        'a hummocky cross-stratified pattern', 'a low-relief mound-and-swale structure',
        'an uneven depositional surface', 'gently rolling internal reflections',
        'a corrugated seismic texture',
    ],
    'chaotic': [
        'chaotic reflections', 'an undefined seismic structure', 'a chaotic pattern',
        'undefined internal geometry', 'chaotic internal geometry',
        'internal structuraly disturbed reflexions',
    ],
    'chaotic-channels': [
        'disordered reflection patterns indicative of potential meandering channels',
        'irregular seismic reflections suggestive of channel systems',
        'undefined internal geometry with possibility of containing channels',
        'complex and chaotic reflection patterns indicating possible presence of channels',
        'chaotic seismic reflections potentially indicative of meandering channel systems',
    ],
    'wavy': [
        'a wavy structure', 'wavy seismic reflection geometry', 'wave-like seismic unit',
        'undulating bedding configuration', 'undulatory reflector pattern',
        'imbricated reflection sets', 'layer-on-layer reflection geometry',
    ],
    'connectors': ['of', 'with', 'containing', 'presenting', 'exhibiting', 'featuring',
                   'characterized by', 'comprising'],
    #'plural_connectors':   [' of', ' with', ' containing', ' presenting', ' exhibiting'],
}

POSSIBLE_LABELS = ['sigmoid', 'shingled', 'subparallel', 'parallel', 'divergent',
                   'mounded', 'deformed', 'hummocky', 'chaotic', 'wavy', ]


def get_filename(label: str) -> str:
    dt = datetime.now()

    filename = f"{label}_{dt.year}-{dt.month:02}-{dt.day:02}_" + \
        f"{dt.hour:02}-{dt.minute:02}-{dt.microsecond}"
    return f'{filename}.json'

def is_plural(seismic_caption: str) -> bool:
    #if seismic_caption[-1] == 's':
    if seismic_caption[0:3] == "an " or seismic_caption[0:2] == "a ":
        return False
    return True

@dataclass
class CaptionGenerator:
    total_files: int
    output_dir: str
    min_captions_file: int = 2
    max_captions_file: int = 7

    def select_caption(self, label):
        possible_captions = DICT_EVENTS[label]

        return random.choice(possible_captions)

    def select_random_label(self) -> str:
        selected_label = random.choice(POSSIBLE_LABELS)
        return selected_label

    def create_caption(self, label_face: str) -> str:
        # caption = f"{self.select_caption('casual')} a {self.select_caption('seismic')}"
        caption = self.select_caption('seismic')

        selected_caption = self.select_caption(label_face)
        
        connector = self.select_caption('connectors')
        if is_plural(selected_caption):
            # connector = self.select_caption('plural_connectors')
            caption += f' {connector} {selected_caption}'
        else:
            # connector = self.select_caption('singular_connectors')
            article = 'an' if selected_caption.lower()[0] in 'aeiou' else 'a'
            caption += f' {connector} {article} {selected_caption}'

        print(caption.strip())
        return f'{caption.strip()}.'

    def generate_captions_for_label(self, label: str):
        n_captions_file = random.randint(
            self.min_captions_file, self.max_captions_file)

        captions = []

        for _ in range(n_captions_file):
            cap = self.create_caption(label)
            captions.append(cap)

        return captions    

    def save_captions_for_label(self, label: str, captions: list[str]):
        dir_captions = self.output_dir
        os.makedirs(dir_captions, exist_ok=True)

        filename = get_filename(label)

        dict_captions = {
            'captions': captions,
            'label': label
        }

        full_filename = os.path.join(dir_captions, filename)

        with open(full_filename, 'w') as fout:
            json.dump(dict_captions, fout, indent=4)

        print(full_filename, "saved successfully.")

    def generate_captions(self) -> None:
        for _ in range(self.total_files):

            label = self.select_random_label()

            captions = self.generate_captions_for_label(label)

            self.save_captions_for_label(label, captions)


def main():
    parser = argparse.ArgumentParser('Caption generation tool.')

    parser.add_argument('-t', '--total_files', type=int, required=True,
                        help='Number of files with captions to generate.')
    parser.add_argument('-o', '--output_dir', type=str, required=True,
                        help='Output directory of captions.')
    parser.add_argument('-m', '--min_captions_file', type=int, default=2,
                        help='Minimum number of captions to generate per json file.')
    parser.add_argument('-M', '--max_captions_file', type=int, default=7,
                        help='Max number of captions to generate per json file.')
    args = parser.parse_args()

    caption_gen = CaptionGenerator(
        args.total_files, args.output_dir,
        args.min_captions_file, args.max_captions_file)

    caption_gen.generate_captions()


if __name__ == "__main__":
    main()
