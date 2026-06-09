# import libraries
from retrieve import retrieve
from groq import Groq
from dotenv import load_dotenv
import os

#load environment variables and connect api
load_dotenv()
client = Groq(api_key = os.getenv('GROQ_API_KEY'))

#ask question and retrieve top 3 chunks
question = ("Why did the narrator kill the old man?")
results = retrieve(question)

# create context
context = "\n\n".join([chunk for score, chunk in results])


prompt = f"""
Answer ONLY using the context.

Context:
{context}

Question:
{question}

If answer not found,
say:
I could not find that in the document.
"""

# send prompt to llm and get response
response = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    messages = [{
        'role': 'user',
        'content': prompt
    }]
)
print("\nANSWER:\n")
print(response.choices[0].message.content)

