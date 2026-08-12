from langchain_postgres import PGVector
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import os 
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

#set up the .env imports
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = "my_pdf_docs"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")

#upload the pdf size 
MAX_FILE_SIZE = 10* 1024*1024 #this is in MB

#set up the embeddings
embedding = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL_NAME)

#set up the vectorstore 
vectorstore = PGVector(
    collection_name=COLLECTION_NAME,
    embeddings=embedding,
    connection= DATABASE_URL
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
llm = ChatGoogleGenerativeAI(model=LLM_MODEL_NAME, temperature=0.7, google_api_key= GOOGLE_API_KEY)

prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assitant. Answer the question ONLY on the provided context of PDF documents.
If the answer is not related to the PDF documents. say SORRY! I can't help with that question.
Keep answers concise but informative.

Context: {context}

Question: {question}

Answer:""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": itemgetter("question") | retriever | format_docs, "question": itemgetter("question")}
    |prompt
    |llm
    |StrOutputParser()
)