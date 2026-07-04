from flask import jsonify
from apiflask import APIBlueprint
from app.services.pacientes_service import buscar_paciente_por_cpf
from app.helpers.auth import auth
from app.schemas.paciente_schema import PacienteSchema

bp = APIBlueprint("pacientes", __name__)

@bp.get("/pacientes/<string:cpf>")
@bp.auth_required(auth)
@bp.output(PacienteSchema)
def get_paciente_por_cpf(cpf):
    paciente = buscar_paciente_por_cpf(cpf)

    if not paciente:
        return jsonify({"erro": "Paciente não encontrado"}), 404

    return jsonify(paciente), 200