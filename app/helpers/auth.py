from functools import wraps
from flask import request, jsonify
from app.database.supabase_client import supabase

def requer_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"erro": "Token não fornecido"}), 401

        token = auth_header.split(" ")[1]

        try:
            user = supabase.auth.get_user(token)
        except Exception:
            return jsonify({"erro": "Token inválido ou expirado"}), 401

        kwargs["auth_uid"] = user.user.id
        return f(*args, **kwargs)

    return decorated