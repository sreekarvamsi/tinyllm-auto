"""
TinyLLM-Auto: Vehicle Assistant
Main class for automotive conversational AI
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
import time


@dataclass
class VehicleContext:
    """Store vehicle-specific information"""
    make: str
    model: str
    year: int
    mileage: int
    vin: Optional[str] = None
    
    def to_prompt(self) -> str:
        """Convert vehicle context to prompt string"""
        return f"""Vehicle Information:
- Make: {self.make}
- Model: {self.model}
- Year: {self.year}
- Current Mileage: {self.mileage:,} miles
"""


class VehicleAssistant:
    """
    Main assistant class for automotive conversational AI.
    Handles LLM inference, context management, and vehicle-specific queries.
    """
    
    def __init__(
        self,
        model_path: str,
        context_size: int = 4096,
        n_threads: Optional[int] = None,
        verbose: bool = False
    ):
        """
        Initialize the Vehicle Assistant
        
        Args:
            model_path: Path to the GGUF model file
            context_size: Maximum context window size
            n_threads: Number of CPU threads (None = auto-detect)
            verbose: Enable detailed logging
        """
        self.model_path = model_path
        self.context_size = context_size
        self.verbose = verbose
        
        # Initialize conversation history
        self.conversation_history: List[Dict[str, str]] = []
        self.vehicle_context: Optional[VehicleContext] = None
        
        # System prompt for automotive assistant
        self.system_prompt = """You are an intelligent automotive assistant integrated into a vehicle's infotainment system. Your role is to help drivers understand their vehicle, diagnose issues, and use features effectively.

Guidelines:
- Provide clear, concise explanations suitable for non-technical users
- Prioritize safety in all recommendations
- For diagnostic codes, explain what they mean and urgency level
- For features, provide step-by-step instructions
- If you're unsure, acknowledge limitations and suggest consulting a mechanic
- Keep responses under 100 words unless detailed explanation is requested
- Be conversational and helpful

