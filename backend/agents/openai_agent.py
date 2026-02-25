"""TodoMaster AI Agent with OpenAI native tool calling"""
import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

logger = logging.getLogger(__name__)

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    timeout=30.0  # Add timeout to prevent hanging
)

# System prompt for TodoMaster Pro
TODO_MASTER_SYSTEM_PROMPT = """You are TodoMaster Pro - an intelligent AI assistant for task management.

## USER CONTEXT
- User Email: {user_email}
- Username: {username}

## YOUR CAPABILITIES
You help users manage tasks: add, list, complete, delete, update, search tasks, and get productivity stats.

## TOOL USAGE RULES
1. ALWAYS use tools for ANY task operation - never make up data
2. When user wants to add/list/update/delete/search tasks - CALL THE APPROPRIATE TOOL
3. For deletion - ALWAYS confirm with user first: "Are you sure you want to delete [task title]?"
4. After tool executes - give a brief, friendly confirmation

## RESPONSE STYLE
- Be concise (1-3 sentences)
- Use emojis appropriately: ✅ ✏️ 🗑️ 🎉 📅 ⚠️ 🚨
- Reference actual task titles/IDs
- Be professional but friendly

## GREETING
"Hello! I'm TodoMaster Pro. How can I help you manage your tasks today?"
"""


class TodoMasterAgent:
    """TodoMaster AI Agent with OpenAI native tool calling"""

    def __init__(self, user_id: str, user_email: Optional[str] = None, username: Optional[str] = None):
        self.user_id = user_id  # Keep as string for Better Auth compatibility
        self.user_email = user_email or "unknown"
        self.username = username or "User"
        self.system_prompt = TODO_MASTER_SYSTEM_PROMPT.format(
            user_email=self.user_email,
            username=self.username
        )

    async def chat(self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Send message to OpenAI and get response with automatic tool execution
        
        Args:
            message: User's message
            conversation_history: List of previous messages in format [{"role": "user"/"assistant", "content": "..."}]
        
        Returns:
            Dict with response text, tool calls, and tool results
        """
        try:
            logger.info(f"Calling OpenAI with message: {message[:100]}...")
            
            # Build messages array
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history if available
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI with tools
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=self._get_tools_schema(),
                tool_choice="auto",
                temperature=0.7,
                max_tokens=1024
            )
            
            assistant_message = response.choices[0].message
            
            logger.info(f"OpenAI response: has_tool_calls={bool(assistant_message.tool_calls)}")
            
            # Check if there are tool calls to execute
            tool_results = []
            if assistant_message.tool_calls:
                logger.info(f"Found {len(assistant_message.tool_calls)} tool calls to execute")
                
                # Execute each tool call
                for tool_call in assistant_message.tool_calls:
                    result = await self._execute_tool(tool_call)
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "tool_name": tool_call.function.name,
                        "result": result
                    })
                    logger.info(f"Tool executed: {tool_call.function.name} -> {result}")
                
                # Add assistant's message with tool calls to messages
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })
                
                # Add tool results to messages
                for tool_result in tool_results:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_result["tool_call_id"],
                        "content": str(tool_result["result"])
                    })
                
                # Get final response from OpenAI after tool execution
                final_response = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=512
                )
                
                return {
                    "text": final_response.choices[0].message.content,
                    "tool_calls": assistant_message.tool_calls,
                    "tool_results": tool_results,
                    "conversation_id": None
                }
            
            # No tool calls - return direct response
            return {
                "text": assistant_message.content,
                "tool_calls": [],
                "tool_results": [],
                "conversation_id": None
            }
            
        except Exception as e:
            logger.error(f"Error in agent chat: {e}", exc_info=True)
            return {
                "text": f"Sorry, kuch error ho gaya: {str(e)} 😅",
                "tool_calls": [],
                "tool_results": [],
                "conversation_id": None
            }

    async def _execute_tool(self, tool_call) -> Dict[str, Any]:
        """Execute a tool call from OpenAI"""
        try:
            tool_name = tool_call.function.name
            import json
            params = json.loads(tool_call.function.arguments)
            
            # Ensure user_id is string (Better Auth compatibility)
            params['user_id'] = str(self.user_id)
            
            logger.info(f"Executing tool: {tool_name} with params: {params}")
            
            # Import and execute the appropriate tool
            from mcp.tools import add_task, list_tasks, complete_task, delete_task, update_task, search_tasks, get_task_stats
            from mcp.server import AddTaskParams, ListTasksParams, CompleteTaskParams, DeleteTaskParams, UpdateTaskParams
            
            # Create proper param objects for each tool
            if tool_name == 'add_task':
                tool_params = AddTaskParams(**{k: v for k, v in params.items() if v is not None})
                result = await add_task(tool_params)
            elif tool_name == 'list_tasks':
                tool_params = ListTasksParams(**{k: v for k, v in params.items() if v is not None})
                result = await list_tasks(tool_params)
            elif tool_name == 'complete_task':
                tool_params = CompleteTaskParams(**{k: v for k, v in params.items() if v is not None})
                result = await complete_task(tool_params)
            elif tool_name == 'delete_task':
                tool_params = DeleteTaskParams(**{k: v for k, v in params.items() if v is not None})
                result = await delete_task(tool_params)
            elif tool_name == 'update_task':
                tool_params = UpdateTaskParams(**{k: v for k, v in params.items() if v is not None})
                result = await update_task(tool_params)
            elif tool_name == 'search_tasks':
                result = await search_tasks(params)
            elif tool_name == 'get_task_stats':
                result = await get_task_stats(params)
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}", exc_info=True)
            return {"error": str(e)}

    def _get_tools_schema(self) -> List[Dict[str, Any]]:
        """Get OpenAI-compatible tool schemas"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task with title, optional description, due date, and priority",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Task title (1-200 chars)"},
                            "description": {"type": "string", "description": "Optional task description (max 1000 chars)"},
                            "due_date": {"type": "string", "description": "Due date in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"},
                            "priority": {"type": "string", "description": "Priority level: low, medium, high, urgent", "enum": ["low", "medium", "high", "urgent"]}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List tasks for the user with optional status filter",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "description": "Filter: all, pending, completed, high_priority, overdue, today, this_week",
                                "enum": ["all", "pending", "completed", "high_priority", "overdue", "today", "this_week"]
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed by ID",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "Task ID to complete"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task by ID (requires prior confirmation from user)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "Task ID to delete"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update task title, description, priority, or due date",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "Task ID to update"},
                            "title": {"type": "string", "description": "New title (optional)"},
                            "description": {"type": "string", "description": "New description (optional)"},
                            "priority": {"type": "string", "description": "New priority: low, medium, high, urgent (optional)", "enum": ["low", "medium", "high", "urgent"]},
                            "due_date": {"type": "string", "description": "New due date in ISO format (optional)"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_tasks",
                    "description": "Search tasks by keyword in title or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search keyword or phrase"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_task_stats",
                    "description": "Get task statistics and productivity summary",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "period": {"type": "string", "description": "Time period: today, week, month, all", "enum": ["today", "week", "month", "all"]}
                        }
                    }
                }
            }
        ]


def create_todo_master_agent(user_id: str, user_email: Optional[str] = None, username: Optional[str] = None) -> TodoMasterAgent:
    """Factory function to create TodoMaster agent"""
    return TodoMasterAgent(user_id=user_id, user_email=user_email, username=username)
