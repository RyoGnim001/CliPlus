from apiflask import APIFlask
from flask import Blueprint, jsonify
from app.helpers.auth import requer_auth
from app.database.supabase_client import supabase

bp = Blueprint("me", __name__)

@bp.get("/me")
@requer_auth
def get_me(auth_uid):
    operador = supabase.table("usuarios")\
        .select("id, email, nome, ativo")\
        .eq("auth_uid", auth_uid)\
        .single()\
        .execute()

    if not operador.data:
        return jsonify({"erro": "Operador não encontrado"}), 404

    return jsonify(operador.data), 200