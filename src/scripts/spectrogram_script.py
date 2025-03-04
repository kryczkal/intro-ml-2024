"""
Author: Jakub Pietrzak, 2024

Modul for generating spectrograms and showing/saving it
"""

import argparse

import matplotlib.pyplot as plt
import soundfile as sf
from sklearn.pipeline import Pipeline
from src.pipeline.audio_data import AudioData

from src.pipeline.audio_cleaner import AudioCleaner
from src.pipeline.spectrogram_generator import SpectrogramGenerator
from src.scripts.spectrogram_from_npy import get_random_file_path


def process(sound_path: str = "", directory: str = "", number_of_samples: int = 1,
            output_path: str = None, show: bool = False,
            mel: bool = False, clean_data: bool = False, show_axis: bool = False):
    # pylint: disable=too-many-locals
    """
    Process function that processes the audio file, generates a spectrogram, and optionally
    cleans the data.

    Args:
        sound_path (str): Path to the audio file.
        directory (str): Path to the directory with audio files to generate randomly.
        number_of_samples (int): Number of samples to generate.
        output_path (str): Optional output path for the spectrogram image.
        show (bool): Flag to show the spectrogram using matplotlib.
        mel (bool): Flag to generate a mel-frequency spectrogram.
        clean_data (bool): Flag to clean and normalize the audio data.
        show_axis (bool): Flag to show axis on the spectrogram plot.
    """
    if not isinstance(number_of_samples, int) or number_of_samples < 1:
        number_of_samples = 1

    for i in range(number_of_samples):
        new_sound_path = sound_path
        if sound_path == "" or sound_path is None:
            new_sound_path = get_random_file_path(directory, ".wav")
        print(new_sound_path)

        data, samplerate = sf.read(new_sound_path)
        audio_data = AudioData(data, samplerate)

        if clean_data:
            transformation_pipeline = Pipeline(steps=[
                ('AudioCleaner', AudioCleaner())
            ])
            transformation_pipeline.fit([audio_data])
            audio_data = transformation_pipeline.transform([audio_data])[0]

        spectrogram = SpectrogramGenerator.gen_spectrogram(audio_data, mel, show_axis)

        # pylint: disable=line-too-long
        if output_path:
            split_path=output_path.split(".")
            SpectrogramGenerator.save_spectrogram(spectrogram, split_path[0]+str(i)+"."+split_path[1])

        if show:
            plt.imshow(spectrogram)
            plt.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            plt.show()


def main(argv: list[str]) -> None:
    """
    Main function that parses command line arguments and runs the processing.

    Args:
        argv (List[str]): List of command line arguments.
    """
    parser = argparse.ArgumentParser(description="Generates a spectrogram from an audio file.")
    parser.add_argument("--file_path", '-f', type=str, help="Path to the audio file.")
    parser.add_argument('--number', '-n', type=int,
                        help='number of samples')
    parser.add_argument('--directory', '-d', type=str,
                        help='Path to the directory with audio files.')
    parser.add_argument('--output', '-o', type=str,
                        help='Optional output file path for the spectrogram.')
    parser.add_argument('--show', '-s', action='store_true',
                        help='Show the spectrogram after generation.')
    parser.add_argument('--clean', '-c', action='store_true',
                        help='Clean and normalize the audio data.')
    parser.add_argument('--mel', '-m', action='store_true',
                        help='Generate a mel-frequency spectrogram.')
    parser.add_argument('--show_axis', '-a', action='store_true',
                        help='Show axis on the spectrogram plot.')

    args = parser.parse_args(argv)
    process(args.file_path, args.directory, args.number, args.output, args.show, args.mel,
            args.clean, args.show_axis)
