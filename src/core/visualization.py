import matplotlib.pyplot as plt
import numpy as np
import os, traceback, struct, wave

from ..utils.helpers import resolve_filepath
from .fft import get_frequency_amplitudes


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
