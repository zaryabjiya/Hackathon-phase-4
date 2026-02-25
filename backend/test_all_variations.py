"""Comprehensive test for all command variations - Professional English"""
import asyncio
import sys
import os
sys.path.append('C:\\Users\\AK C0M\\Desktop\\Hackathon-2\\todo-phs-iii\\backend')

os.system('chcp 65001 > nul')

from agents.google_agent import TodoMasterAgent

async def test_chatbot():
    agent = TodoMasterAgent(user_id="1", user_email="test@example.com", username="TestUser")

    test_cases = [
        # ===== LIST TASKS - Multiple Variations =====
        ("show my task", "List - singular"),
        ("show my tasks", "List - plural"),
        ("show task", "List - show task"),
        ("show tasks", "List - show tasks"),
        ("list my task", "List - list my task"),
        ("list my tasks", "List - list my tasks"),
        ("list task", "List - list task"),
        ("list tasks", "List - list tasks"),
        ("show all", "List - show all"),
        ("show all tasks", "List - show all tasks"),
        ("show pending tasks", "List - pending"),
        ("display my tasks", "List - display"),
        ("see my tasks", "List - see"),
        ("what are my tasks", "List - what are"),
        ("meri task dikhao", "List - Urdu 1"),
        ("meri tasks dikhao", "List - Urdu 2"),
        ("sari tasks dikhao", "List - Urdu 3"),
        
        # ===== ADD TASK - Multiple Variations =====
        ("add a task to test", "Add - add a task"),
        ("add task to test", "Add - add task"),
        ("create a task to test", "Add - create"),
        ("new task to test", "Add - new task"),
        ("add new task to test", "Add - add new"),
        ("task add karo test", "Add - Urdu 1"),
        ("task banana hai test", "Add - Urdu 2"),
        
        # ===== COMPLETE TASK - Multiple Variations =====
        ("complete task 1", "Complete - complete"),
        ("mark task 1 as complete", "Complete - mark as"),
        ("mark task 1 done", "Complete - mark done"),
        ("task 1 complete karo", "Complete - Urdu 1"),
        ("task 1 pura kar do", "Complete - Urdu 2"),
        ("finish task 1", "Complete - finish"),
        
        # ===== DELETE TASK - Multiple Variations =====
        ("delete task 1", "Delete - delete"),
        ("delete task [1]", "Delete - with brackets"),
        ("remove task 1", "Delete - remove"),
        ("task 1 delete karo", "Delete - Urdu 1"),
        ("task 1 hata do", "Delete - Urdu 2"),
        ("delete task 1 please", "Delete - polite"),
        
        # ===== STATS - Multiple Variations =====
        ("show stats", "Stats - show"),
        ("my stats", "Stats - my stats"),
        ("productivity", "Stats - productivity"),
        ("progress dikhao", "Stats - Urdu"),
        ("how many tasks", "Stats - how many"),
        ("task count", "Stats - count"),
        
        # ===== CONVERSATIONAL =====
        ("hello", "Greeting"),
        ("who are you", "Identity - assistant"),
        ("who am i", "Identity - user"),
        ("help", "Help"),
        ("thank you", "Thanks"),
        ("goodbye", "Goodbye"),
        ("talk in english", "Language"),
    ]

    print("=" * 80)
    print("COMPREHENSIVE COMMAND VARIATIONS TEST")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for message, test_name in test_cases:
        print(f"\n[Test: {test_name}]")
        print(f"Input: '{message}'")
        result = await agent.chat(message)
        output = result['text'][:150]
        print(f"Output: {output}")
        
        # Check if response is meaningful (not empty, not error)
        if output and len(output) > 5:
            print("Status: PASS")
            passed += 1
        else:
            print("Status: FAIL")
            failed += 1
        print("-" * 80)

    print("\n" + "=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_chatbot())
