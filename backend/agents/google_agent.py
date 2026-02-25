"""TodoMaster AI Agent with Rule-based Intent Detection (No Gemini Required)"""
import os
import logging
import re
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# System prompt for responses (not used in rule-based mode)
TODO_MASTER_SYSTEM_PROMPT = """You are TodoMaster Pro - a friendly AI task management assistant."""


class TodoMasterAgent:
    """TodoMaster AI Agent with Rule-based intent detection"""

    def __init__(self, user_id: str, user_email: Optional[str] = None, username: Optional[str] = None):
        self.user_id = user_id
        self.user_email = user_email or "unknown"
        self.username = username or "User"
        logger.info(f"Agent initialized for user: {self.username} ({self.user_email})")

    async def chat(self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Process user message and return response with tool execution
        """
        try:
            message_lower = message.lower()
            logger.info(f"Processing message: {message[:100]}...")

            # Detect intent and execute tools
            tool_result = await self._detect_and_execute(message_lower, message)

            if tool_result:
                # Tool was executed
                logger.info(f"Tool executed: {tool_result}")
                return {
                    "text": self._format_tool_response(tool_result),
                    "tool_calls": [tool_result],
                    "tool_results": [tool_result],
                    "conversation_id": None
                }

            # No tool matched - use fallback conversational response
            ai_response = self._get_fallback_response(message_lower)
            return {
                "text": ai_response,
                "tool_calls": [],
                "tool_results": [],
                "conversation_id": None
            }

        except Exception as e:
            logger.error(f"Error in agent chat: {e}", exc_info=True)
            return {
                "text": f"Sorry, kuch error ho gaya: {str(e)}",
                "tool_calls": [],
                "tool_results": [],
                "conversation_id": None
            }

    async def _detect_and_execute(self, message_lower: str, original_message: str) -> Optional[Dict[str, Any]]:
        """Detect intent from message and execute appropriate tool"""

        # UPDATE TASK: Must come before ADD TASK to avoid conflicts
        # Patterns: "update task X", "edit task X", "modify task X", "task X update"
        update_patterns = [
            'update task', 'edit task', 'modify task', 'change task',
            'task update', 'task edit', 'task modify', 'task change',
            'update kar', 'edit kar', 'change kar', 'update karo'
        ]
        if any(x in message_lower for x in update_patterns):
            # Extract task ID
            task_id_match = re.search(r'(?:task\s*)?\[?(\d+)\]?', message_lower)
            if task_id_match:
                task_id = int(task_id_match.group(1))
                
                # Extract title - look for "Title: X" pattern (handles semicolons)
                title_match = re.search(r'title\s*:\s*([^;]+?)(?:\s*;|\s+description\s*:|$)', original_message, re.IGNORECASE)
                title = title_match.group(1).strip() if title_match else None
                
                # Extract description - look for "Description: X" or "Description; X" pattern
                desc_match = re.search(r'description\s*[:;]\s*([^;]+?)(?:\s*;|\s+duedate\s*:|$)', original_message, re.IGNORECASE)
                description = desc_match.group(1).strip() if desc_match else None
                
                # Extract due date - look for "Duedate: X" or "Duedate; X" pattern
                due_date = None
                due_match = re.search(r'duedate\s*[:;]\s*(?:in\s+)?(\d+)\s*(?:din|days?|day)\s*(?:baad|bd|later|bad|in)?', original_message, re.IGNORECASE)
                if due_match:
                    days = int(due_match.group(1))
                    due_date = (datetime.utcnow() + timedelta(days=days)).strftime("%Y-%m-%d")
                
                logger.info(f"Updating task {task_id}: title={title}, description={description}, due_date={due_date}")
                return await self._execute_tool('update_task', {
                    'task_id': task_id,
                    'title': title,
                    'description': description,
                    'due_date': due_date
                })

        # UNMARK/INCOMPLETE TASK: Toggle completion status back to incomplete
        # Patterns: "unmark task X", "incomplete task X", "reopen task X", "mark task X incomplete"
        unmark_patterns = [
            'unmark task', 'incomplete task', 'reopen task', 'mark task incomplete',
            'task unmark', 'task incomplete', 'task reopen',
            'adhura karo', 'wapis adhura', 'unmark kar', 'incomplete kar'
        ]
        if any(x in message_lower for x in unmark_patterns):
            # Extract task ID
            task_id_match = re.search(r'(?:task\s*)?\[?(\d+)\]?', message_lower)
            if task_id_match:
                task_id = int(task_id_match.group(1))
                logger.info(f"Unmarking task {task_id} as incomplete")
                return await self._execute_tool('unmark_task', {
                    'task_id': task_id,
                    'completed': False
                })

        # ADD TASK: Comprehensive English + Roman Urdu patterns
        add_patterns = [
            'add task', 'create task', 'new task', 'add to do', 'add a task',
            'task add', 'banana hai', 'add karo', 'create karo', 'new task bana',
            'add new task', 'create new task', 'task banana', 'add todo'
        ]
        if any(x in message_lower for x in add_patterns):
            # Extract title - improved extraction
            title = self._extract_task_title_improved(original_message, message_lower)

            # Check for priority (English + Urdu)
            priority = "medium"
            if any(x in message_lower for x in ["high priority", "urgent", "zaroori", "jaldi", "high pe"]):
                priority = "high"
            elif any(x in message_lower for x in ["low priority", "kam zaroori", "low pe"]):
                priority = "low"

            # Check for due date - Enhanced with relative days support
            due_date = None
            
            # Check for "X days/din baad" pattern (e.g., "2 din baad", "5 days baad", "3 din bd")
            days_match = re.search(r'(\d+)\s*(?:din|days?|day)\s*(?:baad|bd|later|bad)', message_lower)
            if days_match:
                days = int(days_match.group(1))
                due_date = (datetime.utcnow() + timedelta(days=days)).strftime("%Y-%m-%d")
            elif "tomorrow" in message_lower or "kal" in message_lower:
                due_date = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")
            elif "today" in message_lower or "aaj" in message_lower:
                due_date = datetime.utcnow().strftime("%Y-%m-%d")
            elif "next week" in message_lower or "agle hafte" in message_lower:
                due_date = (datetime.utcnow() + timedelta(weeks=1)).strftime("%Y-%m-%d")

            # Extract description if present
            description = self._extract_description_improved(original_message, message_lower)

            logger.info(f"Adding task: title={title}, description={description}, priority={priority}, due_date={due_date}")
            return await self._execute_tool('add_task', {
                'title': title,
                'description': description,
                'priority': priority,
                'due_date': due_date
            })

        # LIST TASKS: Comprehensive patterns - English + Roman Urdu (singular/plural/flexible)
        list_patterns = [
            'show task', 'show tasks', 'list task', 'list tasks', 'my task', 'my tasks',
            'view task', 'view tasks', 'all tasks', 'pending task', 'pending tasks',
            'task dikhao', 'meri task', 'meri tasks', 'sari task', 'sari tasks',
            'show all', 'show my', 'list all', 'list my', 'display task', 'display tasks',
            'see task', 'see tasks', 'what are my tasks', 'what is my task'
        ]
        if any(x in message_lower for x in list_patterns):
            status = "pending" if ("pending" in message_lower or "adhura" in message_lower or "incomplete" in message_lower) else "all"
            return await self._execute_tool('list_tasks', {'status': status})

        # COMPLETE TASK: Comprehensive patterns - English + Roman Urdu
        complete_patterns = [
            'complete task', 'mark task', 'finish task', 'task complete', 'done task',
            'mark done', 'mark complete', 'finish karo', 'khatam', 'pura kiya', 'ho gaya',
            'complete karo', 'mark kar do', 'complete kar do', 'finish kar do',
            'task pura', 'task complete kar', 'mark as complete', 'mark as done'
        ]
        if any(x in message_lower for x in complete_patterns):
            # Extract task ID - handle formats like "1", "[1]", "task 1", "task [1]"
            task_id_match = re.search(r'(?:task\s*)?\[?(\d+)\]?', message_lower)
            if task_id_match:
                return await self._execute_tool('complete_task', {'task_id': int(task_id_match.group(1))})

        # DELETE TASK: Comprehensive patterns - English + Roman Urdu
        delete_patterns = [
            'delete task', 'remove task', 'task delete', 'task remove', 'hata do',
            'mita do', 'delete karo', 'remove karo', 'delete kar do', 'remove kar do',
            'task hata', 'task mita', 'delete this', 'remove this', 'drop task'
        ]
        if any(x in message_lower for x in delete_patterns):
            # Extract task ID - handle formats like "1", "[1]", "task 1", "task [1]"
            task_id_match = re.search(r'(?:task\s*)?\[?(\d+)\]?', message_lower)
            if task_id_match:
                return await self._execute_tool('delete_task', {'task_id': int(task_id_match.group(1))})

        # SEARCH TASKS: Comprehensive patterns - English + Roman Urdu
        search_patterns = ['search task', 'search tasks', 'find task', 'find tasks', 'task dhoondo', 'search karo', 'find karo', 'look for']
        if any(x in message_lower for x in search_patterns):
            query_match = re.search(r'(?:search|find|dhoondo|karo|look for)\s+(?:task\s+)?(.+)', message_lower)
            if query_match:
                return await self._execute_tool('search_tasks', {'query': query_match.group(1).strip()})

        # STATS: Comprehensive patterns - English + Roman Urdu
        stats_patterns = [
            'stats', 'productivity', 'summary', 'how many tasks', 'kitni task', 'mera progress',
            'count', 'task count', 'my stats', 'progress', 'report', 'analytics',
            'task stats', 'productivity stats', 'show stats', 'dikhao progress'
        ]
        if any(x in message_lower for x in stats_patterns):
            return await self._execute_tool('get_task_stats', {'period': 'all'})

        return None

    def _extract_task_title(self, original_message: str, message_lower: str) -> str:
        """Extract task title from user message"""
        # Patterns to remove from the message
        remove_patterns = [
            r'(?:add task|create task|new task|add to do|add a task|task add|add karo|create karo|new task bana|banana hai|task add karo)\s*',
            r'(?:due|tomorrow|kal|today|aaj|with description|description|high priority|low priority|urgent|zaroori|jaldi|kam zaroori|next week|agle hafte|ke liye|meeting).*$',
        ]

        title = original_message
        for pattern in remove_patterns:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE)

        title = title.strip()
        # Remove leading/trailing punctuation
        title = re.sub(r'^[\s\-\:]+|[\s\-\:]+$', '', title)

        if not title or len(title) < 2:
            return "New Task"

        # Title case for better formatting
        return title.title()

    def _extract_task_title_improved(self, original_message: str, message_lower: str) -> str:
        """Improved task title extraction - handles Title: X Description: Y format"""
        
        # First try to extract after common patterns
        patterns_to_remove = [
            r'(?:add\s+(?:a\s+)?task(?:\s+to)?|create\s+(?:a\s+)?task(?:\s+to)?|new\s+task(?:\s+to)?|add\s+to\s+do|task\s+add|add\s+karo|create\s+karo|task\s+banana|banana\s+hai)\s*',
        ]
        
        title = original_message
        for pattern in patterns_to_remove:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE)
        
        # SMART EXTRACTION: Look for "Title: X Description: Y" pattern
        # This handles: "Title: Movie Description: DDLJ Duedate: After 4days"
        title_match = re.search(r'title\s*:\s*([^;]+?)(?:\s+description\s*:|$)', title, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            # Fallback: Check for semicolon-separated format
            semicolon_match = re.search(r'^([^;]+?)(?:;|$)', title.strip(), re.IGNORECASE)
            if semicolon_match:
                title = semicolon_match.group(1).strip()
        
        # Remove any remaining "Description:", "Duedate:", "Due:" patterns
        title = re.sub(r'\s*description\s*:.*$', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\s*desc\s*:.*$', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\s*duedate\s*:.*$', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\s*due\s*date?\s*:.*$', '', title, flags=re.IGNORECASE)
        
        # Remove common trailing phrases
        trailing_patterns = [
            r'\s+due\s+.*$',
            r'\s+with\s+description\s+.*$',
            r'\s+tomorrow.*$',
            r'\s+kal.*$',
            r'\s+today.*$',
            r'\s+aaj.*$',
            r'\s+for\s+.*$',
        ]
        
        for pattern in trailing_patterns:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE)
        
        title = title.strip()
        title = re.sub(r'^[\s\-\:]+|[\s\-\:]+$', '', title)
        
        if not title or len(title) < 2:
            return "New Task"
        
        # Capitalize first letter of each word except articles
        words = title.split()
        capitalized = []
        for word in words:
            if word.lower() in ['a', 'an', 'the', 'to', 'for', 'in', 'on', 'at']:
                capitalized.append(word.lower())
            else:
                capitalized.append(word.capitalize())
        
        return ' '.join(capitalized)

    def _extract_description(self, original_message: str, message_lower: str) -> Optional[str]:
        """Extract description from user message"""
        # Look for "description" or "with" keywords
        desc_match = re.search(r'(?:with|description|desc)\s*[:\-]?\s*(.+?)(?:\s+due|\s+tomorrow|\s+kal|\s+today|\s+aaj|\s+duedate|$)', message_lower, re.IGNORECASE)
        if desc_match:
            desc = desc_match.group(1).strip()
            if desc and len(desc) > 3:
                return desc
        return None

    def _extract_description_improved(self, original_message: str, message_lower: str) -> Optional[str]:
        """Improved description extraction - handles Title: X Description: Y format"""
        
        # SMART EXTRACTION: Look for "Description: X" pattern first
        # This handles: "Title: Movie Description: DDLJ Duedate: After 4days"
        desc_match = re.search(r'description\s*:\s*([^;]+?)(?:\s+duedate\s*:|$)', original_message, re.IGNORECASE)
        if desc_match:
            desc = desc_match.group(1).strip()
            # Clean up - remove due date references
            desc = re.sub(r'\s*due\s+.*$', '', desc, flags=re.IGNORECASE)
            desc = re.sub(r'\s*duedate\s*:.*$', '', desc, flags=re.IGNORECASE)
            desc = desc.strip()
            if desc and len(desc) > 2:
                return desc
        
        # Fallback: Check for semicolon-separated format: "Title; Description; Due: ..."
        semicolon_parts = original_message.split(';')
        if len(semicolon_parts) >= 2:
            # Second part might be description
            potential_desc = semicolon_parts[1].strip()
            # Make sure it's not a due date pattern
            if not re.search(r'^due\s*date?\s*:', potential_desc, re.IGNORECASE):
                # Remove any due date info from description
                desc = re.sub(r'\s*due\s+.*$', '', potential_desc, flags=re.IGNORECASE)
                desc = re.sub(r'\s*duedate\s*:.*$', '', desc, flags=re.IGNORECASE)
                desc = desc.strip()
                if desc and len(desc) > 3:
                    return desc
        
        # Look for description after colon or "description:"
        desc_patterns = [
            r'description\s*:\s*(.+?)(?:\s+due|\s+tomorrow|\s+kal|\s+today|\s+duedate|$)',
            r':\s*(.+?)(?:\s+due|\s+tomorrow|\s+kal|\s+today|\s+duedate|$)',
            r'\s+-\s+(.+?)(?:\s+due|\s+tomorrow|\s+kal|\s+today|$)',
        ]
        
        for pattern in desc_patterns:
            match = re.search(pattern, original_message, re.IGNORECASE)
            if match:
                desc = match.group(1).strip()
                # Clean up description - remove due date references
                desc = re.sub(r'\s*due\s+.*$', '', desc, flags=re.IGNORECASE)
                desc = re.sub(r'\s*duedate\s*:.*$', '', desc, flags=re.IGNORECASE)
                if desc and len(desc) > 5:
                    return desc
        return None

    async def _execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute a tool"""
        try:
            # Convert user_id to string for MCP tools (they expect string)
            params['user_id'] = str(self.user_id)
            logger.info(f"Executing tool: {tool_name} with params: {params}")

            from mcp.tools import add_task, list_tasks, complete_task, delete_task, update_task, unmark_task, search_tasks, get_task_stats
            from mcp.server import AddTaskParams, ListTasksParams, CompleteTaskParams, DeleteTaskParams, UpdateTaskParams

            if tool_name == 'add_task':
                clean_params = {k: v for k, v in params.items() if v is not None}
                tool_params = AddTaskParams(**clean_params)
                result = await add_task(tool_params)
            elif tool_name == 'list_tasks':
                clean_params = {k: v for k, v in params.items() if v is not None}
                tool_params = ListTasksParams(**clean_params)
                result = await list_tasks(tool_params)
            elif tool_name == 'complete_task':
                clean_params = {k: v for k, v in params.items() if v is not None}
                tool_params = CompleteTaskParams(**clean_params)
                result = await complete_task(tool_params)
            elif tool_name == 'delete_task':
                clean_params = {k: v for k, v in params.items() if v is not None}
                tool_params = DeleteTaskParams(**clean_params)
                result = await delete_task(tool_params)
            elif tool_name == 'update_task':
                clean_params = {k: v for k, v in params.items() if v is not None}
                tool_params = UpdateTaskParams(**clean_params)
                result = await update_task(tool_params)
            elif tool_name == 'unmark_task':
                clean_params = {k: v for k, v in params.items() if v is not None}
                tool_params = CompleteTaskParams(**clean_params)
                result = await unmark_task(tool_params)
            elif tool_name == 'search_tasks':
                result = await search_tasks(params)
            elif tool_name == 'get_task_stats':
                clean_params = {k: v for k, v in params.items() if v is not None}
                result = await get_task_stats(clean_params)
            else:
                result = {"error": f"Unknown tool: {tool_name}"}

            return {"tool_name": tool_name, "result": result}

        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}", exc_info=True)
            return {"tool_name": tool_name, "result": {"error": str(e)}}

    def _format_tool_response(self, tool_result: Dict[str, Any]) -> str:
        """Format tool result into user-friendly response"""
        result = tool_result.get('result', {})
        tool_name = tool_result.get('tool_name', '')

        if tool_name == 'add_task':
            if result.get('success'):
                return f"[OK] Task added: {result.get('message', '')}"
            return f"[Error] {result.get('message', 'Unknown error')}"

        elif tool_name == 'list_tasks':
            tasks = result.get('tasks', [])
            count = result.get('count', 0)
            if count == 0:
                return "No tasks found!"

            response = f"📋 You have {count} task(s):\n\n"
            for task in tasks[:10]:  # Show max 10 tasks
                # Use professional format with ID, title, description, due date
                response += self._format_task_professional(task) + "\n\n"
            if count > 10:
                response += f"... and {count - 10} more task(s)"
            return response
        
        elif tool_name == 'complete_task':
            if result.get('success'):
                return f"[Done] {result.get('message', 'Task completed!')}"
            return f"[Error] {result.get('message', 'Error')}"
        
        elif tool_name == 'unmark_task':
            if result.get('success'):
                return f"[Reopened] {result.get('message', 'Task marked as incomplete!')}"
            return f"[Error] {result.get('message', 'Error')}"
        
        elif tool_name == 'delete_task':
            if result.get('success'):
                return f"[Deleted] {result.get('message', 'Task deleted!')}"
            return f"[Error] {result.get('message', 'Error')}"
        
        elif tool_name == 'get_task_stats':
            total = result.get('total_tasks', 0)
            completed = result.get('completed', 0)
            pending = result.get('pending', 0)
            rate = result.get('completion_rate', 0)
            return f"[Stats] {total} total, {completed} completed, {pending} pending ({rate}% completion rate)"
        
        elif tool_name == 'search_tasks':
            count = result.get('count', 0)
            if count == 0:
                return "No tasks found matching your search"
            return f"Found {count} task(s) matching your query"
        
        elif tool_name == 'update_task':
            if result.get('success'):
                return f"[Updated] {result.get('message', 'Task updated!')}"
            return f"[Error] {result.get('message', 'Error')}"
        
        return str(result)

    def _format_task_professional(self, task: Dict[str, Any]) -> str:
        """Format a single task in professional structure with ID, title, description, due date"""
        task_id = task.get('id', '?')
        title = task.get('title', 'No Title')
        description = task.get('description', '')
        status = task.get('status', 'pending')
        due_date_str = task.get('due_date')
        
        # Format status icon
        icon = "✅" if status == "completed" else "⏳"
        
        # Format due date in human-readable format
        due_date_display = ""
        if due_date_str:
            try:
                due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                now = datetime.utcnow()
                
                # Calculate days difference
                days_diff = (due_date.replace(tzinfo=None) - now).days
                
                if status == "completed":
                    due_date_display = f"Completed"
                elif days_diff < 0:
                    due_date_display = f"Overdue by {abs(days_diff)} day{'s' if abs(days_diff) > 1 else ''}"
                elif days_diff == 0:
                    due_date_display = "Due Today"
                elif days_diff == 1:
                    due_date_display = "Due Tomorrow"
                elif days_diff <= 7:
                    due_date_display = f"Due in {days_diff} day{'s' if days_diff > 1 else ''}"
                else:
                    weeks = days_diff // 7
                    due_date_display = f"Due in {weeks} week{'s' if weeks > 1 else ''}"
            except Exception:
                due_date_display = f"Due: {due_date_str[:10]}"
        
        # Build professional format
        lines = []
        lines.append(f"{icon} Task #{task_id}: {title}")
        
        if description and len(description) > 0:
            lines.append(f"   📝 {description}")
        
        if due_date_display:
            lines.append(f"   📅 {due_date_display}")
        
        return " | ".join(lines)

    def _get_fallback_response(self, message: str) -> str:
        """Simple rule-based conversational responses - Professional English only with user personalization"""

        # New Chat / Clear conversation
        if any(x in message for x in ['new chat', 'fresh chat', 'start over', 'clear chat', 'reset chat']):
            return f"Great idea {self.username}! I've cleared our conversation history. What would you like to work on today?"

        # Recent conversations / Show history - Just acknowledge, frontend will show actual history
        if any(x in message for x in ['recent conversations', 'chat history', 'previous chats', 'show history', 'recent chats', 'show recent conversation history']):
            return f"{self.username}, here's our conversation history. You can scroll up to see all our previous messages!"

        # Greetings (English + Roman Urdu) - Personalized with name
        if any(x in message for x in ['hello', 'hi', 'hey', 'assalam', 'salam', 'namaste']):
            return f"Hello {self.username}! I'm TodoMaster Pro, your intelligent task management assistant. I'm here to help you organize and manage your tasks efficiently. How can I assist you today?"

        # Help requests (English + Roman Urdu)
        elif any(x in message for x in ['help', 'what can you do', 'kya kar', 'kaise', 'help karo', 'madad']):
            return f"""{self.username}, I can help you manage your tasks effectively:

• Add tasks: "Add a task to buy groceries due tomorrow"
• List tasks: "Show my pending tasks" or "Show all tasks"
• Complete tasks: "Mark task 1 as complete"
• Unmark tasks: "Incomplete task 1" or "Reopen task 1"
• Update tasks: "Update task 1 title: New Title"
• Delete tasks: "Delete task 3"
• Search tasks: "Find tasks about meeting"
• Get stats: "Show my productivity stats"

What would you like to do?"""

        # Thanks (English + Roman Urdu)
        elif any(x in message for x in ['thank', 'thanks', 'shukriya', 'thank you', 'thanks yaar']):
            return f"You're welcome {self.username}! I'm always here to help you stay organized and productive. Is there anything else I can assist you with?"

        # Goodbye (English + Roman Urdu)
        elif any(x in message for x in ['bye', 'goodbye', 'see you', 'phir milenge', 'jata hoon', 'chalta hoon']):
            return f"Goodbye {self.username}! Feel free to come back anytime you need help with your tasks. Have a productive day!"

        # Who am I / identity - User asking about themselves
        elif any(x in message for x in ['who am i', 'who i am', 'what is my name', 'what is my email', 'tell me about me']):
            user_info = []
            if self.username and self.username != "User":
                user_info.append(f"Your name is {self.username}")
            if self.user_email and self.user_email != "unknown":
                user_info.append(f"your email is {self.user_email}")
            
            if user_info:
                return f"{self.username}, you are a valued TodoMaster user. " + ". ".join(user_info).capitalize() + ". I'm here to help you manage your tasks efficiently."
            else:
                return f"{self.username}, you are a valued TodoMaster user. I'm here to help you manage your tasks and boost your productivity. You can ask me to add, list, complete, or delete tasks."

        # Who are you - User asking about the assistant
        elif any(x in message for x in ['who are you', 'what are you', 'kaun ho', 'tum kaun', 'tell me about yourself']):
            return f"""{self.username}, I'm TodoMaster Pro - your intelligent task management assistant. I help you:
• Organize and track your daily tasks
• Set priorities and due dates
• Monitor your productivity with stats
• Search and manage your task list

I respond in English and can understand both English and Roman Urdu commands. How can I help you today?"""

        # Language request (Urdu) - Respond in English but acknowledge
        elif any(x in message for x in ['urdu', 'hindi', 'roman urdu', 'urdu mein', 'hindi mein', 'talk in urdu', 'speak urdu']):
            return f"{self.username}, I understand Roman Urdu commands! You can say things like 'Task add karo kal meeting ke liye' or 'Meri tasks dikhao'. However, I respond in English to ensure clarity. What would you like to do?"

        # Language request - English only
        elif any(x in message for x in ['talk in english', 'speak english', 'english only', 'respond in english']):
            return f"{self.username}, I communicate in English to ensure clarity and professionalism. I can understand both English and Roman Urdu commands. How can I assist you with your tasks today?"

        # Ask about capabilities
        elif any(x in message for x in ['what can you', 'what do you', 'can you', 'are you able']):
            return f"""{self.username}, I'm TodoMaster Pro, your intelligent task management assistant. I can:

✅ Add new tasks with titles, descriptions, priorities, and due dates
✅ List all your tasks or filter by status (pending/completed)
✅ Mark tasks as complete when you're done
✅ Unmark/Reopen tasks if needed
✅ Update task titles and descriptions
✅ Delete tasks you no longer need
✅ Search through your tasks to find specific items
✅ Provide productivity stats and summaries

Try saying: "Add a task to prepare for the meeting tomorrow" or "Show my pending tasks"."""

        # Default fallback - More informative and professional
        else:
            return f"""{self.username}, I'm TodoMaster Pro, your intelligent task management assistant. I'm here to help you organize and track your tasks.

You can ask me to:
• Add a task: "Add a task to prepare for meeting due tomorrow"
• Show your tasks: "Show my tasks" or "List pending tasks"
• Complete a task: "Complete task 1"
• Unmark a task: "Incomplete task 1"
• Update a task: "Update task 1 title: New Title"
• Delete a task: "Delete task 2"
• Get productivity stats: "Show my stats"
• Show conversation history: "Show recent conversations"
• Start fresh: "New chat"

What would you like to do today?"""


def create_todo_master_agent(user_id: str, user_email: Optional[str] = None, username: Optional[str] = None) -> TodoMasterAgent:
    """Factory function to create TodoMaster agent"""
    return TodoMasterAgent(user_id=user_id, user_email=user_email, username=username)
