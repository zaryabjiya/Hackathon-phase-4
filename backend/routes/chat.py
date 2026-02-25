"""Chat endpoint for TodoMaster AI with Google Gemini - FREE with Tool Calling"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

from middleware.auth import get_current_user, TokenData
from db.session import get_async_db
from models.conversation import Conversation, Message
from agents.google_agent import TodoMasterAgent
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select as async_select

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tool_calls: Optional[List[Dict[str, Any]]] = None


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: int,
    request: ChatRequest,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Chat with TodoMaster AI to manage tasks via natural language

    - **user_id**: User ID from JWT token (must match authenticated user)
    - **message**: User's natural language message
    - **conversation_id**: Optional existing conversation ID

    Returns AI response with conversation ID for continuing the conversation.
    """
    # Security: Verify user_id matches JWT subject (both are integers)
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID mismatch - unauthorized access"
        )

    # Convert user_id to string for database operations (PostgreSQL expects VARCHAR)
    user_id_str = str(user_id)

    try:
        # Load or create conversation
        if request.conversation_id:
            result = await db.execute(
                async_select(Conversation).where(
                    Conversation.id == request.conversation_id,
                    Conversation.user_id == user_id_str
                )
            )
            conversation = result.scalar_one_or_none()

            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = Conversation(user_id=user_id_str, title="New Chat")
            db.add(conversation)
            await db.commit()
            await db.refresh(conversation)
        
        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        db.add(user_message)
        await db.commit()
        
        # Load conversation history (last 20 messages)
        history_query = async_select(Message).where(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at.desc()).limit(20)
        
        result = await db.execute(history_query)
        history = result.scalars().all()
        
        # Convert to OpenAI chat_history format (chronological order)
        chat_history = []
        for msg in reversed(history):
            chat_history.append({
                "role": "user" if msg.role == "user" else "assistant",
                "content": msg.content
            })
        
        # Create TodoMaster agent with OpenAI
        agent = TodoMasterAgent(
            user_id=user_id,  # Keep as string
            user_email=current_user.email,
            username=current_user.username
        )
        
        logger.info(f"Calling agent chat with message: {request.message[:50]}...")

        # Call agent with tools (async call)
        response_data = await agent.chat(
            message=request.message,
            conversation_history=chat_history if chat_history else None
        )

        logger.info(f"Agent response: text={response_data.get('text', 'EMPTY')[:100]}..., tool_results={response_data.get('tool_results', [])}")

        # Ensure we have a valid response
        response_text = response_data.get("text", "Sorry, kuch error ho gaya 😅")
        if not response_text or response_text.strip() == "":
            response_text = "I'm here to help! Try saying 'Add a task' or 'Show my tasks'"
            logger.warning("Empty response from agent, using fallback")

        # Save assistant response
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=response_text,
            tool_calls={
                "calls": [
                    {"tool_name": tr["tool_name"], "result": tr["result"]}
                    for tr in response_data.get("tool_results", [])
                ]
            } if response_data.get("tool_results") else None
        )
        db.add(assistant_message)
        await db.commit()

        # Format tool calls for response
        tool_results = []
        if response_data.get("tool_results"):
            for tr in response_data["tool_results"]:
                tool_results.append({
                    "tool_name": tr.get("tool_name"),
                    "result": tr.get("result")
                })

        return ChatResponse(
            response=response_text,
            conversation_id=conversation.id,
            tool_calls=tool_results if tool_results else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat error: {str(e)}"
        )


@router.get("/{user_id}/conversations", response_model=List[Dict[str, Any]])
async def get_conversations(
    user_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all conversations for the authenticated user"""
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID mismatch - unauthorized access"
        )

    # Convert user_id to string for database operations
    user_id_str = str(user_id)

    result = await db.execute(
        async_select(Conversation).where(
            Conversation.user_id == user_id_str
        ).order_by(Conversation.updated_at.desc())
    )
    conversations = result.scalars().all()

    return [
        {
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at
        }
        for conv in conversations
    ]


@router.get("/{user_id}/conversations/{conversation_id}", response_model=Dict[str, Any])
async def get_conversation(
    user_id: int,
    conversation_id: str,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific conversation with its messages"""
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID mismatch - unauthorized access"
        )

    # Convert user_id to string for database operations
    user_id_str = str(user_id)

    result = await db.execute(
        async_select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id_str
        )
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    result = await db.execute(
        async_select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())
    )
    messages = result.scalars().all()

    return {
        "id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }
