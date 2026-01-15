import wave, os, struct, traceback, math, cmath
import numpy as np
import matplotlib.pyplot as plt


def map_num(num: float, x1: float, x2: float, x3: float, x4: float) -> float:
    """linearly maps a numeric value from range [x1, x2] to range [x3, x4]"""
    if x1 == x2:
        return 0
    return x3 + (x4 - x3) * (num - x1) / (x2 - x1)


def resolve_filepath(filepath: str, replace: bool = False) -> str:
    """resolves filename collisions by appending an incrementing numeric suffix"""

    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)

    base, ext = os.path.splitext(filepath)

    if not os.path.exists(filepath) or replace:
        return filepath

    i = 1
    while True:
        new_filepath = f"{base} ({i}){ext}"
        if not os.path.exists(new_filepath):
            return new_filepath
        i += 1


def apply_fft(samples: np.ndarray[np.float32], framerate: int) -> dict[float, float]:
    """
    applies discrete fft (discrete fast fourier transform / Cooley-Tukey Algo)
    returns a dict of frequency (Hz) -> amplitude (magnitude)
    """

    def fft(x: list[complex]) -> list[complex]:
        n = len(x)
        if n == 1:
            return x

        even = fft(x[0::2])
        odd = fft(x[1::2])

        result = [0] * n
        for k in range(n // 2):
            twiddle = cmath.exp(-2j * math.pi * k / n) * odd[k]
            result[k] = even[k] + twiddle
            result[k + n // 2] = even[k] - twiddle

        return result

    n = len(samples)
    if n == 0:
        return {}

    power = 1 << (n - 1).bit_length()
    padded = list(samples) + [0.0] * (power - n)

    complex_signal = [complex(s, 0) for s in padded]
    spectrum = fft(complex_signal)

    frequency_amplitudes: dict[float, float] = {}

    for k in range(1, len(spectrum) // 2):
        freq = k * framerate / len(spectrum)
        amp = abs(spectrum[k])
        frequency_amplitudes[freq] = amp

    return frequency_amplitudes


def get_frequency_amplitudes(audio_filepath: str) -> tuple[bool, dict[int, int]]:
    """
    returns success bool and a mapping of frequency (Hz) -> amplitude (magnitude)
    extracted from a .wav audio file using FFT
    """

    # resolving filepath
    if not audio_filepath or not os.path.exists(audio_filepath):
        return False, "audio not found"

    try:
        with wave.open(audio_filepath, "rb") as audio_file:
            n_channels = audio_file.getnchannels()
            framerate = audio_file.getframerate()
            n_frames = audio_file.getnframes()
            frames = audio_file.readframes(n_frames)

        # assume 16 bit PCM
        samples = np.array(
            struct.unpack("<" + "h" * (len(frames) // 2), frames),
            dtype=np.float32,
        )

        # stereo -> mono
        if n_channels == 2:
            samples = samples[::2]

        # FFT
        frequency_amplitudes = apply_fft(samples, framerate)
        frequency_amplitudes_ints = {}
        for key, value in frequency_amplitudes.items():
            frequency_amplitudes_ints[int(round(key))] = int(value)

        return True, frequency_amplitudes_ints

    except Exception:
        return False, traceback.format_exc()


# ================ main helpers👇 ================


def create_audio_file(
    filepath: str,
    samples: tuple,
    framerate: int,
    n_channels: int = 1,
    samp_width: int = 2,
    replace: bool = False,
) -> tuple[bool, str]:
    """returns success bool and actual filepath string or error string"""

    filepath = resolve_filepath(filepath, replace=replace)

    try:
        with wave.open(filepath, "w") as f:
            f.setnchannels(n_channels)
            f.setsampwidth(samp_width)
            f.setframerate(framerate)

            for sample in samples:
                f.writeframes(struct.pack("<h", int(sample)))

        return True, filepath

    except Exception:
        return False, traceback.format_exc()


def visualize_amplitude(
    audio_filepath: str = None,
    img_filepath: str = None,
    replace: bool = False,
) -> tuple[bool, str]:
    """
    generates visualization of amplitude of an audio,
    returns success bool and actual filepath string or error string
    """

    try:
        if not audio_filepath or not os.path.exists(audio_filepath):
            return False, "audio not found"
        if not img_filepath:
            img_filepath = os.path.splitext(audio_filepath)[0] + ".png"
        img_filepath = resolve_filepath(img_filepath, replace=replace)

        # read audio
        with wave.open(audio_filepath, "rb") as audio_file:
            n_channels = audio_file.getnchannels()
            n_frames = audio_file.getnframes()
            frames = audio_file.readframes(n_frames)

        samples = struct.unpack("<" + "h" * (len(frames) // 2), frames)

        # convert stereo -> mono
        if n_channels == 2:
            samples = samples[::2]

        # normalize
        max_amp = max(abs(s) for s in samples) or 1
        samples = [s / max_amp for s in samples]

        plt.figure()
        plt.plot(samples)
        plt.axhline(0, color="black")
        plt.tight_layout()
        plt.savefig(img_filepath)
        plt.close()

        return True, img_filepath

    except Exception:
        return False, traceback.format_exc()


def visualize_frequencies(
    audio_filepath: str = None,
    img_filepath: str = None,
    replace: bool = False,
    max_frequency: int = 10000,
) -> tuple[bool, str]:

    try:
        if not audio_filepath or not os.path.exists(audio_filepath):
            return False, "audio not found"
        if not img_filepath:
            img_filepath = os.path.splitext(audio_filepath)[0] + ".png"
        img_filepath = resolve_filepath(img_filepath, replace=replace)

        frequency_amplitudes_ok, frequency_amplitudes = get_frequency_amplitudes(
            audio_filepath
        )
        if not frequency_amplitudes_ok:
            return False, frequency_amplitudes

        freqs = []
        amps = []

        for freq, amp in frequency_amplitudes.items():
            if 0 <= freq <= max_frequency:
                freqs.append(freq)
                amps.append(amp)

        plt.figure()
        plt.bar(freqs, amps, width=1.0)
        plt.xlim(0, max_frequency)
        plt.tight_layout()
        plt.savefig(img_filepath)
        plt.close()

        return True, img_filepath

    except Exception:
        return False, traceback.format_exc()


def visualize_spectogram(
    audio_filepath: str = None,
    img_filepath: str = None,
    replace: bool = False,
    img_width: int = 1280,
    img_height: int = 720,
    max_frequency: int = 10000,
) -> tuple[bool, str]:
    """
    returns success bool and a spectogram img filepath or error string
    extracted from a .wav audio file using FFT
    """
    try:

        if not audio_filepath or not os.path.exists(audio_filepath):
            return False, "audio not found"
        if not img_filepath:
            img_filepath = os.path.splitext(audio_filepath)[0] + ".png"
        img_filepath = resolve_filepath(img_filepath, replace=replace)

        with wave.open(audio_filepath, "rb") as audio_file:
            n_channels = audio_file.getnchannels()
            framerate = audio_file.getframerate()
            n_frames = audio_file.getnframes()
            frames = audio_file.readframes(n_frames)

        # unpack assuming 16-bit PCM
        samples = np.array(
            struct.unpack("<" + "h" * (len(frames) // 2), frames),
            dtype=np.float32,
        )

        # stereo -> mono
        if n_channels == 2:
            samples = samples[::2]

        # matplotlib figure size
        plt.figure(figsize=(img_width / 100, img_height / 100), dpi=100)

        # spectogram
        pxx, freqs, bin, im = plt.specgram(
            samples,
            Fs=framerate,
            NFFT=2048,
            noverlap=1024,
            cmap="Greys",
        )

        plt.ylim(0, max_frequency)
        plt.tight_layout()
        plt.savefig(img_filepath)
        plt.close()

        return True, img_filepath

    except Exception:
        return False, traceback.format_exc()
