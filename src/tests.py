import math

from .utils.helpers import map_num
from .utils.logger import log
from .core.audio import create_audio_file, generate_wave_samples
from .core.visualization import (
    visualize_amplitude,
    visualize_frequencies,
    visualize_spectogram,
)


def test_create_audio_file(audio_filepath: str, samples: tuple[float] = ()) -> None:

    framerate = 44100
    duration = 5
    amplitude = 2000  # max = 32767
    start_freq = 20  # Hz
    end_freq = 1000  # Hz

    if not samples:
        samples = []
        for i in range(framerate * duration):
            frequency = map_num(i, 0, framerate * duration, start_freq, end_freq)
            samples.append(
                amplitude * math.sin(2 * math.pi * frequency * i / framerate)
            )
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
            prepend="create_audio_file",
            color="green",
        )
    else:
        log(
            msg=f"audio_file created: {result_path}",
            prepend="create_audio_file",
            color="green",
        )


def test_visualize_amplitude(
    audio_filepath: str,
    img_filepath: str,
    replace: bool = True,
) -> None:

    result_ok, result_path = visualize_amplitude(
        audio_filepath,
        img_filepath,
        replace=replace,
    )

    if not result_ok:
        log(
            msg=f"something went wrong: {result_path}",
            prepend="visualize_amplitude",
            color="green",
        )
    else:
        log(
            msg=f"img_file created: {result_path}",
            prepend="visualize_amplitude",
            color="green",
        )


def test_visualize_frequencies(
    audio_filepath: str,
    img_filepath: str,
    replace: bool = True,
    min_frequency: int = 0,
    max_frequency: int = 5000,
    hann_window: bool = True,
) -> None:

    result_ok, result_path = visualize_frequencies(
        audio_filepath,
        img_filepath,
        replace=replace,
        min_frequency=min_frequency,
        max_frequency=max_frequency,
        hann_window=hann_window,
    )

    if not result_ok:
        log(
            msg=f"something went wrong: {result_path}",
            prepend="visualize_frequencies",
            color="green",
        )
    else:
        log(
            msg=f"img_file created: {result_path}",
            prepend="visualize_frequencies",
            color="green",
        )


def test_visualize_spectogram(
    audio_filepath: str,
    img_filepath: str,
    replace: bool = True,
    max_frequency: int = 5000,
    plot_decibels: bool = True,
) -> None:

    result_ok, result_path = visualize_spectogram(
        audio_filepath,
        img_filepath,
        replace=replace,
        max_frequency=max_frequency,
        plot_decibels=plot_decibels,
    )

    if not result_ok:
        log(
            msg=f"something went wrong: {result_path}",
            prepend="visualize_spectogram",
            color="green",
        )
    else:
        log(
            msg=f"img_file created: {result_path}",
            prepend="visualize_spectogram",
            color="green",
        )


def test_visualizations(
    audio_filepath: str,
    replace: bool = True,
    frequencies_img_filepath: str | None = None,
    amplitudes_img_filepath: str | None = None,
    spectogram_img_filepath: str | None = None,
    spectogram_max_freq: int = 5000,
    spectogram_plot_decibels: bool = True,
) -> None:
    """
    creates spectogram, frequency, amplitude visualizations
    """

    # spectogram img
    if spectogram_img_filepath is not None:
        test_visualize_spectogram(
            audio_filepath=audio_filepath,
            img_filepath=spectogram_img_filepath,
            replace=replace,
            max_frequency=spectogram_max_freq,
            plot_decibels=spectogram_plot_decibels,
        )

    # frequencies img
    if frequencies_img_filepath is not None:
        test_visualize_frequencies(
            audio_filepath=audio_filepath,
            img_filepath=frequencies_img_filepath,
            replace=replace,
        )

    # amplitudes img
    if amplitudes_img_filepath is not None:
        test_visualize_amplitude(
            audio_filepath=audio_filepath,
            img_filepath=amplitudes_img_filepath,
            replace=replace,
        )
