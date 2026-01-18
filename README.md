# VisualizingSound

This project focuses on audio signal analysis and visualization using python<br>
It provides:

- utilities to generate audio
- analyze it using [FFT (Fast Fourier Transform)](https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm)
- visualize different signal characteristics such as:
  - waveform amplitude
  - frequency spectrum
  - spectrograms
    <br>

## 🧠 Project Structure

```powershell
VisualizingSound/
│── main.py
│── README.md
│── requirements.txt
│
└── src/
    ├── core/
    │   ├── audio.py          # audio generation & file creation
    │   ├── fft.py            # FFT & frequency extraction
    │   └── visualization.py  # amplitude, frequency, spectrogram plots
    │
    ├── utils/
    │   ├── helpers.py        # path resolution & utility functions
    │   └── logger.py         # colored logging
    │
    ├── assets/
    │   ├── audio_files/      # .wav files
    │   └── img_files/        # .png files
    │
    └── tests.py              # tests for audio & visualization
```

<br>

## 🚀 How to run it

### 1. Clone the repository

```bash
git clone https://github.com/SudevOP1/VisualizingSound.git
cd VisualizingSound
```

### 2. Create and activate virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run tests from `main.py`

```powershell
python -m main
```

### 4. Clean unnecessary files using `cleaner.py`

```powershell
python -m cleaner
```

<br>

## 📌 Notes

- Audio files must be 16-bit PCM `.wav`
- Paths are resolved relative to project root
