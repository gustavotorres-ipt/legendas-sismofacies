import os
import re
import json
import random
import argparse
from tqdm import tqdm
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from dict_synonyms import SEISMIC_EVENTS, POSSIBLE_LABELS, AMPL_FREQ_NOISE

# Probability of adding frequency, amplitude or noise
PROBABILITY_ADDING_FAN = 0.5


def get_filename(info_facies) -> str:
    dt = datetime.now()

    filename = f'{info_facies.label}_'
    filename += f'{info_facies.frequency}_{info_facies.amplitude}_{info_facies.noise}'

    data_info = f"{dt.year}-{dt.month:02}-{dt.day:02}"
    time_info = f"{dt.hour:02}-{dt.minute:02}-{dt.microsecond}"
    return f'{filename}_{data_info}_{time_info}.json'


def is_plural(seismic_caption: str) -> bool:
    if seismic_caption[0:3] == "an " or seismic_caption[0:2] == "a ":
        return False
    return True


@dataclass
class FaciesInfo:
    label: str
    amplitude: Optional[str|None] = None
    frequency: Optional[str|None] = None
    noise: Optional[str|None] = None


@dataclass
class CaptionGenerator:
    total_files: int
    output_dir: str
    min_captions_file: int = 2
    max_captions_file: int = 7

    def get_freq_amp_noi_info(self, info_facies: FaciesInfo):
        # frequency, amplitude, noise info
        fan_info = []

        if (info_facies.frequency is not None
                and random.random() < PROBABILITY_ADDING_FAN
            ):
            fan_info.append(f'{info_facies.frequency} frequency')

        if (info_facies.amplitude is not None
                and random.random() < PROBABILITY_ADDING_FAN
            ):
            fan_info.append(f'{info_facies.amplitude} amplitude')

        if (info_facies.noise is not None
                and random.random() < PROBABILITY_ADDING_FAN
            ):
            fan_info.append(f'{info_facies.noise} noise')

        if len(fan_info) < 1:
            return ''

        elif len(fan_info) < 2:
            synonyms = AMPL_FREQ_NOISE[fan_info[0]]
            # Select a random synonym
            return random.choice(synonyms)

        # Select a random synonym
        fan_info_syn = [random.choice( AMPL_FREQ_NOISE[info] ) for info in fan_info]
        # Shuffle the order of the information
        random.shuffle(fan_info_syn)

        # Return in format high amplitude, high frequency and low noise
        return f"{', '.join(fan_info_syn[:-1])} and {fan_info_syn[-1]}"


    def select_caption(self, label):
        possible_captions = SEISMIC_EVENTS[label]

        return random.choice(possible_captions)

    def select_random_label(self) -> str:
        selected_label = random.choice(POSSIBLE_LABELS)
        return selected_label

    def create_caption(self, info_facies: FaciesInfo, ) -> str:
        caption = self.select_caption('seismic')

        selected_caption = self.select_caption(info_facies.label)

        connector = self.select_caption('connectors')
        caption += f' {connector} {selected_caption}'

        freq_amp_noi_info = self.get_freq_amp_noi_info(info_facies)

        connector = self.select_caption(
            'connectors details') if freq_amp_noi_info else ''
        # connector = random.choice([
        #     'with', 'containing', '. It contains',
        #     '. The seismic section has', '. The image has',
        # ]) if freq_amp_noi_info else ''

        caption = f'{caption} {connector} {freq_amp_noi_info}'
        caption = re.sub(r'\s+', ' ', caption)
        caption = re.sub(r'\s+\.', '.', caption)

        return f'{caption.strip()}.'

    def generate_captions_for_label(self, info_facies: FaciesInfo):
        n_captions_file = random.randint(
            self.min_captions_file, self.max_captions_file)
        captions = []

        for _ in range(n_captions_file):
            cap = self.create_caption(info_facies)
            captions.append(cap)

        return captions    

    def save_captions_for_label(
        self, captions: list[str], info_facies: FaciesInfo
    ):
        dir_captions = self.output_dir
        os.makedirs(dir_captions, exist_ok=True)

        filename = get_filename(info_facies)

        dict_captions = asdict(info_facies)
        dict_captions['captions'] = captions

        full_filename = os.path.join(dir_captions, filename)

        print('\n'.join(dict_captions['captions']))
        with open(full_filename, 'w') as fout:
            json.dump(dict_captions, fout, indent=4)
        print(full_filename, "saved successfully.")

    def generate_captions(self) -> None:
        possible_values = [None, 'low', 'high']

        for _ in tqdm(range(self.total_files)):
            label = self.select_random_label()
            amplitude = random.choice(possible_values) 
            frequency = random.choice(possible_values)
            noise = random.choice(possible_values)

            info_facies = FaciesInfo(label, amplitude, frequency, noise)

            captions = self.generate_captions_for_label(info_facies)
            self.save_captions_for_label(captions, info_facies)


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
