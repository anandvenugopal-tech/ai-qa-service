# import required libraries
from sentence_transformers import SentenceTransformer
from database import conn
from sklearn.metrics.pairwise import cosine_similarity
import re

# load embedding model
model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")

# create retrieve function
def retrieve(query, top_k = 3):
    """This functionn returns retrieve Top 3 chunks
    from the PostgreSQL database."""

    # embed the query
    query_embedding = model.encode([query], normalize_embeddings = True)

    # connect database
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
        chunk_text,
        embedding

        FROM chunks
        """
    )

    # fetch data
    rows = cursor.fetchall()
    results = []


    for chunk, emb in rows:

        score = cosine_similarity(query_embedding, [emb])[0][0]

        results.append((score, chunk))

    results.sort(reverse = True)

    # return top 3 chunks
    return results[:top_k]