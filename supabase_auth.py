import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

#authenticates client
supabase: Client = create_client(supabase_url=url, supabase_key=key)

#test retrieval of database
test_response = supabase.table("Test").select("*").execute()
for row in test_response.data:
    print(f"Name: {row['name']}")