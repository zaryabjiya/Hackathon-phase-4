"""MCP Tool Implementations - Simplified (No FastMCP decorators)"""
from .server import AddTaskParams, ListTasksParams, CompleteTaskParams, DeleteTaskParams, UpdateTaskParams
from sqlmodel import select
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def add_task(params: AddTaskParams) -> dict:
    """Add a new task for the authenticated user"""
    from models.task import Task
    from db.session import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        try:
            # Parse due_date if provided
            due_date = None
            if params.due_date:
                try:
                    due_date = datetime.fromisoformat(params.due_date.replace('Z', '+00:00'))
                except:
                    pass

            # Convert user_id to int (database expects integer)
            user_id = int(params.user_id) if str(params.user_id).isdigit() else params.user_id

            task = Task(
                user_id=user_id,
                title=params.title,
                description=params.description,
                completed=False,
                due_date=due_date
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)

            logger.info(f"Task created: {task.id} for user {params.user_id}")

            msg = f"Task '{task.title}' has been added!"
            if due_date:
                msg += f" Due: {due_date.strftime('%b %d')}"

            return {
                "success": True,
                "task_id": task.id,
                "message": msg
            }
        except Exception as e:
            logger.error(f"Error creating task: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Task create karne mein error aaya: {str(e)}"
            }


async def list_tasks(params: ListTasksParams) -> dict:
    """List tasks for the authenticated user with optional status filter"""
    from models.task import Task
    from db.session import AsyncSessionLocal
    from datetime import datetime, timedelta

    async with AsyncSessionLocal() as session:
        try:
            # Convert user_id to int
            user_id = int(params.user_id) if str(params.user_id).isdigit() else params.user_id

            query = select(Task).where(Task.user_id == user_id)

            # Apply filters
            if params.status == "pending":
                query = query.where(Task.completed == False)
            elif params.status == "completed":
                query = query.where(Task.completed == True)
            elif params.status == "overdue":
                now = datetime.utcnow()
                query = query.where(
                    Task.due_date < now,
                    Task.completed == False
                )
            elif params.status == "today":
                today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                today_end = today_start + timedelta(days=1)
                query = query.where(
                    Task.due_date >= today_start,
                    Task.due_date < today_end
                )
            elif params.status == "this_week":
                today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                week_start = today - timedelta(days=today.weekday())
                week_end = week_start + timedelta(days=7)
                query = query.where(
                    Task.due_date >= week_start,
                    Task.due_date < week_end
                )

            result = await session.execute(query.order_by(Task.created_at.desc()))
            tasks = result.scalars().all()

            # Format tasks for display
            formatted_tasks = []
            for task in tasks:
                icon = "[x]" if task.completed else "[ ]"

                due = ""
                if task.due_date:
                    if task.due_date.date() == datetime.utcnow().date():
                        due = " (Today)"
                    elif task.due_date < datetime.utcnow():
                        due = f" (Overdue: {task.due_date.strftime('%b %d')})"
                    else:
                        due = f" (Due: {task.due_date.strftime('%b %d')})"

                formatted_tasks.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description or "",
                    "status": "completed" if task.completed else "pending",
                    "priority": "medium",
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "display": f"{icon} [{task.id}] {task.title}{due}"
                })

            return {
                "tasks": formatted_tasks,
                "count": len(formatted_tasks),
                "status": params.status or "all"
            }
        except Exception as e:
            logger.error(f"Error listing tasks: {e}")
            return {
                "tasks": [],
                "count": 0,
                "error": str(e)
            }


async def complete_task(params: CompleteTaskParams) -> dict:
    """Mark a task as completed"""
    from models.task import Task
    from db.session import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        try:
            # Convert user_id to int
            user_id = int(params.user_id) if str(params.user_id).isdigit() else params.user_id

            query = select(Task).where(
                Task.id == params.task_id,
                Task.user_id == user_id
            )
            result = await session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                return {
                    "success": False,
                    "message": "Task nahi mila... koi aur ID try karo?"
                }

            task.completed = True
            task.updated_at = datetime.utcnow()
            await session.commit()

            logger.info(f"Task completed: {task.id}")

            return {
                "success": True,
                "message": "Task complete mark kar diya! Well done!"
            }
        except Exception as e:
            logger.error(f"Error completing task: {e}")
            return {
                "success": False,
                "message": "Task complete karne mein error aaya."
            }


async def unmark_task(params: CompleteTaskParams) -> dict:
    """Mark a task as incomplete (unmark/reopen)"""
    from models.task import Task
    from db.session import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        try:
            # Convert user_id to int
            user_id = int(params.user_id) if str(params.user_id).isdigit() else params.user_id

            query = select(Task).where(
                Task.id == params.task_id,
                Task.user_id == user_id
            )
            result = await session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                return {
                    "success": False,
                    "message": "Task nahi mila... koi aur ID try karo?"
                }

            task.completed = False
            task.updated_at = datetime.utcnow()
            await session.commit()

            logger.info(f"Task unmarked: {task.id}")

            return {
                "success": True,
                "message": "Task ko incomplete mark kar diya! No worries!"
            }
        except Exception as e:
            logger.error(f"Error unmarking task: {e}")
            return {
                "success": False,
                "message": "Task incomplete karne mein error aaya."
            }


