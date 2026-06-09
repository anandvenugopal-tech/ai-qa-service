# import libraries
from pypdf import PdfReader
import re
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from database import conn, cursor

# read PDF file
reader = PdfReader('../data/tell_tale_heart.pdf')

# extract text page by page and store pages
pages = []
for page in reader.pages:
    extracted = page.extract_text()
    if extracted:
        pages.append(extracted)

# combine all pages into one document
text = "\n".join(pages)
text = re.sub(r"\s+"," ",text).strip() # remove extra spaces and line breaks

# split the text into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500, 
    chunk_overlap = 100,
    separators = ["\n\n", "\n", ". ", " ", ""]
    )
chunks = splitter.split_text(text)
chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 80]
print(f"chunks: {len(chunks)}")

#load embedding model and convert text into vectors
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks, normalize_embeddings = True, show_progress_bar = True)

# store chunk and embedding into PostgreSQL
for chunk, emb in zip(chunks, embeddings):

    cursor.execute("""INSERT INTO chunks(chunk_text, embedding) VALUES (%s,%s)""" ,(chunk, emb.tolist()))

# save changes and closs DB connection
conn.commit()
print(f"{len(chunks)} chunks stored")

cursor.close()
conn.close()