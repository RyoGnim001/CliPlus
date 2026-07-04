from flask import jsonify
from apiflask import APIBlueprint
from app.services.consultas_service import registrar_consulta
from app.helpers.auth import auth
from app.database.supabase_client import supabase
from app.schemas.consulta_schema import ConsultaSchema

bp = APIBlueprint("consultas", __name__)

@bp.post("/consultas")
@bp.auth_required(auth)
@bp.input(ConsultaSchema, arg_name="dados")
def post_consulta(dados):
    user = auth.current_user

    operador = supabase.table("usuarios")\
        .select("id")\
        .eq("auth_uid", str(user.id))\
        .single()\
        .execute()

    if not operador.data:
        return jsonify({"erro": "Operador não encontrado"}), 404

    resultado = registrar_consulta(dados, operador.data["id"])
    return jsonify(resultado), 201