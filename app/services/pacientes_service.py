from app.repository.pacientes_repository import buscar_por_cpf

def buscar_paciente_por_cpf(cpf: str):
    paciente = buscar_por_cpf(cpf)
    return paciente