async def delete_task(params: DeleteTaskParams) -> dict:
    """Delete a task (requires confirmation in agent logic)"""
    from models.task import Task
    from db.session import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        try:
            # Convert user_id to int
            user_id = int(params.user_id) if str(params.user_id).isdigit() else params.user_id

            query = select(Task).where(
                Task.id == params.task_id,
                Task.user_id == user_id
            )
            result = await session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                return {
                    "success": False,
                    "message": "Task nahi mila... koi aur ID try karo?"
                }

            await session.delete(task)
            await session.commit()

            logger.info(f"Task deleted: {task.id}")

            return {
                "success": True,
                "message": "Task delete ho gaya!"
            }
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            return {
                "success": False,
                "message": "Task delete karne mein error aaya."
            }


async def update_task(params: UpdateTaskParams) -> dict:
    """Update task title, description, or due date"""
    from models.task import Task
    from db.session import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        try:
            # Convert user_id to int
            user_id = int(params.user_id) if str(params.user_id).isdigit() else params.user_id

            query = select(Task).where(
                Task.id == params.task_id,
                Task.user_id == user_id
            )
            result = await session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                return {
                    "success": False,
                    "message": "Task nahi mila... koi aur ID try karo?"
                }

            if params.title:
                task.title = params.title
            if params.description:
                task.description = params.description
            
            # Update due date if provided
            if params.due_date:
                try:
                    task.due_date = datetime.fromisoformat(params.due_date.replace('Z', '+00:00'))
                except Exception as e:
                    logger.warning(f"Invalid due date format: {params.due_date}, error: {e}")

            task.updated_at = datetime.utcnow()
            await session.commit()

            logger.info(f"Task updated: {task.id}")

            return {
                "success": True,
                "message": "Task update ho gaya!"
            }
        except Exception as e:
            logger.error(f"Error updating task: {e}")
            return {
                "success": False,
                "message": "Task update karne mein error aaya."
            }


async def search_tasks(params: dict) -> dict:
    """Search tasks by keyword in title or description"""
    from models.task import Task
    from db.session import AsyncSessionLocal
    from sqlalchemy import or_

    async with AsyncSessionLocal() as session:
        try:
            # Convert user_id to int
            user_id = int(params['user_id']) if str(params['user_id']).isdigit() else params['user_id']

            query = select(Task).where(
                Task.user_id == user_id,
                or_(
                    Task.title.ilike(f"%{params['query']}%"),
                    Task.description.ilike(f"%{params['query']}%")
                )
            )
            result = await session.execute(query)
            tasks = result.scalars().all()

            return {
                "tasks": [task.model_dump() for task in tasks],
                "count": len(tasks),
                "query": params['query']
            }
        except Exception as e:
            logger.error(f"Error searching tasks: {e}")
            return {
                "tasks": [],
                "count": 0,
                "error": str(e)
            }


async def get_task_stats(params: dict) -> dict:
    """Get task statistics and productivity summary"""
    from models.task import Task
    from db.session import AsyncSessionLocal
    from datetime import datetime, timedelta

    async with AsyncSessionLocal() as session:
        try:
            # Convert user_id to int
            user_id = int(params['user_id']) if str(params['user_id']).isdigit() else params['user_id']

            now = datetime.utcnow()

            # Base query for user's tasks
            base_query = select(Task).where(Task.user_id == user_id)

            # Get all tasks
            all_tasks_result = await session.execute(base_query)
            all_tasks = all_tasks_result.scalars().all()

            # Calculate stats
            total = len(all_tasks)
            completed = sum(1 for t in all_tasks if t.completed)
            pending = total - completed

            # Today's tasks
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            today_query = base_query.where(
                Task.created_at >= today_start,
                Task.created_at < today_end
            )
            today_result = await session.execute(today_query)
            today_count = len(list(today_result.scalars().all()))

            # This week's tasks
            week_start = today_start - timedelta(days=now.weekday())
            week_query = base_query.where(Task.created_at >= week_start)
            week_result = await session.execute(week_query)
            week_count = len(list(week_result.scalars().all()))

            return {
                "total_tasks": total,
                "completed": completed,
                "pending": pending,
                "completion_rate": round((completed / total * 100) if total > 0 else 0, 1),
                "today": today_count,
                "this_week": week_count,
                "period": params.get('period', 'all')
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                "error": str(e),
                "total_tasks": 0,
                "completed": 0,
                "pending": 0
            }
