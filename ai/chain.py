from fastapi import APIRouter, status, Depends, UploadFile, File, HTTPException
from ai.brain import rag_chain, retriever, vectorstore, MAX_FILE_SIZE, format_docs, llm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from routers.auth import get_current_user
from db.database import get_db
import tempfile , asyncio, os
from db.schemas import UserQuestion
from db.models import User, PDFDocument, ChatMessage
from sqlalchemy.orm import Session
from datetime import datetime 
from sqlalchemy.sql import func
import pdfplumber

router = APIRouter()

@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    #validate the file name 
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="File must be a PDF.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #read the file 
    content = await file.read()

    #check the file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"File is too large! maximum size is {MAX_FILE_SIZE // (1024*1024)} MB.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #Use tempfile(auto save and cleanup)
    with tempfile.NamedTemporaryFile(delete=False, prefix=".pdf") as temp_file:
        temp_file_path = temp_file.name
        temp_file.write(content)

    #now uploading the pdf
    try:
        loader = await asyncio.to_thread(PyPDFLoader, temp_file_path)
        doc = loader.load()

        #split the doc into chunks 
        splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
        docs_split = await asyncio.to_thread(splitter.split_documents, doc)

        #Add some metadata
        for doc in docs_split:
            doc.metadata['source'] = file.filename
            doc.metadata['category'] = "my_pdf_docs"
            #this is for the multiuser support
            doc.metadata['user_id'] = current_user.id

        #Get the text from the chunks 
        full_text = " ".join([doc.page_content for doc in docs_split])

        new_document = PDFDocument(
                user_id = current_user.id,
                filename = file.filename,
                file_path = temp_file_path,
                content = full_text,
                uploaded_at = func.now()
            )

        db.add(new_document)
        db.commit()

        print(f" SUCCCESS: Saved documents to DB with ID: {new_document.id}")

        #save to the vectorstore 
        await asyncio.to_thread(vectorstore.add_documents, docs_split)

        return {
            "message": f" PDF File '{file.filename}' Processed successfull!",
            "chunk_processed": len(docs_split)
        }
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error":str(e)}
        )

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

@router.delete("/delete-pdf/{document_id}")
async def delete_pdf(
    document_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    #check for the existance of the documents
    document = db.query(PDFDocument).filter(
        PDFDocument.id == document_id,
        PDFDocument.user_id == current_user.id #delete only one specific person file 
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document Not Found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    #delete the file from the disk 
    import os 
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    #Delete the database 
    db.delete(document)
    db.commit()

    return {
        "messages": " PDF File deleted successfully !"
    }