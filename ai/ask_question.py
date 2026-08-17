from fastapi import APIRouter, HTTPException, status, Depends, Request
from db.models import User, ChatMessage
from db.schemas import UserQuestion
from db.database import get_db
from routers.auth import get_current_user
from ai.brain import rag_chain
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/ask-ai")
async def ask_question(
    request : UserQuestion,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 

    if not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try: 
        #pass the question to the llm 
        answer =rag_chain.invoke({"question": request.question})

        #save the entire chat to the database
        chat_message = ChatMessage(
            user_id = current_user.id,
            question = request.question,
            answer = answer,
        )
        db.add(chat_message)
        db.commit()
        db.refresh(chat_message)

        return {
            "question": request.question,
            "answer": answer,
            "message_id": chat_message.id
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f" AI Processed Failed: {str(e)}"
        )
