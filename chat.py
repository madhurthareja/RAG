import numpy as np
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key or not gemini_api_key:
    raise ValueError("Supabase URL, Key, or Gemini API Key is missing!")

supabase_client: Client = create_client(url, key)
supabase_client: Client = create_client(url, key)

def generate_response(query_embedding: np.ndarray) -> str:
    """Finds the most relevant documents using vector search and generates a response."""
    query_embedding = np.array(query_embedding, dtype=np.float32).tolist()  # Convert NumPy array to list

    try:
        # Use pgvector nearest neighbor search (Supabase supports <-> for cosine distance)
        stored_docs = (
            supabase_client.rpc("match_documents", {"query_embedding": query_embedding, "match_count": 3})
            .execute()
        )

        if not stored_docs.data:
            return "No relevant documents found."

    except Exception as e:
        print("Error retrieving documents:", e)
        return "Error fetching documents."

    # Extract document contents
    top_docs = [doc["content"] for doc in stored_docs.data]
    combined_docs = "\n\n".join(top_docs)

    return gemini_generate_response(combined_docs)

def gemini_generate_response(combined_docs: str) -> str:
    """Generates a response using the Gemini model from Google Generative AI."""
    prompt = f"Based on the following documents, generate a comprehensive response:\n\n{combined_docs}\n\nAnswer:"

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Error in Gemini response:", e)
        return "Sorry, I couldn't generate a response."
