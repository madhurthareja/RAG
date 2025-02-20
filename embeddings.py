from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str):
    """Generates an embedding for the given text."""
    return model.encode(text)
