"""
TinyLLM-Auto: Voice Interface
Integrates Whisper (STT) and Coqui TTS for voice interaction
"""

import os
import time
import wave
import tempfile
from typing import Optional, Callable
import numpy as np


class VoiceAssistant:
    """
    Voice-enabled automotive assistant combining STT, LLM, and TTS
    """
    
    def __init__(
        self,
        llm_path: str,
        stt_model: str = "tiny",
        tts_model: str = "tts_models/en/ljspeech/tacotron2-DDC",
        verbose: bool = False
    ):
        """
        Initialize the voice assistant
        
        Args:
            llm_path: Path to the GGUF LLM model
            stt_model: Whisper model size (tiny, base, small, medium, large)
            tts_model: Coqui TTS model name
            verbose: Enable detailed logging
        """
        self.verbose = verbose
        self.llm_path = llm_path
        
        # Initialize components (lazy loading)
        self._whisper_model = None
        self._tts_model = None
        self._vehicle_assistant = None
        
        self.stt_model_name = stt_model
        self.tts_model_name = tts_model
        
        if self.verbose:
            print("VoiceAssistant initialized")
    
    def _load_whisper(self):
        """Lazy load Whisper STT model"""
        if self._whisper_model is None:
            try:
                import whisper
                
                if self.verbose:
                    print(f"Loading Whisper {self.stt_model_name} model...")
                    start_time = time.time()
                
                self._whisper_model = whisper.load_model(self.stt_model_name)
                
                if self.verbose:
                    load_time = time.time() - start_time
                    print(f"Whisper loaded in {load_time:.2f} seconds")
                    
            except ImportError:
                raise ImportError(
                    "whisper is required. Install with: "
                    "pip install openai-whisper"
                )
    
    def _load_tts(self):
        """Lazy load Coqui TTS model"""
        if self._tts_model is None:
            try:
                from TTS.api import TTS
                
                if self.verbose:
                    print(f"Loading TTS model: {self.tts_model_name}...")
                    start_time = time.time()
                
                self._tts_model = TTS(model_name=self.tts_model_name)
                
                if self.verbose:
                    load_time = time.time() - start_time
                    print(f"TTS loaded in {load_time:.2f} seconds")
                    
            except ImportError:
                raise ImportError(
                    "TTS is required. Install with: "
                    "pip install TTS"
                )
    
    def _load_llm(self):
        """Lazy load the vehicle assistant (LLM)"""
        if self._vehicle_assistant is None:
            from .assistant import VehicleAssistant
            
            self._vehicle_assistant = VehicleAssistant(
                model_path=self.llm_path,
                verbose=self.verbose
            )
    
    def transcribe_audio(self, audio_path: str) -> str:
        """
        Convert speech to text using Whisper
        
        Args:
            audio_path: Path to audio file (WAV format)
            
        Returns:
            Transcribed text
        """
        self._load_whisper()
        
        if self.verbose:
            print(f"Transcribing audio: {audio_path}")
            start_time = time.time()
        
        result = self._whisper_model.transcribe(audio_path)
        transcription = result["text"].strip()
        
        if self.verbose:
            transcription_time = time.time() - start_time
            print(f"Transcription: '{transcription}'")
            print(f"STT time: {transcription_time:.2f}s")
        
        return transcription
    
    def synthesize_speech(self, text: str, output_path: Optional[str] = None) -> str:
        """
        Convert text to speech using Coqui TTS
        
        Args:
            text: Text to synthesize
            output_path: Path to save audio file (None = temp file)
            
        Returns:
            Path to generated audio file
        """
        self._load_tts()
        
        if output_path is None:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix='.wav',
                prefix='tts_'
            )
            output_path = temp_file.name
            temp_file.close()
        
        if self.verbose:
            print(f"Synthesizing speech: '{text[:50]}...'")
            start_time = time.time()
        
        # Generate speech
        self._tts_model.tts_to_file(
            text=text,
            file_path=output_path
        )
        
        if self.verbose:
            synthesis_time = time.time() - start_time
            print(f"TTS time: {synthesis_time:.2f}s")
            print(f"Audio saved to: {output_path}")
        
        return output_path
    
    def process_voice_query(
        self,
        audio_input_path: str,
        audio_output_path: Optional[str] = None
    ) -> tuple[str, str, str]:
        """
        Process a complete voice interaction: STT -> LLM -> TTS
        
        Args:
            audio_input_path: Path to user's audio input
            audio_output_path: Path to save assistant's audio response
            
        Returns:
            Tuple of (transcribed_text, llm_response, output_audio_path)
        """
        if self.verbose:
            print("\n" + "="*60)
            print("Processing voice query...")
            print("="*60)
            total_start_time = time.time()
        
        # Step 1: Speech to Text
        transcribed_text = self.transcribe_audio(audio_input_path)
        
        # Step 2: LLM Processing
        self._load_llm()
        llm_response = self._vehicle_assistant.ask(transcribed_text)
        
        # Step 3: Text to Speech
        output_audio = self.synthesize_speech(llm_response, audio_output_path)
        
        if self.verbose:
            total_time = time.time() - total_start_time
            print(f"\nTotal pipeline time: {total_time:.2f}s")
            print("="*60 + "\n")
        
        return transcribed_text, llm_response, output_audio
    
    def set_vehicle_context(self, make: str, model: str, year: int, mileage: int):
        """Set vehicle context for the LLM"""
        self._load_llm()
        self._vehicle_assistant.set_vehicle_context(make, model, year, mileage)
    
    def record_audio(
        self,
        duration: int = 5,
        sample_rate: int = 16000,
        output_path: Optional[str] = None
    ) -> str:
        """
        Record audio from microphone
        
        Args:
            duration: Recording duration in seconds
            sample_rate: Audio sample rate
            output_path: Path to save recording (None = temp file)
            
        Returns:
            Path to recorded audio file
        """
        try:
            import sounddevice as sd
            
            if self.verbose:
                print(f"Recording for {duration} seconds...")
            
            # Record audio
            audio_data = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype='int16'
            )
            sd.wait()  # Wait until recording is finished
            
            if output_path is None:
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix='.wav',
                    prefix='recording_'
                )
                output_path = temp_file.name
                temp_file.close()
            
            # Save as WAV file
            with wave.open(output_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(sample_rate)
                wf.writeframes(audio_data.tobytes())
            
            if self.verbose:
                print(f"Recording saved to: {output_path}")
            
            return output_path
            
        except ImportError:
            raise ImportError(
                "sounddevice is required for recording. Install with: "
                "pip install sounddevice"
            )
    
    def play_audio(self, audio_path: str):
        """
        Play audio file
        
        Args:
            audio_path: Path to audio file
        """
        try:
            import sounddevice as sd
            import soundfile as sf
            
            if self.verbose:
                print(f"Playing audio: {audio_path}")
            
            # Read audio file
            data, sample_rate = sf.read(audio_path)
            
            # Play audio
            sd.play(data, sample_rate)
            sd.wait()  # Wait until playback is finished
            
        except ImportError:
            raise ImportError(
                "sounddevice and soundfile are required. Install with: "
                "pip install sounddevice soundfile"
            )
    
    def interactive_voice_session(self):
        """
        Start an interactive voice session
        User speaks -> System responds with voice
        """
        print("\n" + "="*60)
        print("Interactive Voice Session Started")
        print("="*60)
        print("Press Ctrl+C to exit")
        print("="*60 + "\n")
        
        try:
            while True:
                print("\n🎤 Listening... (speak for 5 seconds)")
                
                # Record user input
                audio_input = self.record_audio(duration=5)
                
                # Process the query
                try:
                    user_text, assistant_text, audio_output = self.process_voice_query(
                        audio_input
                    )
                    
                    print(f"\n👤 You said: {user_text}")
                    print(f"🤖 Assistant: {assistant_text}")
                    
                    # Play the response
                    print("🔊 Playing response...")
                    self.play_audio(audio_output)
                    
                    # Clean up temp files
                    os.remove(audio_input)
                    os.remove(audio_output)
                    
                except Exception as e:
                    print(f"❌ Error processing query: {e}")
                    continue
                
                print("\n" + "-"*60)
                
        except KeyboardInterrupt:
            print("\n\n👋 Voice session ended")


# Example usage
if __name__ == "__main__":
    # Initialize voice assistant
    voice_assistant = VoiceAssistant(
        llm_path="models/phi-2-4bit.gguf",
        stt_model="tiny",  # Fastest Whisper model
        verbose=True
    )
    
    # Set vehicle context
    voice_assistant.set_vehicle_context(
        make="Toyota",
        model="Camry",
        year=2023,
        mileage=15000
    )
    
    # Start interactive session
    print("\nStarting interactive voice session...")
    print("Speak your questions about your vehicle!")
    
    voice_assistant.interactive_voice_session()
