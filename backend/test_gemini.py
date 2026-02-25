"""
Test Google Gemini Integration - Quick Test
"""
import asyncio
from agents.google_agent import TodoMasterAgent

async def test_gemini():
    print("=" * 60)
    print("Testing Google Gemini Integration")
    print("=" * 60)
    
    # Create agent
    agent = TodoMasterAgent(
        user_id="test-user-123",
        user_email="test@example.com",
        username="Test User"
    )
    
    # Test 1: Simple greeting
    print("\n1. Testing simple greeting...")
    response = await agent.chat("Hello!")
    print(f"   Response: {response['text'][:100]}...")
    
    # Test 2: Add task (will fail without DB but tests tool calling)
    print("\n2. Testing add task...")
    response = await agent.chat("Add a task to practice math tomorrow at 3pm")
    print(f"   Response: {response['text'][:100]}...")
    print(f"   Tool calls: {len(response['tool_calls'])}")
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_gemini())
