# TTS Auto-Slicer (Audio to LJSpeech)

An automated Python tool that takes long audio files (like AI-generated TTS MP3s) and converts them into a perfectly formatted LJSpeech dataset ready for training custom voice models in Piper TTS, VITS, or Tacotron.

This script uses `librosa` for highly accurate, energy-based silence detection and OpenAI's `whisper` to automatically generate the `metadata.csv` transcriptions. 

**Note:** This tool intentionally bypasses `pydub` to ensure full compatibility with Python 3.13+, which removed the built-in `audioop` module.

## ✨ Features
* **Auto-Slicing:** Intelligently splits massive audio blocks into short, sentence-level clips based on decibel thresholds.
* **Auto-Formatting:** Forces all output audio into the strict 16-bit, 22050 Hz Mono `.wav` format required by Piper.
* **Auto-Transcription:** Uses Whisper to transcribe every slice and compile the `metadata.csv`.
* **Python 3.13+ Safe:** Uses `librosa` and `soundfile` instead of deprecated legacy audio modules.

## 🛠️ Prerequisites

### 1. FFmpeg (Required by Whisper)
Whisper requires FFmpeg to process audio files. 
* **Windows (via Winget):**
  ```bash
  winget install ffmpeg
  ```
  *(Note: You must restart your terminal/IDE after installing this before running the script).*

### 2. Python Dependencies
Install the required libraries:
```bash
pip install librosa soundfile openai-whisper
```

### 3. GPU Acceleration (Highly Recommended)
By default, the standard `pip` installation of PyTorch (which Whisper relies on) runs on your CPU, which is slow and generates a lot of heat. If you have an NVIDIA GPU, install the CUDA-enabled version of PyTorch to make transcription nearly instantaneous. You can install the latest stable PyTorch build with CUDA support (e.g., CUDA 12.6) using the following commands:
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu126](https://download.pytorch.org/whl/cu126)
```

## 🚀 Usage

1. Clone the repository to your local machine.
2. Create a folder named `raw_audio` in the same directory as the script.
3. Place your long `.mp3` or `.wav` files inside the `raw_audio` folder.
4. Run the script:
   ```bash
   python build_dataset.py
   ```

### Output
The script will automatically generate a `bloop_dataset` folder containing:
* A `wavs/` folder populated with perfectly formatted, numbered audio slices.
* A `metadata.csv` file linking each audio file to its transcribed text. This file consists of one record per line, delimited by the pipe character.

## ⚠️ Troubleshooting

**My CSV looks broken in Excel!**
Do **NOT** open and save the `metadata.csv` file in Microsoft Excel. Excel expects comma-separated values, but LJSpeech requires a pipe (`|`) delimiter. Excel will shove all the text into a single column, and if you hit save, it may inject hidden commas and ruin the dataset. 

Always view and prune your `metadata.csv` using a plain text editor like **Notepad** or **VS Code**.

**Whisper cut off a word / hallucinated a sentence.**
No AI is perfect. You should always manually review the `metadata.csv` and listen to the corresponding `.wav` files. If a sentence is cut midway or the audio contains background noise, delete the `.wav` file **and** delete its corresponding line from the `metadata.csv`. It is better to have a slightly smaller dataset than to train your model on broken audio.

```