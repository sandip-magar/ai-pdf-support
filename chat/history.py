from db.database import get_db
from db.models import User, PDFDocument, ChatMessage
from fastapi import APIRouter, HTTPException, status, Depends 
from sqlalchemy.orm import Session
from routers.auth import get_current_user
from sqlalchemy import desc

router = APIRouter()

@router.get("/")
async def get_user_history(
    limit: int = 10, 
    skip: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).order_by(desc(ChatMessage.created_at)).offset(skip).limit(limit).all()

    return messages

@router.delete("/delete-chat")
async def delete_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    messages = db.query(ChatMessage).filter(ChatMessage.user_id == current_user.id).delete(synchronize_session=False)

    db.commit()

    return {
        "messages": "Chat history cleared successfully",
        "deleted_messages": messages
    }