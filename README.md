# 🤖 AI PDF Support system

A full-stack AI-powered chatbot that answers questions from uploaded PDF documents using RAG (Retrievel-Augmented Generation). Build with FASTAPI, Streamlit, and postgreSQL with pgvector.

## ✨ Features

-🔏 **User Authentication** -JWT-based user registration and login.
-📄 **PDF Uploaded & Processing** - Upload PDF's and automatically extract/embed text, and chunk it for the AI.
-🧠**Semantic Search** - Uses pgvector to store and retrieve document embeddings for accurate answers.
-**Interactive Chat** - Clean Streamlit interface to chat with your uploaded documents.
-📊 **Chat History** - Persists user conversations in a PostgreSQL database.

## Tech Stack 

**Backend**
-FastAPI (High-Performance Python API)
-LangChain(LLM orchestration and RAG pipeline)
-PostgreSQL + pgvector (Vector Database for embeddings)
-Google Gemini API(LLM and Embeddings)
-SQLAlchemy (ORM)

**Frontend.**
-Streamlit(Interactive Web UI)

## 🗄️Prerequisites

-Python 3.10+
-PostgreSQL 16+ (with 'pgvector' extension enabled)
-A Google Gemini API Key

## Installation & Setup

1. **Clone the repository.**
```bash
   git clone https://github.com/sandipagar/ai-pdf-support.git
   cd ai-pdf-support
```

2. **Create and activate a virtual environment.**
```bash
   python -m venv venv
   #Windows:
   venv/scripts/activate
   #Mac/Linux
   source venv/bin/activate
```

3. **Install dependencies.**
```bash
   pip install -r requirements.txt
```

4. **Configure Environment Variables.**
   Create a '.env' file in the root directory and add your credentials:
```env
   GOOGLE_API_KEY = your_google_api_key_key_here
   LLM_MODEL_NAME = gemini-3.5-flash-lite
   EMBEDDING_MODEL_NAME = gemini-embedding-001
   DATABASE_URL = postgresql://postgre:Your_Password@localhost:5432/ai_pdf_db
   SECRET_KEY = your_super_secret_jwt_key
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

5. **Enable pgvector in your database.**
   Open your PostgreSQL query tool and run:
```sql
   CREATE EXTENSION IF NOT EXISTS vector;
```

6. **Run the backend.**
```bash
   uvicorn main:app -reload --port 8000
```
   
   *(You can view the interactive API docs at 'http://localhost:8000/docs')*

7. **Run the Frontend.**
```bash
   stremlit run app.py
```

## 📂 Project Structure

```text
ai-pdf-support/
core/                   #Security, JWT, and config
db/                     #SQLAlchemy models and database connection 
routers/                #API endpoint (Auth, AI, Chat)
app.py/                 #Streamlit frontend
main.py/                #FastAPI backend entry point
requirements.txt/       #Python dependencies
```

## API Endpoints

-'POST /api/auth/register' -Register a new user
-'POST /api/auth/login' - Authenticate and receive a JWT token
-'POST /api/ai/upload-pdf' - Upload and proecess a PDF file
-'POST /api/ai/ask-ai' - Send a question to the RAG pipeline
-'DELETE /api/ai/chat-history - Clear the user's chat history 

## Author
**Sandip Agar**
-GitHub: [@sandip-magar](https://github.com/sandip-magar)

--
*Built with ❤️ using FastAPI, LangChain, and Streamlit*