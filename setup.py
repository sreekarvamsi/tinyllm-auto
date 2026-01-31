"""
Setup script for TinyLLM-Auto
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="tinyllm-auto",
    version="0.1.0",
    author="Sreekar Gajula",
    author_email="your.email@example.com",
    description="Edge LLM for In-Vehicle Deployment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sreekar-gajula/tinyllm-auto",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "llama-cpp-python>=0.2.0",
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "tqdm>=4.66.0",
    ],
    extras_require={
        "voice": [
            "openai-whisper>=20231117",
            "TTS>=0.22.0",
            "sounddevice>=0.4.6",
            "soundfile>=0.12.1",
        ],
        "demo": [
            "gradio>=4.0.0",
        ],
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tinyllm-auto=demo:main",
        ],
    },
)
