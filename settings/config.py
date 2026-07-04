import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

MAIL_EMAIL  = os.getenv("MAIL_EMAIL")
MAIL_SENHA  = os.getenv("MAIL_SENHA")