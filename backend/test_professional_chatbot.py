"""Test script for professional English responses"""
import asyncio
import sys
import os
sys.path.append('C:\\Users\\AK C0M\\Desktop\\Hackathon-2\\todo-phs-iii\\backend')

# Fix Windows console encoding
os.system('chcp 65001 > nul')

from agents.google_agent import TodoMasterAgent

async def test_chatbot():
    agent = TodoMasterAgent(user_id="1", user_email="user@example.com", username="John Doe")

    test_cases = [
        # Professional responses tests
        ("Hello", "Greeting"),
        ("Who are you", "Identity - Assistant"),
        ("Who am I", "Identity - User"),
        ("What is my name", "User Info - Name"),
        ("What is my email", "User Info - Email"),
        ("Help", "Help Request"),
        ("What can you do", "Capabilities"),
        ("Talk in English", "Language Preference"),
        ("Thank you", "Thanks"),
        ("Goodbye", "Goodbye"),
        ("I need help with tasks", "General Query"),
    ]

    print("=" * 80)
    print("TODO MASTER PROFESSIONAL CHATBOT - TEST RESULTS")
    print("=" * 80)

    for message, test_name in test_cases:
        print(f"\n[Test: {test_name}]")
        print(f"Input: '{message}'")
        result = await agent.chat(message)
        print(f"Output:\n{result['text']}")
        print("-" * 80)

    print("\nAll tests completed!")

if __name__ == "__main__":
    asyncio.run(test_chatbot())
