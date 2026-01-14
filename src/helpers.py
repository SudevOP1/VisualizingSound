import wave, os, struct, traceback
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw


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
        fft_values = np.fft.rfft(samples)
        magnitudes = np.abs(fft_values)
        frequencies = np.fft.rfftfreq(len(samples), d=1.0 / framerate)

        frequency_amplitudes: dict[int, int] = {}
        for freq, amp in zip(frequencies, magnitudes):
            if freq > 0:
                frequency_amplitudes[int(round(freq))] = int(amp)

        return True, frequency_amplitudes

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
    img_width: int = 1280,
    img_height: int = 720,
    x_padding: int = 100,
    y_padding: int = 100,
    bg_color: tuple[int] = (0, 0, 0),  # black
    wave_color: tuple[int] = (0, 200, 0),  # green
) -> tuple[bool, str]:
    """
    generates visualization of amplitude of an audio,
    returns success bool and actual filepath string or error string
    """
    try:

        # resolving filepaths
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

        if n_channels == 2:
            samples = samples[::2]

        # drawable area
        drawable_width = img_width - 2 * x_padding
        drawable_height = img_height - 2 * y_padding

        # downsample to drawable width
        step = max(1, len(samples) // drawable_width)
        samples = samples[::step][:drawable_width]

        max_amp = max(abs(s) for s in samples) or 1

        img_obj = Image.new("RGB", (img_width, img_height), bg_color)
        draw_obj = ImageDraw.Draw(img_obj)

        mid_y = y_padding + drawable_height // 2
        max_line_height = drawable_height // 2

        for i, sample in enumerate(samples):
            amplitude = abs(sample) / max_amp
            line_height = int(amplitude * max_line_height)

            x = x_padding + i

            draw_obj.line(
                (x, mid_y - line_height, x, mid_y + line_height),
                fill=wave_color,
                width=1,
            )

        img_obj.save(img_filepath)
        return True, img_filepath

    except Exception:
        return False, traceback.format_exc()


def visualize_frequencies(
    audio_filepath: str = None,
    img_filepath: str = None,
    replace: bool = False,
    img_width: int = 1280,
    img_height: int = 720,
    x_padding: int = 100,
    y_padding: int = 100,
    bg_color: tuple[int] = (0, 0, 0),  # black
    amp_color: tuple[int] = (0, 200, 0),  # green
    axis_color: tuple[int] = (255, 255, 255),  # white
    label_step: int = 500,
    max_frequency: int = 10000,
) -> tuple[bool, str]:
    """
    returns success bool and a mapping of frequency (Hz) -> amplitude (magnitude)
    extracted from a .wav audio file using FFT
    """

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

        # drawable area
        drawable_width = img_width - 2 * x_padding
        drawable_height = img_height - 2 * y_padding

        min_freq = 0
        max_freq = max_frequency
        max_amp = max(frequency_amplitudes.values()) or 1

        img = Image.new("RGB", (img_width, img_height), bg_color)
        draw = ImageDraw.Draw(img)

        # x-axis position
        x_axis_y = img_height - y_padding

        # frequency -> x-mapping
        def freq_to_x(freq: int) -> int:
            return x_padding + int(
                (freq - min_freq) / (max_freq - min_freq) * drawable_width
            )

        # amplitude -> y-mapping
        def amp_to_y(amp: int) -> int:
            return x_axis_y - int((amp / max_amp) * drawable_height)

        # frequency bars
        for freq, amp in frequency_amplitudes.items():
            if min_freq <= freq <= max_freq:
                x = freq_to_x(freq)
                y = amp_to_y(amp)
                draw.line((x, x_axis_y, x, y), fill=amp_color, width=1)

        # x-axis
        draw.line(
            (x_padding, x_axis_y, img_width - x_padding, x_axis_y),
            fill=axis_color,
            width=1,
        )

        # x-axis labels
        for freq in range(0, max_freq + 1, label_step):
            x = freq_to_x(freq)
            draw.line((x, x_axis_y, x, x_axis_y + 5), fill=axis_color, width=1)
            draw.text((x - 15, x_axis_y + 8), f"{freq}", fill=axis_color)

        img.save(img_filepath)
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
