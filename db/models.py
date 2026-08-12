from db.database import Base, engine
from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(355), nullable=False)
    is_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=func.now())

    #connect to the pdfdocument table and the chatmessages 
    messages = relationship('ChatMessage', back_populates='users', cascade="all, delete-orphan") 
    documents = relationship('PDFDocument', back_populates='users', cascade="all, delete-orphan")

class PDFDocument(Base):
    __tablename__ = "pdf-files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    uploaded_at = Column(DateTime, default=func.now())

    file_path = Column(String, nullable=True)

    content = Column(Text, nullable=False)
    embedding = Column(Vector(3072))

    #connect to the user table 
    users = relationship("User", back_populates='documents')

class ChatMessage(Base):
    __tablename__ = "chatmessages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    #connect to the user table 
    users = relationship('User', back_populates='messages')

Base.metadata.create_all(bind=engine)