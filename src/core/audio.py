import wave, struct, traceback, math

from ..utils.helpers import resolve_filepath


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


def generate_wave_samples(
    sine_frequency_amplitudes: dict[int, int] = {},
    cosine_frequency_amplitudes: dict[int, int] = {},
    framerate: int = 44100,
    duration: float = 5.0,
) -> tuple[float]:
    """
    generates audio samples by adding sine and cosine waves
    defined by frequency-amplitude mappings
    """

    # default sine freqs if both sine and cosine are passed empty
    if not sine_frequency_amplitudes and not cosine_frequency_amplitudes:
        # freqs of 500, 2000 Hz
        sine_frequency_amplitudes = {500: 2000, 2000: 2000}

    # calc samples
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

    return tuple(samples)
