from flask import g
from apiflask.security import HTTPTokenAuth
from app.database.supabase_client import supabase

auth = HTTPTokenAuth(scheme="Bearer")

@auth.verify_token
def verify_token(token):
    try:
        response = supabase.auth.get_user(token)
        if response is None or response.user is None:
            return None
        g.current_user = response.user  # <-- adiciona isso
        return response.user
    except Exception:
        return None

def get_auth_uid():
    return g.get("current_user")