import os

# ==========================================
# CONFIGURATION
# ==========================================
DATASET_DIR = "audio-dataset"
WAVS_DIR = os.path.join(DATASET_DIR, "wavs")
METADATA_FILE = os.path.join(DATASET_DIR, "metadata.csv")

def validate_dataset():
    if not os.path.exists(METADATA_FILE):
        print(f"❌ Error: Could not find '{METADATA_FILE}'.")
        return
    if not os.path.exists(WAVS_DIR):
        print(f"❌ Error: Could not find '{WAVS_DIR}'.")
        return

    print("Scanning dataset... \n")

    # Grab all filenames listed in the CSV
    csv_files = set()
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            # Split by the pipe delimiter
            parts = line.split('|')
            if len(parts) >= 1:
                filename = parts[0].strip()
                # Ensure it has the .wav extension for direct comparison
                if not filename.endswith('.wav'):
                    filename += '.wav'
                csv_files.add(filename)

    # Grab all actual .wav files in the folder
    actual_wavs = set([f for f in os.listdir(WAVS_DIR) if f.endswith('.wav')])

    # Find the discrepancies
    missing_audio = csv_files - actual_wavs
    orphaned_audio = actual_wavs - csv_files

    # Print the final report
    print("=== 🔍 Dataset Validation Report ===")
    print(f"Total entries in CSV:  {len(csv_files)}")
    print(f"Total files in folder: {len(actual_wavs)}\n")

    if not missing_audio and not orphaned_audio:
        print("✅ PERFECT MATCH! Your dataset is absolutely pristine and ready.")
        return

    if missing_audio:
        print(f"🚨 Missing Audio Files ({len(missing_audio)}):")
        print("   These are typed in your CSV, but the .wav file doesn't exist.")
        for f in sorted(missing_audio):
            print(f"   - {f}")
        print()

    if orphaned_audio:
        print(f"👻 Orphaned Audio Files ({len(orphaned_audio)}):")
        print("   These .wav files are in your folder, but are missing from the CSV.")
        for f in sorted(orphaned_audio):
            print(f"   - {f}")

if __name__ == "__main__":
    validate_dataset()