"""
TinyLLM-Auto: Command Line Demo
Simple CLI interface for testing the automotive assistant
"""

import argparse
from pathlib import Path
from assistant import VehicleAssistant


def main():
    parser = argparse.ArgumentParser(
        description="TinyLLM-Auto: In-Vehicle AI Assistant Demo"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="models/phi-2-4bit.gguf",
        help="Path to GGUF model file"
    )
    parser.add_argument(
        "--make",
        type=str,
        default="Toyota",
        help="Vehicle make"
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default="Camry",
        help="Vehicle model"
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2023,
        help="Vehicle year"
    )
    parser.add_argument(
        "--mileage",
        type=int,
        default=15000,
        help="Current mileage"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Check if model exists
    if not Path(args.model).exists():
        print("❌ Error: Model file not found!")
        print(f"   Looking for: {args.model}")
        print("\n📥 Please download the model first:")
        print("   python scripts/download_model.py")
        return
    
    print("="*60)
    print("🚗 TinyLLM-Auto: In-Vehicle AI Assistant")
    print("="*60)
    print()
    
    # Initialize assistant
    print("Loading model...")
    assistant = VehicleAssistant(
        model_path=args.model,
        context_size=4096,
        verbose=args.verbose
    )
    
    # Set vehicle context
    assistant.set_vehicle_context(
        make=args.make,
        model=args.model_name,
        year=args.year,
        mileage=args.mileage
    )
    
    print(f"✓ Assistant ready for: {args.year} {args.make} {args.model_name}")
    print()
    
    # Demo questions
    demo_questions = [
        "What does P0420 diagnostic code mean?",
        "How serious is this issue?",
        "Can I still drive the car?",
    ]
    
    print("Running demo conversation...")
    print("="*60)
    print()
    
    for question in demo_questions:
        print(f"👤 User: {question}")
        response = assistant.ask(question)
        print(f"🤖 Assistant: {response}")
        print()
        print("-"*60)
        print()
    
    # Interactive mode
    print("Entering interactive mode...")
    print("Type 'quit' to exit, 'reset' to clear conversation history")
    print("="*60)
    print()
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'reset':
                assistant.reset_conversation()
                print("✓ Conversation reset\n")
                continue
            
            response = assistant.ask(user_input)
            print(f"🤖 Assistant: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()
