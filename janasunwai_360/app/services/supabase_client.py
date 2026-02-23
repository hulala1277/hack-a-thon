import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client


BASE_dir = Path(__file__).resolve().parent.parent.parent

env_path = BASE_dir / '.env'

load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")    

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

