from flask import jsonify
from apiflask import APIBlueprint
from app.services.consultas_service import registrar_consulta
from app.services.comprovante_service import gerar_pdf
from app.services.email_service import enviar_comprovante
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
        .select("id, nome")\
        .eq("auth_uid", str(user.id))\
        .single()\
        .execute()

    if not operador.data:
        return jsonify({"erro": "Operador não encontrado"}), 404

    resultado = registrar_consulta(dados, operador.data["id"])

    email_paciente = resultado["paciente"].get("email")
    if email_paciente:
        try:
            pdf = gerar_pdf(resultado["paciente"], resultado["consulta"], operador.data)
            enviar_comprovante(
                destinatario=email_paciente,
                nome_paciente=resultado["paciente"]["nome_completo"],
                pdf_bytes=pdf,
                consulta_id=resultado["consulta"]["id"]
            )
        except Exception as e:
            print(f"Erro ao enviar email: {e}")

    return jsonify(resultado), 201