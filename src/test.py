import wave, struct, math
from helpers import *


def test_read_wav() -> None:
    filepath = "audio_files/audio.wav"
    with wave.open(filepath, "r") as f:
        log(msg=f"filepath: {filepath}", func_name="test_read_wav", color="green")
        log(
            msg=f"f.getnchannels(): {f.getnchannels()}",
            func_name="test_read_wav",
            color="green",
        )
        log(
            msg=f"getsampwidth(): {f.getsampwidth()}",
            func_name="test_read_wav",
            color="green",
        )
        log(
            msg=f"getframerate(): {f.getframerate()}",
            func_name="test_read_wav",
            color="green",
        )
        log(
            msg=f"getnframes(): {f.getnframes()}",
            func_name="test_read_wav",
            color="green",
        )
        log(
            msg=f"getcomptype(): {f.getcomptype()}",
            func_name="test_read_wav",
            color="green",
        )
        log(
            msg=f"getcompname(): {f.getcompname()}",
            func_name="test_read_wav",
            color="green",
        )
        log(
            msg=f"getparams(): {f.getparams()}",
            func_name="test_read_wav",
            color="green",
        )
        log(
            msg=f"getmarkers(): {f.getmarkers()}",
            func_name="test_read_wav",
            color="green",
        )
        log(msg=f"rewind(): {f.rewind()}", func_name="test_read_wav", color="green")
        log(msg=f"tell(): {f.tell()}", func_name="test_read_wav", color="green")


def test_write_simple_wav() -> None:
    filepath = "audio_files/new_audio.wav"
    framerate = 44100  # samples per second
    duration = 5  # seconds
    # frequency = 350  # Hz
    amplitude = 2000  # max=32767 for 16-bit audio

    n_samples = framerate * duration

    with wave.open(filepath, "w") as f:
        f.setnchannels(1)  # mono
        f.setsampwidth(2)  # 16-bit
        f.setframerate(framerate)

        for i in range(n_samples):
            frequency = 150 if (i < n_samples / 2) else 350
            sample = amplitude * math.sin(2 * math.pi * frequency * i / framerate)
            f.writeframes(struct.pack("<h", int(sample)))


def test_create_audio_file(audio_filepath: str) -> None:

    framerate = 44100
    duration = 5
    amplitude = 2000  # max = 32767

    samples = []
    for i in range(framerate * duration):
        frequency = map_num(i, 0, framerate * duration, 20, 1000)
        samples.append(amplitude * math.sin(2 * math.pi * frequency * i / framerate))
    samples = tuple(samples)

    result_ok, result_path = create_audio_file(
        audio_filepath,
        samples,
        framerate,
        replace=True,
    )
    if not result_ok:
        log(
            msg=f"something went wrong: {result_path}",
            func_name="test_create_audio_file",
            color="green",
        )
    else:
        log(
            msg=f"audio_file created: {result_path}",
            func_name="test_create_audio_file",
            color="green",
        )


def test_visualize_amplitude(audio_filepath: str, img_filepath: str) -> None:

    result_ok, result_path = visualize_amplitude(
        audio_filepath,
        img_filepath,
        replace=True,
    )
    if not result_ok:
        log(
            msg=f"something went wrong: {result_path}",
            func_name="test_visualize_amplitude",
            color="green",
        )
    else:
        log(
            msg=f"img_file created: {result_path}",
            func_name="test_visualize_amplitude",
            color="green",
        )


def test_visualize_frequencies(audio_filepath: str, img_filepath: str) -> None:

    result_ok, result_path = visualize_frequencies(
        audio_filepath,
        img_filepath,
        replace=True,
    )
    if not result_ok:
        log(
            msg=f"something went wrong: {result_path}",
            func_name="test_visualize_frequencies",
            color="green",
        )
    else:
        log(
            msg=f"img_file created: {result_path}",
            func_name="test_visualize_frequencies",
            color="green",
        )


def test_visualize_spectogram(audio_filepath: str, img_filepath: str) -> None:

    result_ok, result_path = visualize_spectogram(
        audio_filepath,
        img_filepath,
        replace=True,
        max_frequency=5000,
    )
    if not result_ok:
        log(
            msg=f"something went wrong: {result_path}",
            func_name="test_visualize_spectogram",
            color="green",
        )
    else:
        log(
            msg=f"img_file created: {result_path}",
            func_name="test_visualize_spectogram",
            color="green",
        )


