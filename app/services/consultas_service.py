from app.repository.pacientes_repository import buscar_por_cpf, criar_paciente
from app.repository.consultas_repository import criar_consulta

def registrar_consulta(dados: dict, usuario_id: int):
    paciente = buscar_por_cpf(dados["cpf"])

    if not paciente:
        data_nasc = dados.get("data_nascimento")
        paciente = criar_paciente({
            "cpf":              dados["cpf"],
            "nome_completo":    dados["nome_completo"],
            "data_nascimento":  str(data_nasc) if data_nasc else None,
            "sexo":             dados.get("sexo"),
            "telefone":         dados.get("telefone"),
            "email":            dados.get("email"),
            "endereco":         dados.get("endereco"),
            "cidade":           dados.get("cidade"),
            "estado":           dados.get("estado"),
            "cep":              dados.get("cep"),
            "convenio":         dados.get("convenio"),
        })

    data_consulta = dados["data_consulta"]
    consulta = criar_consulta({
        "paciente_id":   paciente["id"],
        "usuario_id":    usuario_id,
        "data_consulta": str(data_consulta) if data_consulta else None,
        "especialidade": dados.get("especialidade"),
        "motivo":        dados.get("motivo"),
        "status":        dados.get("status", "agendada"),
        "observacoes":   dados.get("observacoes"),
        "valor":         dados.get("valor"),
    })

    return {
        "consulta": consulta,
        "paciente": paciente
    }