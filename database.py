import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

# We allow the app to run even if credentials are empty to prevent breaking the flow
supabase: Client = None
if url and key:
    try:
        supabase = create_client(url, key)
    except Exception as e:
        print(f"Supabase init error: {e}")

def save_chat_analysis(input_type: str, user_input: str, key_findings: str, summary: str, next_steps: str):
    if not supabase: return False
    try:
        supabase.table("chat_history").insert({
            "input_type": input_type,
            "user_input": user_input,
            "key_findings": key_findings,
            "summary": summary,
            "next_steps": next_steps
        }).execute()
        return True
    except Exception as e:
        print(f"Error saving to database: {e}")
        return False

def get_chat_history(limit: int = 10):
    if not supabase: return []
    try:
        response = supabase.table("chat_history").select("*").order("created_at", desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching from database: {e}")
        return []
