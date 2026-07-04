from flask import send_file, jsonify
from apiflask import APIBlueprint
from app.helpers.auth import auth
from app.database.supabase_client import supabase
from app.services.comprovante_service import gerar_pdf
import io

bp = APIBlueprint("comprovante", __name__)

@bp.get("/consultas/<int:consulta_id>/comprovante")
@bp.auth_required(auth)
def get_comprovante(consulta_id):
    # busca consulta
    consulta = supabase.table("consultas")\
        .select("*")\
        .eq("id", consulta_id)\
        .single()\
        .execute()

    if not consulta.data:
        return jsonify({"erro": "Consulta não encontrada"}), 404

    # busca paciente
    paciente = supabase.table("pacientes")\
        .select("*")\
        .eq("id", consulta.data["paciente_id"])\
        .single()\
        .execute()

    # busca operador
    usuario = supabase.table("usuarios")\
        .select("nome")\
        .eq("id", consulta.data["usuario_id"])\
        .single()\
        .execute()

    pdf = gerar_pdf(paciente.data, consulta.data, usuario.data)

    return send_file(
        io.BytesIO(pdf),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"comprovante_{consulta_id}.pdf"
    )