import os
import numpy as np
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Supabase URL or Key is missing!")

supabase_client: Client = create_client(url, key)

def store_document(file_name, text, embedding):
    """Stores document text and embedding in Supabase."""
    # Remove null characters from the text
    clean_text = text.replace("\x00", "").replace("\u0000", "")

    # Convert numpy array to list of floats
    if isinstance(embedding, np.ndarray):
        embedding = embedding.astype(np.float32).tolist()

    print(f"Storing document: {file_name}")
    print(f"Text: {clean_text[:100]}...")  # Print first 100 characters of the text
    print(f"Embedding: {embedding[:10]}...")  # Print first 10 elements of the embedding

    try:
        response = supabase_client.table("documents").insert({
            "file_name": file_name,
            "content": clean_text,  # Store cleaned text
            "embedding": embedding  # Ensure it's a list of floats
        }).execute()
        print("Document stored successfully.")
        print(response)  # Print the response from Supabase
        return response
    except Exception as e:
        print("Error storing document:", e)
        return None
