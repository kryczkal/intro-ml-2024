import os
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt 
import librosa
import librosa.display
from PIL import Image




"""
Function generates mel-frequency spectrogram based on audio data. Audio data is a numpy array. It 
retrurns numpy array that represents - 
image of spectrogram.
It uses Mel scale, which is more aligned with human hearing perception. This makes it effective for
speech or voice-based tasks.
Mel scale emphasizes the lower frequencies where most of the speech information resides while 
compressing the higher frequencies.
This makes Mel spectrogram efficient for voice recognition and voice detection and emotion 
detection.
It underline sounds that human ear hears.
Mel-frequency scale, which is a linear frequency space below 1000 Hz and a logarithmic space above
1000 Hz.
"""
def gen_spectrogram(audio_data, sample_rate, save_to_file=True, 
                    save_path="./image_spectrograms/spectrogram.png", 
                    show_axis=False, width=400, height=300):
    dpi = 100
    fmax = 8000

    # Generate Mel spectrogram
    S = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate, 
                                       n_fft=4096, hop_length=512, n_mels=512, fmax=fmax)
    S_db = librosa.power_to_db(S, ref=np.max)

    # Set figure size in inches (for the given width and height in pixels)
    width_in_inches = width / dpi
    height_in_inches = height / dpi
    fig, ax = plt.subplots(figsize=(width_in_inches, height_in_inches), dpi=dpi)

    # Display Mel spectrogram with or without axis
    if show_axis:
        img = librosa.display.specshow(S_db, sr=sample_rate, fmax=fmax, 
                                       x_axis='time', y_axis='mel', ax=ax)
        plt.colorbar(img, format='%+2.0f dB')
        plt.title('Mel-Frequency Spectrogram')
    else:
        img = librosa.display.specshow(S_db, sr=sample_rate, fmax=fmax, ax=ax)
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Save to file if required
    if save_to_file:
        plt.savefig(save_path, bbox_inches='tight', pad_inches=0)

    # Save figure to a buffer and convert it to a NumPy array
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)

    # Open the buffer as an image and convert to NumPy array
    image = Image.open(buf).convert('RGB')
    image_array = np.array(image)

    # Close the buffer and figure
    buf.close()
    plt.close(fig)

    return image_array


def save_figure(file_name):
    output_directory = './image_spectrogram/spectrograms_nmels'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file_path = os.path.join(output_directory, file_name)