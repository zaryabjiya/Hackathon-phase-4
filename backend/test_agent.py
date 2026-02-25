"""Quick test of TodoMaster Agent"""
import asyncio
from agents.google_agent import TodoMasterAgent

async def test():
    print("=" * 60)
    print("Testing TodoMaster Agent")
    print("=" * 60)
    
    agent = TodoMasterAgent(
        user_id="4",  # Your user ID
        user_email="zaryab.ned@gmail.com",
        username="zaryab irfan"
    )
    
    # Test 1: Add task
    print("\n1. Testing ADD TASK...")
    response = await agent.chat("Add a task to practice math")
    print(f"   Response: {response['text']}")
    
    # Test 2: List tasks
    print("\n2. Testing LIST TASKS...")
    response = await agent.chat("Show my tasks")
    print(f"   Response: {response['text'][:200]}...")
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test())
