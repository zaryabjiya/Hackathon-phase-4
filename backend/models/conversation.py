"""Conversation and Message SQLModel classes for chat history"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from sqlalchemy import JSON, Column


class Conversation(SQLModel, table=True):
    """Chat session between user and TodoMaster AI"""
    __tablename__ = "conversations"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(nullable=False, index=True)  # Removed foreign_key for SQLite compatibility
    title: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    messages: list["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """Individual message within a conversation"""
    __tablename__ = "messages"
    
    id: int = Field(primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", nullable=False, index=True)
    role: str = Field(nullable=False)  # "user" or "assistant"
    content: str = Field(nullable=False)
    tool_calls: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON)
    )  # JSON for tool call data
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    conversation: Conversation = Relationship(back_populates="messages")
