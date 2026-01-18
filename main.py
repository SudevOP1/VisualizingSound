from src.utils.logger import log
from src.tests import *


def test1_audio():
    """
    creates basic .wav file
    """
    print("")
    log(msg="test1_audio", color="yellow")
    test_create_audio_file(audio_filepath="src/assets/audio_files/new_audio.wav")
    print("")


def test2_visualization():
    """
    tests all 3 visualization methods
    amplitude, frequencies and spectogram
    """
    print("")
    log(msg="test2_visualization", color="yellow")

    test_visualize_amplitude(
        audio_filepath="src/assets/audio_files/audio.wav",
        img_filepath="src/assets/img_files/audio_amplitude_visualization.png",
    )
    test_visualize_frequencies(
        audio_filepath="src/assets/audio_files/audio.wav",
        img_filepath="src/assets/img_files/audio_frequencies_visualization.png",
    )
    test_visualize_spectogram(
        audio_filepath="src/assets/audio_files/audio.wav",
        img_filepath="src/assets/img_files/audio_spectogram_visualization.png",
    )
    print("")


def test3_fft():
    """
    creates audio of beat frequency of 1000, 1001 Hz
    then applies fft and creates frequency visualization
    """
    print("")
    log(msg="test3_fft", color="yellow")

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
        img_filepath="src/assets/img_files/beat_frequency_audio_frequencies_visualization.png",
        min_frequency=0,
        max_frequency=32,
    )
    print("")


def test4_hann_window():
    """
    creates audio of beat frequency of 1000, 1001 Hz
    then applies fft with and without hann window
    to create frequency visualization
    """
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
        img_filepath="src/assets/img_files/beat_frequency_audio_frequency_visualization_without_hann_window.png",
        hann_window=False,
        min_frequency=0,
        max_frequency=32,
    )
    test_visualize_frequencies(
        audio_filepath=audio_filepath,
        img_filepath="src/assets/img_files/beat_frequency_audio_frequency_visualization_with_hann_window.png",
        hann_window=True,
        min_frequency=0,
        max_frequency=32,
    )
    print("")


if __name__ == "__main__":
    for test in [
        # test1_audio,
        # test2_visualization,
        test3_fft,
        test4_hann_window,
    ]:
        test()
