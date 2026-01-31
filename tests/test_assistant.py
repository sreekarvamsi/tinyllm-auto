"""
Unit tests for VehicleAssistant
Tests that don't require actual model loading for CI/CD
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from assistant import VehicleContext


class TestVehicleContext:
    """Test VehicleContext dataclass"""
    
    def test_vehicle_context_creation(self):
        """Test creating a vehicle context"""
        context = VehicleContext(
            make="Toyota",
            model="Camry",
            year=2023,
            mileage=15000
        )
        
        assert context.make == "Toyota"
        assert context.model == "Camry"
        assert context.year == 2023
        assert context.mileage == 15000
    
    def test_vehicle_context_to_prompt(self):
        """Test converting context to prompt string"""
        context = VehicleContext(
            make="Honda",
            model="Civic",
            year=2022,
            mileage=20000
        )
        
        prompt = context.to_prompt()
        
        assert "Honda" in prompt
        assert "Civic" in prompt
        assert "2022" in prompt
        assert "20,000" in prompt


class TestVehicleAssistantStructure:
    """Test VehicleAssistant class structure without loading models"""
    
    def test_assistant_initialization_structure(self):
        """Test assistant initialization without loading model"""
        # Import here to avoid loading llama_cpp
        from assistant import VehicleAssistant
        
        assistant = VehicleAssistant(
            model_path="test_model.gguf",
            context_size=2048,
            verbose=False
        )
        
        assert assistant.model_path == "test_model.gguf"
        assert assistant.context_size == 2048
        assert assistant.conversation_history == []
        assert assistant.vehicle_context is None
        assert assistant._llm is None  # Should not be loaded yet
    
    def test_set_vehicle_context(self):
        """Test setting vehicle context"""
        from assistant import VehicleAssistant
        
        assistant = VehicleAssistant(
            model_path="test_model.gguf",
            verbose=False
        )
        
        assistant.set_vehicle_context(
            make="Tesla",
            model="Model 3",
            year=2024,
            mileage=5000
        )
        
        assert assistant.vehicle_context.make == "Tesla"
        assert assistant.vehicle_context.model == "Model 3"
        assert assistant.vehicle_context.year == 2024
        assert assistant.vehicle_context.mileage == 5000
    
    def test_build_prompt_without_context(self):
        """Test prompt building without vehicle context"""
        from assistant import VehicleAssistant
        
        assistant = VehicleAssistant(
            model_path="test_model.gguf",
            verbose=False
        )
        
        prompt = assistant._build_prompt("What is P0420?")
        
        assert "automotive assistant" in prompt.lower()
        assert "What is P0420?" in prompt
        assert "User:" in prompt
        assert "Assistant:" in prompt
    
    def test_build_prompt_with_context(self):
        """Test prompt building with vehicle context"""
        from assistant import VehicleAssistant
        
        assistant = VehicleAssistant(
            model_path="test_model.gguf",
            verbose=False
        )
        
        assistant.set_vehicle_context(
            make="Ford",
            model="F-150",
            year=2023,
            mileage=10000
        )
        
        prompt = assistant._build_prompt("Check engine light on")
        
        assert "Ford" in prompt
        assert "F-150" in prompt
        assert "2023" in prompt
        assert "Check engine light on" in prompt
    
    def test_conversation_history_management(self):
        """Test conversation history management"""
        from assistant import VehicleAssistant
        
        assistant = VehicleAssistant(
            model_path="test_model.gguf",
            verbose=False
        )
        
        # Manually add to history
        assistant.conversation_history.append({
            'user': 'Question 1',
            'assistant': 'Answer 1'
        })
        
        assert len(assistant.conversation_history) == 1
        assert assistant.conversation_history[0]['user'] == 'Question 1'
        
        # Test reset
        assistant.reset_conversation()
        assert len(assistant.conversation_history) == 0
    
    def test_system_prompt_content(self):
        """Test that system prompt contains key elements"""
        from assistant import VehicleAssistant
        
        assistant = VehicleAssistant(
            model_path="test_model.gguf",
            verbose=False
        )
        
        system_prompt = assistant.system_prompt.lower()
        
        # Check for key automotive concepts
        assert "automotive" in system_prompt or "vehicle" in system_prompt
        assert "diagnostic" in system_prompt
        assert "safety" in system_prompt
    
    def test_get_conversation_history(self):
        """Test retrieving conversation history"""
        from assistant import VehicleAssistant
        
        assistant = VehicleAssistant(
            model_path="test_model.gguf",
            verbose=False
        )
        
        # Add some history
        assistant.conversation_history = [
            {'user': 'Q1', 'assistant': 'A1'},
            {'user': 'Q2', 'assistant': 'A2'}
        ]
        
        history = assistant.get_conversation_history()
        assert len(history) == 2
        assert history[0]['user'] == 'Q1'


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_conversation_history(self):
        """Test behavior with empty conversation history"""
        from assistant import VehicleAssistant
        
        assistant = VehicleAssistant(
            model_path="test_model.gguf",
            verbose=False
        )
        
        history = assistant.get_conversation_history()
        assert history == []
    
    def test_long_conversation_history_truncation(self):
        """Test handling of long conversation history"""
        from assistant import VehicleAssistant
        
        assistant = VehicleAssistant(
            model_path="test_model.gguf",
            verbose=False
        )
        
        # Add many conversation turns
        for i in range(10):
            assistant.conversation_history.append({
                'user': f'Question {i}',
                'assistant': f'Answer {i}'
            })
        
        # Build prompt should only include last 5 turns
        prompt = assistant._build_prompt("New question")
        
        # Count occurrences of "User:" in prompt
        user_count = prompt.count("User:")
        # Should be 6: 5 from history + 1 current
        assert user_count == 6
    
    def test_vehicle_context_optional_vin(self):
        """Test that VIN is optional in vehicle context"""
        context = VehicleContext(
            make="BMW",
            model="X5",
            year=2021,
            mileage=30000
        )
        
        assert context.vin is None
        
        # Test with VIN
        context_with_vin = VehicleContext(
            make="BMW",
            model="X5",
            year=2021,
            mileage=30000,
            vin="1234567890ABCDEFG"
        )
        
        assert context_with_vin.vin == "1234567890ABCDEFG"


class TestImports:
    """Test that all modules can be imported"""
    
    def test_import_assistant(self):
        """Test importing assistant module"""
        from assistant import VehicleAssistant, VehicleContext
        assert VehicleAssistant is not None
        assert VehicleContext is not None
    
    def test_import_package(self):
        """Test importing from package"""
        import sys
        from pathlib import Path
        
        # Ensure src is in path
        src_path = str(Path(__file__).parent.parent / "src")
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # Import from package
        try:
            from assistant import VehicleAssistant
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])