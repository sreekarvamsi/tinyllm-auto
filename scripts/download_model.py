"""
Download the Phi-2 4-bit GGUF model for TinyLLM-Auto
"""

import os
import requests
from pathlib import Path
from tqdm import tqdm


def download_file(url: str, destination: str):
    """
    Download a file with progress bar
    
    Args:
        url: URL to download from
        destination: Local path to save file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    # Check if file already exists
    if os.path.exists(destination):
        print(f"✓ File already exists: {destination}")
        return
    
    print(f"Downloading model to {destination}...")
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as file, tqdm(
        desc=os.path.basename(destination),
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)
    
    print(f"✓ Download complete: {destination}")


def download_phi2_model():
    """Download Phi-2 4-bit GGUF model"""
    
    # Model URLs (using Hugging Face)
    # Note: You'll need to replace this with the actual model URL
    # The actual Phi-2 GGUF models can be found on Hugging Face
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    print("="*60)
    print("TinyLLM-Auto Model Downloader")
    print("="*60)
    print()
    
    # Phi-2 4-bit GGUF model
    print("📥 Downloading Phi-2 4-bit GGUF model (~1.6GB)...")
    print()
    print("⚠️  Manual Download Required:")
    print("Due to model licensing and hosting constraints, please manually download:")
    print()
    print("1. Visit: https://huggingface.co/TheBloke/phi-2-GGUF")
    print("2. Download: phi-2.Q4_K_M.gguf (~1.6GB)")
    print("3. Place in: models/phi-2-4bit.gguf")
    print()
    print("Alternative (automated download from HuggingFace):")
    print("Run: huggingface-cli download TheBloke/phi-2-GGUF phi-2.Q4_K_M.gguf --local-dir models/")
    print()
    
    # Optionally download Whisper model
    print("="*60)
    print("📥 Downloading Whisper Tiny model for STT...")
    print()
    print("Whisper models are downloaded automatically on first use.")
    print("Tiny model (~39MB) will be downloaded when you first run the voice interface.")
    print()
    
    print("="*60)
    print("✓ Setup Instructions:")
    print("="*60)
    print()
    print("1. Download the Phi-2 model as instructed above")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the demo: python src/demo.py")
    print()
    
    return True


if __name__ == "__main__":
    download_phi2_model()
