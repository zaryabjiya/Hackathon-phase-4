"""Test script for improved chatbot with Roman Urdu support"""
import asyncio
import sys
import os
sys.path.append('C:\\Users\\AK C0M\\Desktop\\Hackathon-2\\todo-phs-iii\\backend')

# Fix Windows console encoding
os.system('chcp 65001 > nul')

from agents.google_agent import TodoMasterAgent

async def test_chatbot():
    agent = TodoMasterAgent(user_id="1", user_email="test@example.com", username="TestUser")
    
    test_cases = [
        # English commands
        ("Add a task to buy groceries", "Add task English"),
        ("Add task to learn Python description: Start on Monday", "Add task with description"),
        ("Show my tasks", "List tasks"),
        ("Complete task 1", "Complete task"),
        ("Delete task 2", "Delete task"),
        ("Show my productivity", "Get stats"),
        
        # Roman Urdu commands
        ("Task add karo kal meeting ke liye", "Add task Urdu"),
        ("Meri tasks dikhao", "List tasks Urdu"),
        ("Task 1 complete karo", "Complete task Urdu"),
        ("Task 2 delete karo", "Delete task Urdu"),
        ("Mera progress dikhao", "Stats Urdu"),
        ("Hello", "Greeting"),
        ("Shukriya", "Thanks"),
    ]
    
    print("=" * 60)
    print("TODO MASTER CHATBOT - TEST RESULTS")
    print("=" * 60)
    
    for message, test_name in test_cases:
        print(f"\n[Test: {test_name}]")
        print(f"Input: '{message}'")
        result = await agent.chat(message)
        print(f"Output: {result['text'][:200]}")
        print("-" * 60)
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    asyncio.run(test_chatbot())
