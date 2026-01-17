from src.utils.logger import log
from src.tests import (
    test_create_audio_file,
    test_visualize_amplitude,
    test_visualize_frequencies,
    test_visualize_spectogram,
    test_fft,
)


def test1_audio():
    print("")
    log(msg="test1_audio", color="yellow")
    test_create_audio_file(audio_filepath="src/assets/audio_files/new_audio.wav")
    print("")


def test2_visualization():
    print("")
    log(msg="test2_visualization", color="yellow")

    test_visualize_amplitude(
        audio_filepath="src/assets/audio_files/audio.wav",
        img_filepath="src/assets/img_files/audio_amplitude.png",
    )
    test_visualize_frequencies(
        audio_filepath="src/assets/audio_files/audio.wav",
        img_filepath="src/assets/img_files/audio_frequencies.png",
    )
    test_visualize_spectogram(
        audio_filepath="src/assets/audio_files/audio.wav",
        img_filepath="src/assets/img_files/audio_spectogram.png",
    )
    print("")


def test3_fft():
    print("")
    log(msg="test3_fft", color="yellow")

    test_fft(
        audio_filepath="src/assets/audio_files/fft_test_audio.wav",
        spectogram_img_filepath="src/assets/img_files/fft_test_spectogram.png",
        frequencies_img_filepath="src/assets/img_files/fft_test_frequencies.png",
        amplitudes_img_filepath="src/assets/img_files/fft_test_amplitudes.png",
        sine_frequency_amplitudes={
            1000: 2000,
            1001: 2000,
        },
    )
    print("")


if __name__ == "__main__":
    test3_fft()
