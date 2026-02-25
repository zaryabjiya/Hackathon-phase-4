"""TodoMaster AI Agent with Cohere integration"""
import cohere
import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize Cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY not found in environment variables")

co = cohere.Client(COHERE_API_KEY)

# TodoMaster System Prompt - Professional Version (Works with Cohere Free Tier)
TODO_MASTER_SYSTEM_PROMPT = """You are TodoMaster Pro - an intelligent AI assistant for task management.

## USER CONTEXT
- User Email: {user_email}
- Username: {username}

## YOUR CAPABILITIES
You help users manage tasks: add, list, complete, delete, update, search tasks, and get stats.

## RESPONSE STYLE
- Be concise (1-3 sentences)
- Use emojis: ✅ ✏️ 🗑️ 🎉 📅 ⚠️ 🚨
- Be professional but friendly

## IMPORTANT
You are a conversational AI. When users ask about tasks, respond helpfully and let them know you can assist with task management.

## GREETING
"Hello! I'm TodoMaster Pro. How can I help you manage your tasks today?"
"""


class TodoMasterAgent:
    """TodoMaster AI Agent for conversational todo management"""

    def __init__(self, user_id: str, user_email: Optional[str] = None, username: Optional[str] = None):
        self.user_id = user_id
        self.user_email = user_email
        self.username = username
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build system prompt with user context"""
        return TODO_MASTER_SYSTEM_PROMPT.format(
            user_email=self.user_email or "unknown",
            username=self.username or "User"
        )

    async def chat(self, message: str, chat_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Send message to Cohere and get conversational response
        Note: Tool calling requires Cohere paid tier, using conversational mode for free tier
        """
        try:
            logger.info(f"Calling Cohere with message: {message[:100]}...")
            
            # Call Cohere (without tools for free tier compatibility)
            response = co.chat(
                message=message,
                chat_history=chat_history,
                preamble=self.system_prompt,
                temperature=0.7,
                max_tokens=512
            )

            logger.info(f"Cohere response: {response.text[:100] if response.text else 'None'}...")

            return {
                "text": response.text,
                "tool_calls": [],
                "tool_results": [],
                "conversation_id": getattr(response, 'conversation_id', None)
            }

    def _get_tools_schema(self) -> List[Dict[str, Any]]:
        """Get tool schemas for Cohere (requires paid tier)"""
        # Note: Tool calling requires Cohere paid tier
        return []


def create_todo_master_agent(user_id: str, user_email: Optional[str] = None) -> TodoMasterAgent:
    """Factory function to create TodoMaster agent"""
    return TodoMasterAgent(user_id=user_id, user_email=user_email)
