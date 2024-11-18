"""
Author: Jakub Pietrzak, 2024

File collects various logic correlated to spectrogram processing.
"""

from io import BytesIO

import librosa
import numpy as np
from PIL import Image
from librosa import feature
from matplotlib import pyplot as plt
from src.audio.audio_data import AudioData

from src.constants import SPECTROGRAM_WIDTH, SPECTROGRAM_HEIGHT, DENOISE_FREQ_HIGH_CUT

def gen_spectrogram(audio:AudioData, mel:bool=False,
                    show_axis: bool = False, width: int = SPECTROGRAM_WIDTH,
                    height: int = SPECTROGRAM_HEIGHT) -> np.array:
    """
    Generates a normal spectrogram from audio data.
    Args:
        audio_data (np.array): Input audio signal as a NumPy array.
        sample_rate (int): Sample rate of the audio signal.
        show_axis (bool, optional): If True, display axes on the plot. Defaults to False.
        width (int, optional): Width of the output image in pixels. Defaults to 400.
        height (int, optional): Height of the output image in pixels.
    Returns:
        np.array: NumPy array representing the spectrogram image.
    """
    dpi = 100
    if mel:
        s=feature.melspectrogram(y=audio.audio_signal, sr=audio.sample_rate,
                                       n_fft=4096, hop_length=512, n_mels=512,
                                       fmax=DENOISE_FREQ_HIGH_CUT)
        s_db = librosa.power_to_db(s, ref=np.max)
    else:
        s = librosa.stft(audio.audio_signal, n_fft=4096, hop_length=512)
        s_db = librosa.amplitude_to_db(np.abs(s), ref=np.max)

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)

    if mel:
        img = librosa.display.specshow(s_db, sr=audio.sample_rate, fmax=DENOISE_FREQ_HIGH_CUT,
                                       x_axis='time', y_axis='mel', ax=ax)
    else:
        img = librosa.display.specshow(s_db, sr=audio.sample_rate, x_axis='time',
                                       y_axis='log', ax=ax)

    if show_axis:
        plt.colorbar(img, format='%+2.0f dB')
        plt.title('Spectrogram')
    else:
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)

    image = Image.open(buf).convert('RGB')
    image_array = np.array(image)

    buf.close()
    plt.close(fig)

    return image_array


def save_spectrogram(spectrogram: np.ndarray, file_path: str):
    """
    Saves a spectrogram image to a file.

    Args:
        spectrogram (np.ndarray): Spectrogram to save as an image.
        file_path (str): Path to save the spectrogram image file.
    """
    plt.imshow(spectrogram)
    plt.axis('off')
    plt.savefig(file_path, bbox_inches='tight', pad_inches=0)
    plt.close()
