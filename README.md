# 📄 AI PDF RAG Application

A production-ready document intelligence system that allows users to upload PDFs and ask questions using natural language. Built with FastAPI, pgvector, and Gemini AI.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)

## ✨ Features

- *📥 PDF Upload*: Multi-file upload with automatic text extraction
- *🧩 Smart Chunking*: Intelligent document chunking for optimal retrieval
- *🔍 Semantic Search*: Vector similarity search using pgvector
- * Natural Q&A*: Ask questions in plain English about your documents
- *🔐 User Authentication**: Secure JWT-based authentication
- *📊 Chat History**: Persistent conversation history per user
- *🐳 Dockerized**: One-command deployment with Docker Compose
- *🧪 Tested**: Full pytest coverage

## ️ Architecture

This project implements a *RAG (Retrieval-Augmented Generation)* pipeline:

## Porject Structure
```
ai-pdf-support/
├── ai/                          # AI Core Logic
│   ├── __init__.py
│   ├── ask_question.py          # Question handling & RAG logic
│   ├── brain.py                 # LLM & Embedding configuration
│   └── file_upload.py           # PDF processing & chunking
├── chat/                        # Chat History Management
│   ├── __init__.py
│   └── chat_history.py          # Get/delete conversation history
├── core/                        # Configuration & Security
│   ├── __init__.py             
│   ├── security.py              # JWT, password hashing
│   └── extensions.py            # Logging & middleware
├── db/                          # Database Layer
│   ├── __init__.py
│   ├── database.py              # Database connection & session
│   ├── models.py                # SQLAlchemy models
│   └── schemas.py               # Pydantic schemas
├── routers/                     # API Endpoints
│   ├── __init__.py
│   ├── auth.py                  # Register, login, auth routes
│   └── users.py                 # User CRUD operations
├── docker-compose.yml           # Docker orchestration
├── Dockerfile                   # Python 3.11 environment
├── init.sql                     # Database initialization
├── main.py                      # FastAPI app
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── .dockerignore                # Docker ignore rules
└── README.md                    # Project documentation
|-- test_security.py             #Testing of the security with pytest
```

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

* 🐳 **[Docker & Docker Compose]*(https://www.docker.com/products/docker-desktop/)*** - Required to run containers
*  **[Google Gemini API Key]*(https://aistudio.google.com/app/apikey)*** - For AI embeddings

### Installation

1. *Clone the repository:*
git clone https://github.com/sandip-magar/AI-PDF-RAG.git
cd AI-PDF-RAG

2. *Create environment file:*
cp .env.example .env
# Edit .env with your credentials

3. *Access the application:*
- Swagger UI: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 🛠️ Docker Management Commands

*Stop the containers (keeps data):*
```bash
docker-compose down
```

*Stop and reset database (deletes all data):*
```bash
docker-compose down -v
```

*View logs (debugging):*
```bash
docker-compose logs -f
```

*Rebuild after code changes:*
```bash
docker-compose up --build -d
```

## 🧪 Running Tests
```bash
#Run all tests
pytest

#Run with verbose output
pytest -v

#Run with coverage report
pytest --cov=app
```

## 📡 API Endpoints

### Authentication
- POST /auth/register - Create new user account
- POST /auth/login - Authenticate and receive JWT token
- POST /auth/logout - Logout current user

### Documents
- POST /documents/upload - Upload PDF file (multipart/form-data)
- GET /documents - List all user documents
- GET /documents/{doc_id} - Get specific document details
- DELETE /documents/{doc_id} - Delete document

### Chat & Q&A
- POST /chat/ask - Ask question about uploaded documents
- GET /chat/history - Get conversation history
- DELETE /chat/clear - Clear chat history

## 🔧 Environment Variables

Create a .env file in the root directory:
```bash
env
# Database Configuration
POSTGRES_USER=admin
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=ai_pdf_db
DATABASE_URL=postgresql://admin:your_secure_password@db:5432/ai_pdf_db

# Security
SECRET_KEY=your_32_character_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Configuration
GOOGLE_API_KEY=your_gemini_api_key_here
EMBEDDING_MODEL=gemini-embedding-001
LLM_MODEL=gemini-pro
EMBEDDING_DIMENSION=3072

# RAG Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
SIMILARITY_TOP_K=3

# Application
ENVIRONMENT=development
DEBUG=True
```

## 🧠 How It Works

### 1. Document Processing Pipeline
- *Upload*: User uploads PDF file via API
- *Extraction*: PyPDF2 extracts text from each page
- *Chunking*: Text split into overlapping chunks (1000 chars, 200 overlap)
- *Embedding*: Gemini embedding model converts chunks to 3072-dim vectors
- *Storage*: Vectors stored in PostgreSQL with pgvector extension

### 2. Question Answering Flow
- *Query*: User asks a question in natural language
- *Embedding*: Question converted to vector using same embedding model
- *Search*: Cosine similarity search finds top 3 relevant chunks
- *Context*: Retrieved chunks + question sent to LLM
- *Answer*: LLM generates answer based on retrieved context

## ️ Database Schema

### Tables:
- *users*: User accounts (id, email, hashed_password, created_at, is_active)
- *documents*: Uploaded PDFs (id, user_id, filename, file_path, uploaded_at, file_size)
- *document_chunks*: Vector embeddings (id, doc_id, page_number, content, embedding vector(3072))
- *chat_messages*: Conversation history (id, user_id, thread_id, role, content, created_at)

### Indexes:
- *HNSW index* on embedding column for O(log n) similarity search
- *B-tree indexes* on user_id, doc_id for relational queries

## 🔒 Security Features

- *Password Hashing*: bcrypt with salt rounds
- *JWT Tokens*: Secure authentication with expiration
- *Input Validation*: Pydantic schemas for all endpoints
- *CORS*: Configurable cross-origin resource sharing
- *SQL Injection Prevention*: SQLAlchemy ORM with parameterized queries
- *File Upload Validation*: PDF type checking and size limits (max 10MB)

## 🚀 Performance Optimization

1. *Vector Indexing*: HNSW (Hierarchical Navigable Small World) for fast similarity search
2. *Connection Pooling*: PostgreSQL connection pool via SQLAlchemy
3. *Async/Await*: Non-blocking I/O with FastAPI async endpoints
4. *Chunking Strategy*: Optimal chunk size (1000 chars) balances context vs. performance
5. *Batch Processing*: Multiple chunks embedded in single API call

##  Scaling Considerations

For production deployment with high traffic:

- *Horizontal Scaling*: Multiple FastAPI instances behind Nginx load balancer
- *Database*: PostgreSQL read replicas for query distribution
- *Vector Search*: Dedicated pgvector instance or Pinecone/Weaviate
- *Background Tasks*: Celery + Redis for async PDF processing
- *File Storage*: AWS S3 or cloud storage instead of local filesystem
- *Monitoring*: Prometheus + Grafana for metrics and alerting
- *Caching*: Redis for frequently asked questions

## 🐛 Troubleshooting

*Issue*: Docker container won't start  
*Solution*: Check .env file exists and has correct DATABASE_URL

*Issue*: "Connection refused" to database  
*Solution*: Ensure PostgreSQL container is healthy: docker-compose ps

*Issue*: Slow similarity search  
*Solution*: Verify HNSW index exists on embedding column

*Issue*: PDF upload fails  
*Solution*: Check file size (max 10MB) and ensure it's a valid PDF


## 👨‍💻 Author

*Sandip Magar*  
[GitHub]*(https://github.com/sandip-magar)*

---

*Built with ❤️ for efficient document intelligence*