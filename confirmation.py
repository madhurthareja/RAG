import os
import supabase
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.getenv("SUPAVEC_URL")
supabase_key = os.getenv("SUPAVEC_API_KEY")
supabase_client = supabase.create_client(supabase_url, supabase_key)

print("Connected to Supavec (Supabase)!")
