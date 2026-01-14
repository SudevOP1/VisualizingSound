import wave, struct, math
from helpers import *


def test_read_wav() -> None:
    filepath = "audio_files/audio.wav"
    with wave.open(filepath, "r") as f:
        print(f"filepath: {filepath}")

        print(f"f.getnchannels(): {f.getnchannels()}")
        print(f"getsampwidth(): {f.getsampwidth()}")
        print(f"getframerate(): {f.getframerate()}")
        print(f"getnframes(): {f.getnframes()}")
        print(f"getcomptype(): {f.getcomptype()}")
        print(f"getcompname(): {f.getcompname()}")
        print(f"getparams(): {f.getparams()}")
        print(f"getmarkers(): {f.getmarkers()}")
        # print(f"getmark(id): {f.getmark(id)}")
        # print(f"readframes(n): {f.readframes(n)}")
        print(f"rewind(): {f.rewind()}")
        # print(f"setpos(pos): {f.setpos(pos)}")
        print(f"tell(): {f.tell()}")


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
        print(f"something went wrong: {result_path}")
    else:
        print(f"audio_file created: {result_path}")


def test_visualize_amplitude(audio_filepath: str, img_filepath: str) -> None:

    result_ok, result_path = visualize_amplitude(
        audio_filepath,
        img_filepath,
        replace=True,
    )
    if not result_ok:
        print(f"something went wrong: {result_path}")
    else:
        print(f"img_file created: {result_path}")


def test_visualize_frequencies(audio_filepath: str, img_filepath: str) -> None:

    result_ok, result_path = visualize_frequencies(
        audio_filepath,
        img_filepath,
        replace=True,
    )
    if not result_ok:
        print(f"something went wrong: {result_path}")
    else:
        print(f"img_file created: {result_path}")


if __name__ == "__main__":
    # test_read_wav()
    # test_write_simple_wav()
    test_create_audio_file("audio_files/new_audio.wav")
    test_visualize_amplitude("audio_files/new_audio.wav", "img_files/amplitude_img.png")
    test_visualize_frequencies("audio_files/new_audio.wav", "img_files/frequencies_img.png")
