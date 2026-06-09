# 📚 Tell-Tale Heart RAG API

A simple Retrieval-Augmented Generation (RAG) system built using FastAPI, PostgreSQL, Sentence Transformers, and Groq.

This project reads a PDF document, creates text chunks, generates embeddings, retrieves relevant chunks using cosine similarity, and generates answers using an LLM.

---

## Features

* PDF ingestion
* Recursive text chunking
* Embedding generation
* PostgreSQL storage
* Cosine similarity retrieval
* FastAPI REST API
* Groq integration

---

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* Sentence Transformers
* Groq
* Render
* Hugging Face

---

## Installation

Clone repository:

```bash
git clone https://github.com/anandvenugopal-tech/ai-qa-service
cd PROJECT_NAME
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run Ingestion

```bash
python ingest.py
```

---

## Run API

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Example Request

POST `/ask`

```json
{
  "question": "Why did the narrator kill the old man?"
}
```

Example Response:

```json
{
  "answer": "The narrator killed the old man because he was disturbed by the old man's eye."
}
```

---

## Project Structure

```text
app/
├── main.py
├── retrieve.py
├── ingest.py
├── database.py

data/
└── tell_tale_heart.pdf

requirements.txt
README.md
```
