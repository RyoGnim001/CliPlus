from app.repository.pacientes_repository import buscar_por_cpf, criar_paciente
from app.repository.consultas_repository import criar_consulta

def registrar_consulta(dados: dict, usuario_id: int):
    # busca paciente pelo CPF
    paciente = buscar_por_cpf(dados["cpf"])

    # se não existir, cria
    if not paciente:
        paciente = criar_paciente({
            "cpf": dados["cpf"],
            "nome_completo": dados["nome_completo"],
            "data_nascimento": dados.get("data_nascimento"),
            "sexo": dados.get("sexo"),
            "telefone": dados.get("telefone"),
            "email": dados.get("email"),
            "endereco": dados.get("endereco"),
            "cidade": dados.get("cidade"),
            "estado": dados.get("estado"),
            "cep": dados.get("cep"),
            "convenio": dados.get("convenio"),
        })

    # registra a consulta vinculada ao paciente e ao operador
    consulta = criar_consulta({
        "paciente_id": paciente["id"],
        "usuario_id": usuario_id,
        "data_consulta": dados["data_consulta"],
        "especialidade": dados.get("especialidade"),
        "motivo": dados.get("motivo"),
        "status": dados.get("status", "agendada"),
        "observacoes": dados.get("observacoes"),
    })

    return {
        "consulta": consulta,
        "paciente": paciente
    }