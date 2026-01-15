import wave, struct, math
from helpers import *


def test_read_wav() -> None:
    filepath = "audio_files/audio.wav"
    with wave.open(filepath, "r") as f:
        print(f"[test_read_wav] filepath: {filepath}")

        print(f"[test_read_wav] f.getnchannels(): {f.getnchannels()}")
        print(f"[test_read_wav] getsampwidth(): {f.getsampwidth()}")
        print(f"[test_read_wav] getframerate(): {f.getframerate()}")
        print(f"[test_read_wav] getnframes(): {f.getnframes()}")
        print(f"[test_read_wav] getcomptype(): {f.getcomptype()}")
        print(f"[test_read_wav] getcompname(): {f.getcompname()}")
        print(f"[test_read_wav] getparams(): {f.getparams()}")
        print(f"[test_read_wav] getmarkers(): {f.getmarkers()}")
        # print(f"[test_read_wav] getmark(id): {f.getmark(id)}")
        # print(f"[test_read_wav] readframes(n): {f.readframes(n)}")
        print(f"[test_read_wav] rewind(): {f.rewind()}")
        # print(f"[test_read_wav] setpos(pos): {f.setpos(pos)}")
        print(f"[test_read_wav] tell(): {f.tell()}")


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
        print(f"[test_create_audio_file] something went wrong: {result_path}")
    else:
        print(f"[test_create_audio_file] audio_file created: {result_path}")


def test_visualize_amplitude(audio_filepath: str, img_filepath: str) -> None:

    result_ok, result_path = visualize_amplitude(
        audio_filepath,
        img_filepath,
        replace=True,
    )
    if not result_ok:
        print(f"[test_visualize_amplitude] something went wrong: {result_path}")
    else:
        print(f"[test_visualize_amplitude] img_file created: {result_path}")


def test_visualize_frequencies(audio_filepath: str, img_filepath: str) -> None:

    result_ok, result_path = visualize_frequencies(
        audio_filepath,
        img_filepath,
        replace=True,
    )
    if not result_ok:
        print(f"[test_visualize_frequencies] something went wrong: {result_path}")
    else:
        print(f"[test_visualize_frequencies] img_file created: {result_path}")


def test_visualize_spectogram(audio_filepath: str, img_filepath: str) -> None:

    result_ok, result_path = visualize_spectogram(
        audio_filepath,
        img_filepath,
        replace=True,
        max_frequency=5000,
    )
    if not result_ok:
        print(f"[test_visualize_spectogram] something went wrong: {result_path}")
    else:
        print(f"[test_visualize_spectogram] img_file created: {result_path}")


def test_fft(
    audio_filepath: str,
    img_filepath: str,
    sine_frequency_amplitudes: dict[int, int] = {},
    cosine_frequency_amplitudes: dict[int, int] = {},
    duration: float = 5.0,
) -> None:
    """
    creates an audio as a sum of sine and cosine waves of multiple frequencies
    then applies fft on it and creates spectogram
    """

    # default sine freqs if both sine and cosine are passed empty
    if not sine_frequency_amplitudes and not cosine_frequency_amplitudes:
        # freqs of 500, 2000 Hz
        sine_frequency_amplitudes = {500: 2000, 2000: 2000}

    framerate = 44100
    num_samples = int(framerate * duration)

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

    audio_path_ok, audio_path = create_audio_file(
        audio_filepath,
        samples,
        framerate,
        replace=True,
    )
    if not audio_path_ok:
        print(f"[test_fft] something went wrong in creating audio file: {audio_path}")
        return
    print(f"[test_fft] audio_file created: {audio_path}")

    # calc max_freq for visualization
    max_freq_candidates = []
    if sine_frequency_amplitudes:
        max_freq_candidates.append(max(sine_frequency_amplitudes))
    if cosine_frequency_amplitudes:
        max_freq_candidates.append(max(cosine_frequency_amplitudes))
    max_freq = max(max_freq_candidates) + 500 if max_freq_candidates else 2000

    img_path_ok, img_path = visualize_spectogram(
        audio_path,
        img_filepath,
        replace=True,
        max_frequency=max_freq,
    )
    if not img_path_ok:
        print(
            f"[test_visualize_spectogram] something went wrong in creating spectogram: {img_path}"
        )
    else:
        print(f"[test_visualize_spectogram] img_file created: {img_path}")


if __name__ == "__main__":

    def test1():
        print("test1:")
        test_read_wav()
        test_write_simple_wav()

    def test2():
        print("test2:")
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
        print("test3:")
        test_fft("audio_files/fft_test_audio.wav", "img_files/fft_test_spectogram.png")

    test3()
