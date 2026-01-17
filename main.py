from src.utils.logger import log
from src.tests import *


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
        audio_filepath="src/assets/audio_files/beat_frequency_audio.wav",
        spectogram_img_filepath="src/assets/img_files/fft_test_spectogram.png",
        frequencies_img_filepath="src/assets/img_files/fft_test_frequencies.png",
        amplitudes_img_filepath="src/assets/img_files/fft_test_amplitudes.png",
        sine_frequency_amplitudes={
            1000: 2000,
            1001: 2000,
        },
    )
    print("")


def test4_hann_window():
    print("")
    log(msg="test4_hann_window", color="yellow")

    audio_filepath = "src/assets/audio_files/beat_frequency_audio.wav"
    samples = generate_wave_samples(
        duration=1.0,  # 1 second for less calculation time
        sine_frequency_amplitudes={
            5: 2000,
            6: 2000,
        },
    )
    test_create_audio_file(audio_filepath=audio_filepath, samples=samples)

    test_visualize_frequencies(
        audio_filepath=audio_filepath,
        img_filepath="src/assets/img_files/beat_frequency_visualization_without_hann_window.png",
        hann_window=False,
        min_frequency=0,
        max_frequency=32,
    )
    test_visualize_frequencies(
        audio_filepath=audio_filepath,
        img_filepath="src/assets/img_files/beat_frequency_visualization_with_hann_window.png",
        hann_window=True,
        min_frequency=0,
        max_frequency=32,
    )
    print("")


if __name__ == "__main__":
    test4_hann_window()
