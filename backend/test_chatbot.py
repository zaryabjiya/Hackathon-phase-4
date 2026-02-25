"""
Test script for TodoMaster Pro Chatbot with OpenAI

This script tests natural language task management commands.
Make sure the backend is running on http://localhost:8000

Usage:
    python test_chatbot.py
"""
import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000"
USER_ID = "1"  # Replace with your actual user ID from Better Auth
USER_EMAIL = "test@example.com"

# Test credentials (you need to login first to get a token)
# Run this after logging in via the frontend

def get_auth_token():
    """Get auth token by logging in"""
    print("📝 Getting auth token...")
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        data={
            "username": USER_EMAIL,
            "password": "your-password"  # Replace with actual password
        }
    )
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"✅ Token obtained: {token[:20]}...")
        return token
    else:
        print(f"❌ Login failed: {response.text}")
        return None


def test_chat(message: str, token: str, conversation_id: str = None):
    """Send a message to the chatbot"""
    print(f"\n💬 Sending: '{message}'")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "message": message,
        "conversation_id": conversation_id
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/{USER_ID}/chat",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"🤖 Response: {data.get('response', 'No response')}")
        
        if data.get('tool_calls'):
            print(f"🔧 Tool calls: {json.dumps(data['tool_calls'], indent=2)}")
        
        return data.get('conversation_id')
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None


def run_tests():
    """Run all test scenarios"""
    print("=" * 60)
    print("🤖 TodoMaster Pro Chatbot - Natural Language Tests")
    print("=" * 60)
    
    # Get auth token
    token = get_auth_token()
    if not token:
        print("\n⚠️  Skipping tests - no auth token")
        print("   Please login via frontend first, then use the token from localStorage")
        token = input("Enter token manually: ")
    
    conversation_id = None
    
    # Test 1: List tasks
    print("\n" + "=" * 60)
    print("TEST 1: List pending tasks")
    print("=" * 60)
    conversation_id = test_chat("Show my pending tasks", token, conversation_id)
    
    # Test 2: Add task
    print("\n" + "=" * 60)
    print("TEST 2: Add a new task")
    print("=" * 60)
    conversation_id = test_chat("Add a task to practice math tomorrow at 3pm with high priority", token, conversation_id)
    
    # Test 3: Add another task
    print("\n" + "=" * 60)
    print("TEST 3: Add another task")
    print("=" * 60)
    conversation_id = test_chat("Add task: Buy groceries from the store", token, conversation_id)
    
    # Test 4: List all tasks
    print("\n" + "=" * 60)
    print("TEST 4: List all tasks")
    print("=" * 60)
    conversation_id = test_chat("Show all my tasks", token, conversation_id)
    
    # Test 5: Complete a task
    print("\n" + "=" * 60)
    print("TEST 5: Complete a task (task ID 1)")
    print("=" * 60)
    conversation_id = test_chat("Mark task 1 as complete", token, conversation_id)
    
    # Test 6: Search tasks
    print("\n" + "=" * 60)
    print("TEST 6: Search tasks")
    print("=" * 60)
    conversation_id = test_chat("Find tasks about math", token, conversation_id)
    
    # Test 7: Get stats
    print("\n" + "=" * 60)
    print("TEST 7: Get productivity stats")
    print("=" * 60)
    conversation_id = test_chat("Show my productivity statistics", token, conversation_id)
    
    # Test 8: User context
    print("\n" + "=" * 60)
    print("TEST 8: Ask about user info")
    print("=" * 60)
    conversation_id = test_chat("What is my email?", token, conversation_id)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print(f"\n💡 Final conversation_id: {conversation_id}")
    print(f"   Use this ID to continue the conversation")


if __name__ == "__main__":
    run_tests()