def test_fft(
    audio_filepath: str,
    spectogram_img_filepath: str,
    frequencies_img_filepath: str,
    amplitudes_img_filepath: str,
    sine_frequency_amplitudes: dict[int, int] = {},
    cosine_frequency_amplitudes: dict[int, int] = {},
    duration: float = 5.0,
) -> None:
    """
    creates an audio as a sum of sine and cosine waves of multiple frequencies
    then applies fft on it and creates spectogram, frequency, amplitude visualizations
    """

    # default sine freqs if both sine and cosine are passed empty
    if not sine_frequency_amplitudes and not cosine_frequency_amplitudes:
        # freqs of 500, 2000 Hz
        sine_frequency_amplitudes = {500: 2000, 2000: 2000}

    framerate = 44100
    num_samples = int(framerate * duration)

    # calc samples
    samples: list[float] = []
    for i in range(num_samples):
        sample = 0.0
        time_secs = i / framerate

        # sine frequencies
        for freq, amp in sine_frequency_amplitudes.items():
            sample += amp * math.sin(2.0 * math.pi * freq * time_secs)

        # cosine frequencies
        for freq, amp in cosine_frequency_amplitudes.items():
            sample += amp * math.cos(2.0 * math.pi * freq * time_secs)

        samples.append(sample)
    samples = tuple(samples)

    # creating audio file
    audio_path_ok, audio_path = create_audio_file(
        audio_filepath,
        samples,
        framerate,
        replace=True,
    )
    if not audio_path_ok:
        log(
            msg=f"something went wrong in creating audio file: {audio_path}",
            func_name="test_fft",
            color="green",
        )
        return
    log(
        msg=f"audio_file created: {audio_path}",
        func_name="test_fft",
        color="green",
    )

    # calc max_freq for visualization
    max_freq_candidates = []
    if sine_frequency_amplitudes:
        max_freq_candidates.append(max(sine_frequency_amplitudes))
    if cosine_frequency_amplitudes:
        max_freq_candidates.append(max(cosine_frequency_amplitudes))
    max_freq = max(max_freq_candidates) + 500 if max_freq_candidates else 2000

    # creating spectogram img
    spectogram_img_path_ok, spectogram_img_path = visualize_spectogram(
        audio_path,
        spectogram_img_filepath,
        replace=True,
        max_frequency=max_freq,
    )
    if not spectogram_img_path_ok:
        log(
            msg=f"something went wrong in creating spectogram img: {spectogram_img_path}",
            func_name="test_fft",
            color="green",
        )
    else:
        log(
            msg=f"img_file created: {spectogram_img_path}",
            func_name="test_fft",
            color="green",
        )

    # creating frequencies img
    frequencies_img_path_ok, frequencies_img_path = visualize_frequencies(
        audio_path,
        frequencies_img_filepath,
        replace=True,
    )
    if not frequencies_img_path_ok:
        log(
            msg=f"something went wrong in creating frequencies img: {frequencies_img_path}",
            func_name="test_fft",
            color="green",
        )
    else:
        log(
            msg=f"img_file created: {frequencies_img_path}",
            func_name="test_fft",
            color="green",
        )

    # creating amplitudes img
    amplitudes_img_path_ok, amplitudes_img_path = visualize_amplitude(
        audio_path,
        amplitudes_img_filepath,
        replace=True,
    )
    if not amplitudes_img_path_ok:
        log(
            msg=f"something went wrong in creating amplitudes img: {amplitudes_img_path}",
            func_name="test_fft",
            color="green",
        )
    else:
        log(
            msg=f"img_file created: {amplitudes_img_path}",
            func_name="test_fft",
            color="green",
        )


if __name__ == "__main__":

    def test1():
        print(f"{COLORS["yellow"]}test1:{COLORS["reset"]}")
        test_read_wav()
        test_write_simple_wav()

    def test2():
        print(f"{COLORS["yellow"]}test2:{COLORS["reset"]}")
        test_create_audio_file("audio_files/new_audio.wav")
        test_visualize_amplitude(
            "audio_files/new_audio.wav", "img_files/new_audio_amplitude.png"
        )
        test_visualize_frequencies(
            "audio_files/new_audio.wav", "img_files/new_audio_frequencies.png"
        )
        test_visualize_spectogram(
            "audio_files/audio.wav", "img_files/new_audio_spectogram.png"
        )

    def test3():
        print(f"{COLORS["yellow"]}test3:{COLORS["reset"]}")
        test_fft(
            audio_filepath="audio_files/fft_test_audio.wav",
            spectogram_img_filepath="img_files/fft_test_spectogram.png",
            frequencies_img_filepath="img_files/fft_test_frequencies.png",
            amplitudes_img_filepath="img_files/fft_test_amplitudes.png",
            sine_frequency_amplitudes={
                1000: 2000,
                1001: 2000,
            },
        )

    test3()
