# AI PDF SUPPORT 

**AI PDF SUPPORT** is an intelligent, fully containerized document processing API. It allows users to securely register, upload PDF documents, and ask complex questions about their content using advanced AI. 

By leveraging **Retrieval-Augmented Generation(RAG)** and **Vector Database**, the application understand the semantic meaning of your documents, providing highly accurate, contet-aware answers.

--

## Features

- **Secure Authentication**: JWT-based user registration and login.
- **PDF Processing**: Automatic text extraction and chunking from ploaded PDF files. 
- **AI-Powered Q&A**: Ask questions about your documents and get accurate answers powered by Google Gemini.
- **Semantic Search**: Uses 'pgvector' to find the most relevant document sections based on meaning, not just keywords.
- **Fully Dockerized**: One-command setup for both the API and the Vector Database.

--

## Tech Stack

- **Backend Framework**: Python, FastAPI
- **Database**: PostgreSQL 16
- **Vector Extension**: pgvector (for AI Embeddings)
- **Containerization**: Docker & Docker Compose 
- **AI Models**: Google Gemini (LLM) & Text Embedding (Vectorization)

--

## Prerequisites 

Before you begin, ensure you have the following installed on your machine: 
-[Docker Desktop](https://www.docker.com/products/docker-desktop/)(Required to run the app)
-[Git](https://git-scm.com/) (To clone the repository)

--

## Installation & Setup 

Follow these steps to get the application running on your local machine in minutes.

### 1. Clone the repository 
Open your terminal or PowerShell and run: 
```bash
git clone https://github.com/sandip-magar/ai-pdf-support.git
cd ai_pdf_db
```

### 2. Configure Environment Variables
The application requires a '.env' file to manage secrets and configuration.

**Step A: Generate a Secure Secret Key**
First, you need to generate a secure random string for your JWT authentication. Run this command in your terminal.
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

*Copy the long string that gets printed out.*

**Step B: Create the '.env' File**
Create a new file named exactly '.env' in the root directory of the project and paste the following configuration.

```env
# Database Configuration (Do not changethe host 'db', it connets to the Docker container)
DATABASE_URL=postgresql://admin:securepassword123@db:5432/ai_pdf_db

# AI Configuration
GOOGLE_API_KEY=Your_actual_google_api_key_here
LLM_MODEL_NAME=gemini-3.5-flash-lite
EMBEDDING_MODEL_NAME=gemini-embedding-001

#Security Configuration 
SECRET_KEY=paste_the_generated_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTE=1440
```

*(Make sure to replace 'your_actual_google_api_key_here' with your real Google AI Studio API key, and paste your generated key into 'SECRET_KEY'.)

### 3. Access the API 
Once the container are running, open your web browser and navigate to the interactive Swagger UI documentation.

**http://localhost:8000/docs**

Here you can test all the endpoints, register a user, login, upload PDFs, and ask questions!

--

## Managing the application 

**Stop the application (keeps your database data safe).**
```bash
docker-compose down 
```

**Restart the appliation**
```bash
docker-compose up -d
```

**Wipe everything (Deletes the database and starts fresh).**
*Warning: This will permanently delete all users and uploaded PDFs.*
```bash
docker-compose down -v
```

--

## Project Structure

ai-pdf-support/
├── core/               # Database connection and security configs
├── models/             # SQLAlchemy database models (Users, PDFs)
├── routers/            # FastAPI API endpoints (Auth, PDF, Chat)
├── services/           # Business logic (AI processing, PDF parsing)
├── docker-compose.yml  # Docker orchestration file
├── Dockerfile          # Python environment build instructions
├── init.sql            # Initializes pgvector extension on DB startup
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (DO NOT COMMIT TO GITHUB)
├── .env.example        # Template for environment variables
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
