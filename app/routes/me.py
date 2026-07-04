from flask import jsonify
from apiflask import APIBlueprint
from app.helpers.auth import auth
from app.database.supabase_client import supabase

bp = APIBlueprint("me", __name__)

@bp.get("/me")
@bp.auth_required(auth)
def get_me():
    user = auth.current_user

    operador = supabase.table("usuarios")\
        .select("id, email, nome, ativo")\
        .eq("auth_uid", str(user.id))\
        .single()\
        .execute()

    if not operador.data:
        return jsonify({"erro": "Operador não encontrado"}), 404

    return jsonify(operador.data), 200