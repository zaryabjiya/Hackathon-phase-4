"""MCP Server for Todo Chatbot Tools - Simplified (No FastMCP dependency)"""
from pydantic import BaseModel, Field
from typing import Optional, Literal


# Tool parameter schemas (used by the agent)
class AddTaskParams(BaseModel):
    user_id: str = Field(..., description="Authenticated user ID")
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    due_date: Optional[str] = Field(None, description="Due date in ISO format")
    priority: Optional[Literal["low", "medium", "high", "urgent"]] = Field("medium", description="Priority level")


class ListTasksParams(BaseModel):
    user_id: str = Field(..., description="Authenticated user ID")
    status: Optional[Literal["all", "pending", "completed", "high_priority", "overdue", "today", "this_week"]] = Field("all", description="Filter status")


class CompleteTaskParams(BaseModel):
    user_id: str = Field(..., description="Authenticated user ID")
    task_id: int = Field(..., description="Task ID to complete")


class DeleteTaskParams(BaseModel):
    user_id: str = Field(..., description="Authenticated user ID")
    task_id: int = Field(..., description="Task ID to delete")


class UpdateTaskParams(BaseModel):
    user_id: str = Field(..., description="Authenticated user ID")
    task_id: int = Field(..., description="Task ID to update")
    title: Optional[str] = Field(None, max_length=200, description="New title")
    description: Optional[str] = Field(None, max_length=1000, description="New description")
    priority: Optional[Literal["low", "medium", "high", "urgent"]] = Field(None, description="New priority")
    due_date: Optional[str] = Field(None, description="New due date in ISO format")
