import wave, math, cmath, os, struct, traceback
import numpy as np


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
        amp = (2.0 / n) * abs(spectrum[k])
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
        frequency_amplitudes_binned = {}
        for freq, amp in frequency_amplitudes.items():
            rounded_freq = int(round(freq))
            frequency_amplitudes_binned[rounded_freq] = max(
                frequency_amplitudes_binned.get(rounded_freq, 0.0),
                amp,
            )

        return True, frequency_amplitudes_binned

    except Exception:
        return False, traceback.format_exc()