When answering about diagnostic codes (e.g., P0420), always include:
1. What the code means
2. Likely causes
3. Severity/urgency
4. Whether it's safe to drive
5. Recommended next steps
"""
        
        # Lazy load the LLM (only when first needed)
        self._llm = None
        
        if self.verbose:
            print(f"VehicleAssistant initialized with model: {model_path}")
    
    def _load_llm(self):
        """Lazy load the LLM model"""
        if self._llm is None:
            try:
                from llama_cpp import Llama
                
                if self.verbose:
                    print("Loading LLM model...")
                    start_time = time.time()
                
                self._llm = Llama(
                    model_path=self.model_path,
                    n_ctx=self.context_size,
                    n_threads=self.n_threads if hasattr(self, 'n_threads') else None,
                    verbose=self.verbose
                )
                
                if self.verbose:
                    load_time = time.time() - start_time
                    print(f"Model loaded in {load_time:.2f} seconds")
                    
            except ImportError:
                raise ImportError(
                    "llama-cpp-python is required. Install with: "
                    "pip install llama-cpp-python"
                )
    
    def set_vehicle_context(
        self,
        make: str,
        model: str,
        year: int,
        mileage: int,
        vin: Optional[str] = None
    ):
        """
        Set the vehicle context for personalized responses
        
        Args:
            make: Vehicle manufacturer (e.g., "Toyota")
            model: Vehicle model (e.g., "Camry")
            year: Model year
            mileage: Current mileage in miles
            vin: Vehicle Identification Number (optional)
        """
        self.vehicle_context = VehicleContext(
            make=make,
            model=model,
            year=year,
            mileage=mileage,
            vin=vin
        )
        
        if self.verbose:
            print(f"Vehicle context set: {year} {make} {model}")
    
    def _build_prompt(self, user_message: str) -> str:
        """
        Build the full prompt including system prompt, vehicle context, and history
        
        Args:
            user_message: The user's current question
            
        Returns:
            Complete prompt string
        """
        prompt_parts = [self.system_prompt]
        
        # Add vehicle context if available
        if self.vehicle_context:
            prompt_parts.append(self.vehicle_context.to_prompt())
        
        # Add conversation history (last 5 turns for context window management)
        if self.conversation_history:
            prompt_parts.append("Previous conversation:")
            for turn in self.conversation_history[-5:]:
                prompt_parts.append(f"User: {turn['user']}")
                prompt_parts.append(f"Assistant: {turn['assistant']}")
        
        # Add current user message
        prompt_parts.append(f"User: {user_message}")
        prompt_parts.append("Assistant:")
        
        return "\n\n".join(prompt_parts)
    
    def ask(
        self,
        question: str,
        max_tokens: int = 256,
        temperature: float = 0.7,
        stream: bool = False
    ) -> str:
        """
        Ask the assistant a question
        
        Args:
            question: User's question
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            stream: Whether to stream the response
            
        Returns:
            Assistant's response as a string
        """
        # Lazy load LLM if not already loaded
        self._load_llm()
        
        # Build the full prompt
        prompt = self._build_prompt(question)
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"User: {question}")
            print(f"{'='*60}")
            start_time = time.time()
        
        # Generate response
        response = self._llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["User:", "\n\n\n"],
            echo=False
        )
        
        # Extract the text
        response_text = response['choices'][0]['text'].strip()
        
        # Update conversation history
        self.conversation_history.append({
            'user': question,
            'assistant': response_text
        })
        
        if self.verbose:
            inference_time = time.time() - start_time
            tokens_generated = response['usage']['completion_tokens']
            tokens_per_sec = tokens_generated / inference_time
            
            print(f"Assistant: {response_text}")
            print(f"\nMetrics:")
            print(f"  Inference time: {inference_time:.2f}s")
            print(f"  Tokens generated: {tokens_generated}")
            print(f"  Speed: {tokens_per_sec:.1f} tokens/sec")
            print(f"{'='*60}\n")
        
        return response_text
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        if self.verbose:
            print("Conversation history cleared")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the full conversation history"""
        return self.conversation_history
    
    def save_conversation(self, filepath: str):
        """
        Save conversation history to a JSON file
        
        Args:
            filepath: Path to save the conversation
        """
        conversation_data = {
            'vehicle_context': self.vehicle_context.__dict__ if self.vehicle_context else None,
            'conversation': self.conversation_history
        }
        
        with open(filepath, 'w') as f:
            json.dump(conversation_data, f, indent=2)
        
        if self.verbose:
            print(f"Conversation saved to {filepath}")
    
    def load_conversation(self, filepath: str):
        """
        Load conversation history from a JSON file
        
        Args:
            filepath: Path to the saved conversation
        """
        with open(filepath, 'r') as f:
            conversation_data = json.load(f)
        
        # Restore vehicle context
        if conversation_data['vehicle_context']:
            ctx = conversation_data['vehicle_context']
            self.vehicle_context = VehicleContext(**ctx)
        
        # Restore conversation history
        self.conversation_history = conversation_data['conversation']
        
        if self.verbose:
            print(f"Conversation loaded from {filepath}")
            print(f"Restored {len(self.conversation_history)} conversation turns")


# Example usage
if __name__ == "__main__":
    # Initialize assistant
    assistant = VehicleAssistant(
        model_path="models/phi-2-4bit.gguf",
        context_size=4096,
        verbose=True
    )
    
    # Set vehicle context
    assistant.set_vehicle_context(
        make="Toyota",
        model="Camry",
        year=2023,
        mileage=15000
    )
    
    # Example interactions
    print("\n" + "="*60)
    print("TinyLLM-Auto - Vehicle Assistant Demo")
    print("="*60 + "\n")
    
    # Diagnostic code question
    response = assistant.ask("What does P0420 diagnostic code mean?")
    
    # Follow-up question
    response = assistant.ask("How serious is this issue?")
    
    # Feature question
    response = assistant.ask("How do I connect my phone via Bluetooth?")
    
    # Save conversation
    assistant.save_conversation("conversation_history.json")
