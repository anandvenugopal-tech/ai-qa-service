
# import required libraries
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from retrieve import retrieve
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

# create groq client
client = Groq(api_key = os.getenv('GROQ_API_KEY'))

# creat FastAPI application object
app = FastAPI()

class Question(BaseModel):
    question: str

# home endpoint
@app.get("/")
def home():
    return {"message": "RAG API running"}

# main RAG endpoint  
@app.post('/ask')
def ask(data: Question):
    """Ask question, retrieve top related chunks 
    and get answer"""

    # retrieve chunks
    results = retrieve(data.question)
    
    context = "\n\n".join([chunk for score, chunk in results])
    
    # create prompt for llm
    prompt = f"""
Answer ONLY using context.

Context:
{context}

Question:
{data.question}

If the answer is not present,
say: I could not find that in document."""
    
    # send prompt to llm
    response = client.chat.completions.create(
        model = 'llama-3.3-70b-versatile',
        messages = [{
            'role': 'user',
            'content': prompt
        }]
    )

    # return API response
    return {
        'question': data.question,
        'answer': response.choices[0].message.content,
        'chunk_used': len(results)
    }