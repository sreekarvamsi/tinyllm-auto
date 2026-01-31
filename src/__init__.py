"""
TinyLLM-Auto: Edge LLM for In-Vehicle Deployment
"""

from .assistant import VehicleAssistant, VehicleContext
from .voice_interface import VoiceAssistant

__version__ = "0.1.0"
__all__ = ["VehicleAssistant", "VehicleContext", "VoiceAssistant"]
