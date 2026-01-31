# TinyLLM-Auto – Edge LLM for In-Vehicle Deployment

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/sreekarvamsi/tinyllm-auto?style=social)](https://github.com/sreekarvamsi/tinyllm-auto/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/sreekarvamsi/tinyllm-auto?style=social)](https://github.com/sreekarvamsi/tinyllm-auto/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/sreekarvamsi/tinyllm-auto)](https://github.com/sreekarvamsi/tinyllm-auto/issues)
[![CI](https://github.com/sreekarvamsi/tinyllm-auto/workflows/CI/badge.svg)](https://github.com/sreekarvamsi/tinyllm-auto/actions)

Optimized small language model deployment on automotive edge hardware with CPU-only constraint (<8GB RAM). Demonstrates the feasibility of in-vehicle conversational AI on existing ECU platforms.

![TinyLLM-Auto Demo](docs/demo.gif)

## 🎯 Project Overview

TinyLLM-Auto enables conversational AI capabilities in vehicles using resource-constrained automotive edge computing units (ECUs). The system runs entirely on CPU with minimal memory footprint, making it practical for deployment on existing vehicle hardware.

### Key Features

- **Lightweight Model**: Phi-2 (2.7B parameters) with 4-bit GGML quantization
- **CPU-Optimized**: Runs on automotive ECUs without GPU requirements
- **Low Memory Footprint**: Only 1.6GB for model, 3.2GB total runtime memory
- **Fast Inference**: 450ms first token latency, 45 tokens/second generation
- **Voice Interface**: Integrated speech-to-text and text-to-speech
- **Automotive Context**: Optimized for vehicle-specific queries and diagnostics

## 🚗 Real-World Applications

### 1. **Intelligent Voice Assistant**
Replace traditional command-based systems with natural language interaction:
- "What does the P0420 diagnostic code mean?"
- "How do I connect my phone via Bluetooth?"
- "Why is my tire pressure warning light on?"
- "What's the recommended oil change interval?"

### 2. **Diagnostic Explanation System**
Translate technical diagnostic codes into user-friendly explanations:
- OBD-II code interpretation
- Sensor failure diagnosis
- Maintenance reminder explanations
- Warning light clarification

### 3. **Interactive Owner's Manual**
Conversational access to vehicle documentation:
- "How do I adjust the driver's seat memory?"
- "Where is the spare tire located?"
- "How do I use adaptive cruise control?"
- "What does the eco mode do?"

### 4. **Maintenance & Service Assistant**
Proactive vehicle health monitoring:
- Service schedule reminders with context
- DIY maintenance guidance
- Parts identification and replacement instructions
- Fluid level checking procedures

### 5. **Navigation & Feature Discovery**
Help drivers utilize vehicle features:
- Infotainment system guidance
- ADAS feature explanation
- Climate control optimization
- Connectivity troubleshooting

### 6. **Driver Education & Training**
Onboard learning system for new vehicle owners:
- Feature walkthroughs
- Safety system explanations
- Eco-driving tips
- Technology tutorials

### 7. **Accessibility Features**
Enhanced accessibility for all drivers:
- Voice-controlled vehicle functions
- Simplified technical explanations
- Multilingual support potential
- Reduced reliance on manual reading

### 8. **Fleet Management Integration**
For commercial applications:
- Driver reporting ("Log issue with rear camera")
- Maintenance scheduling
- Route optimization queries
- Vehicle health status updates

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Voice Interface                       │
│  ┌──────────────┐    ┌──────────┐    ┌──────────────┐  │
│  │   Whisper    │ -> │  Phi-2   │ -> │  Coqui TTS   │  │
│  │     STT      │    │   LLM    │    │              │  │
│  └──────────────┘    └──────────┘    └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │  llama.cpp     │
                    │  Inference     │
                    │  Engine        │
                    └───────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼──────┐  ┌────────▼─────────┐
│ Prompt Cache   │  │  KV Cache   │  │ Context Window   │
│ (System +      │  │ Optimization│  │ Management       │
│  Vehicle Data) │  │             │  │ (4096 tokens)    │
└────────────────┘  └─────────────┘  └──────────────────┘
```

## 🔧 Technical Specifications

### Model Selection Process
Evaluated multiple small language models:

| Model | Parameters | Quantized Size | Quality Score | Selected |
|-------|-----------|----------------|---------------|----------|
| TinyLlama | 1.1B | 0.6GB | 62% | ❌ |
| Phi-2 | 2.7B | 1.6GB | 78% | ✅ |
| Llama-2-7B | 7B | 3.9GB | 82% | ❌ |
| Mistral-7B | 7B | 4.1GB | 84% | ❌ |

**Winner: Phi-2** - Best balance of quality, size, and reasoning capability

### Quantization Strategy

| Format | Size | Quality Impact | Selected |
|--------|------|----------------|----------|
| FP16 | 5.4GB | Baseline (100%) | ❌ |
| 8-bit | 2.9GB | -2% | ❌ |
| 4-bit GGML | 1.6GB | -7% | ✅ |

### Performance Benchmarks

**Test Environment**: Intel i7-10700K CPU, 8GB RAM, Ubuntu 22.04

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| First Token Latency | 450ms | <500ms | ✅ |
| Generation Speed | 45 tokens/sec | >30 tokens/sec | ✅ |
| Memory Usage (Runtime) | 3.2GB | <4GB | ✅ |
| Model Size (Disk) | 1.6GB | <2GB | ✅ |
| Automotive QA Accuracy | 78% | >75% | ✅ |

**Comparison**: GPT-3.5-turbo achieves 85% on the same benchmark (7% difference)

### Optimizations Implemented

1. **Prompt Caching**: Cache system prompt + vehicle context to reduce recomputation
2. **KV Cache Optimization**: Reuse attention cache for multi-turn conversations
3. **Response Streaming**: Token-by-token generation improves perceived latency
4. **Sliding Window Context**: Efficient 4096 token context management
5. **Batching**: Process multiple requests together for increased throughput

## 📦 Installation

### Prerequisites

- Python 3.8+
- 8GB RAM (minimum)
- 4GB free disk space
- Linux, macOS, or Windows with WSL2

### Quick Start

```bash
# Clone the repository
git clone https://github.com/sreekar-gajula/tinyllm-auto.git
cd tinyllm-auto

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download the Phi-2 model (4-bit GGML quantized)
python scripts/download_model.py

# Run the demo
python src/demo.py
```

### Raspberry Pi 4 Setup

```bash
# For ARM architecture
pip install -r requirements-arm.txt

# Adjust memory settings
sudo nano /boot/config.txt
# Add: gpu_mem=64  (reduce GPU memory to maximize CPU memory)

# Run optimized for Pi
python src/demo.py --device raspberry-pi
```

## 🚀 Usage

### Basic Python API

```python
from tinyllm_auto import VehicleAssistant

# Initialize the assistant
assistant = VehicleAssistant(
    model_path="models/phi-2-4bit.gguf",
    context_size=4096
)

# Set vehicle context
assistant.set_vehicle_context(
    make="Toyota",
    model="Camry",
    year=2023,
    mileage=15000
)

# Ask questions
response = assistant.ask("What does P0420 mean?")
print(response)
# Output: "P0420 indicates a Catalyst System Efficiency Below Threshold..."

# Multi-turn conversation
assistant.ask("How serious is this?")
assistant.ask("Can I drive to the mechanic?")
```

### Voice Interface

```python
from tinyllm_auto import VoiceAssistant

# Initialize with STT and TTS
voice_assistant = VoiceAssistant(
    stt_model="whisper-tiny",
    tts_model="coqui-tts",
    llm_path="models/phi-2-4bit.gguf"
)

# Start voice interaction
voice_assistant.start_listening()
# Speak: "Why is my check engine light on?"
# System responds with voice output
```

### Gradio Web Interface

```bash
# Launch interactive demo
python src/gradio_demo.py

# Open browser to http://localhost:7860
```

## 📊 Benchmarks & Evaluation

### Automotive QA Benchmark

Custom evaluation set of 500 automotive-related questions across categories:

| Category | Questions | Accuracy |
|----------|-----------|----------|
| Diagnostic Codes | 150 | 82% |
| Maintenance | 120 | 79% |
| Features/Controls | 130 | 75% |
| Safety Systems | 100 | 76% |
| **Overall** | **500** | **78%** |

### Latency Breakdown (End-to-End Voice)

```
User speaks -> STT (Whisper) -> LLM (Phi-2) -> TTS (Coqui) -> Audio output
    [300ms]        [450ms]          [800ms]      [350ms]      [1900ms total]
```

### Memory Usage Profile

```
Component             | RAM Usage
----------------------|----------
Model Loading         | 1.6GB
KV Cache             | 0.8GB
Prompt Cache         | 0.3GB
Inference Runtime    | 0.5GB
----------------------|----------
Total                | 3.2GB
```

## 🛠️ Tech Stack

- **Inference Engine**: [llama.cpp](https://github.com/ggerganov/llama.cpp) - CPU-optimized LLM inference
- **Quantization**: GGML 4-bit - Efficient model compression
- **LLM Model**: Phi-2 (2.7B parameters) - Microsoft Research
- **Speech-to-Text**: OpenAI Whisper (tiny model)
- **Text-to-Speech**: Coqui TTS
- **Backend**: Python 3.8+, C++ (llama.cpp bindings)
- **Demo UI**: Gradio
- **Testing**: pytest, automotive QA benchmark

## 📁 Project Structure

```
tinyllm-auto/
├── src/
│   ├── __init__.py
│   ├── assistant.py          # Main VehicleAssistant class
│   ├── inference.py          # llama.cpp wrapper
│   ├── voice_interface.py    # STT/TTS integration
│   ├── context_manager.py    # Sliding window context
│   ├── demo.py              # CLI demo
│   └── gradio_demo.py       # Web UI demo
├── scripts/
│   ├── download_model.py    # Model downloader
│   ├── benchmark.py         # Performance testing
│   └── evaluate.py          # QA accuracy evaluation
├── models/                  # Model weights (gitignored)
├── data/
│   ├── vehicle_contexts/    # Sample vehicle data
│   └── qa_benchmark/        # Evaluation dataset
├── tests/
│   ├── test_inference.py
│   ├── test_assistant.py
│   └── test_voice.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── API_REFERENCE.md
├── requirements.txt
├── requirements-arm.txt     # For Raspberry Pi
├── setup.py
├── LICENSE
└── README.md
```

## 🎥 Demo

### Raspberry Pi 4 Deployment

Successfully deployed on Raspberry Pi 4 (ARM, 8GB) proving feasibility for automotive ECU platforms:

- **Total Latency**: <2 seconds (including STT/TTS)
- **Memory**: 3.5GB (within 8GB constraint)
- **CPU Usage**: 60-70% during inference

**[Watch Demo Video](#)** *(Link to YouTube demo)*

### Example Interactions

**Diagnostic Query:**
```
User: "What does P0420 diagnostic code mean?"
Assistant: "P0420 indicates that your catalytic converter's efficiency 
has fallen below the threshold. This usually means the catalyst is 
degraded and may need replacement. It's safe to drive but should be 
addressed within the next few weeks to avoid emissions test failures."
```

**Feature Help:**
```
User: "How do I pair my phone via Bluetooth?"
Assistant: "To pair your phone: 1) Turn on Bluetooth on your phone,
2) On your vehicle's infotainment screen, go to Settings > Bluetooth,
3) Select 'Add New Device', 4) Choose your phone from the list,
5) Confirm the pairing code matches on both devices. The process 
takes about 30 seconds."
```

**Vehicle Status:**
```
User: "Why is my check engine light on?"
Assistant: "Your check engine light can indicate various issues. Let me 
check your vehicle's diagnostic codes... Based on your vehicle's history,
this could be related to the oxygen sensor. I recommend using an OBD-II 
scanner to read the specific error code, which will help identify the 
exact problem. Would you like me to explain how to use an OBD-II scanner?"
```

## 🔬 Future Enhancements

- [ ] Fine-tuning on vehicle-specific documentation
- [ ] Integration with vehicle CAN bus for real-time diagnostics
- [ ] Multi-language support (Spanish, Chinese, French)
- [ ] Personalized driver profiles and history
- [ ] Over-the-air model updates
- [ ] Integration with manufacturer-specific APIs
- [ ] Expanded automotive knowledge base
- [ ] Voice activity detection for hands-free operation
- [ ] Emotion recognition for safety alerts

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/sreekarvamsi/tinyllm-auto.git
cd tinyllm-auto
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run benchmarks
python scripts/benchmark.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Microsoft Research for the Phi-2 model
- Georgi Gerganov for llama.cpp
- OpenAI for Whisper
- Coqui for TTS
- The open-source community

## 📧 Contact

**Sreekar Gajula** - [GitHub](https://github.com/sreekarvamsi)

Project Link: [https://github.com/sreekarvamsi/tinyllm-auto](https://github.com/sreekarvamsi/tinyllm-auto)

---

⭐ If you find this project useful, please consider giving it a star!
