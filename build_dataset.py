import os
import whisper
import librosa
import soundfile as sf

# ==========================================
# CONFIGURATION
# ==========================================
INPUT_FOLDER = "raw-audio" # Put your raw audio here
OUTPUT_FOLDER = "audio-dataset" # Automatically make a new folder with the result
WAVS_FOLDER = os.path.join(OUTPUT_FOLDER, "wavs")
METADATA_FILE = os.path.join(OUTPUT_FOLDER, "metadata.csv")

# Piper's Strict Audio Requirements
TARGET_SAMPLE_RATE = 22050

def process_dataset():
    print("Loading Whisper AI... (This might take a moment)")
    model = whisper.load_model("base") 

    os.makedirs(WAVS_FOLDER, exist_ok=True)
    
    file_counter = 1

    # Find all MP3s in the input folder
    mp3_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".mp3")]
    
    if not mp3_files:
        print(f"Error: No MP3 files found in '{INPUT_FOLDER}'.")
        return

    print(f"Found {len(mp3_files)} MP3 files. Starting processing...\n")

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        for filename in mp3_files:
            filepath = os.path.join(INPUT_FOLDER, filename)
            print(f"Processing: {filename}")
            
            # Load audio and force 22050Hz Mono
            # librosa automatically handles the mp3 decoding
            y, sr = librosa.load(filepath, sr=TARGET_SAMPLE_RATE, mono=True)
            
            # Split on silence (40dB below peak volume)
            intervals = librosa.effects.split(y, top_db=40, frame_length=2048, hop_length=512)
            
            # Calculate 250ms of padding so words aren't abruptly cut off
            pad_samples = int(TARGET_SAMPLE_RATE * 0.25) 

            for start, end in intervals:
                # Add the padding back to the ends of the chunk
                start_padded = max(0, start - pad_samples)
                end_padded = min(len(y), end + pad_samples)
                
                chunk = y[start_padded:end_padded]
                
                # Skip chunks that are way too short to be a sentence (< 1 second)
                if len(chunk) < TARGET_SAMPLE_RATE:
                    continue
                    
                wav_filename = f"bloop_{file_counter:04d}.wav"
                wav_path = os.path.join(WAVS_FOLDER, wav_filename)
                
                # Export as 16-bit PCM WAV
                sf.write(wav_path, chunk, TARGET_SAMPLE_RATE, subtype='PCM_16')
                
                # Transcribe with Whisper
                result = model.transcribe(wav_path, language="en")
                text = result["text"].strip()
                
                # Skip if Whisper hallucinated or failed to transcribe
                if not text:
                    os.remove(wav_path)
                    continue
                    
                # Write to metadata.csv
                file_id = wav_filename.replace('.wav', '')
                f.write(f"{file_id}|{text}\n")
                print(f"  Saved {wav_filename}: {text}")
                
                file_counter += 1

    print("\n✅ Dataset creation complete!")
    print(f"Generated {file_counter - 1} perfectly formatted audio clips in '{WAVS_FOLDER}'.")
    print(f"Metadata saved to '{METADATA_FILE}'.")

if __name__ == "__main__":
    process_dataset()