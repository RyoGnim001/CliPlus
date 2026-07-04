from apiflask.fields import String, Date, DateTime
from apiflask.validators import Length, OneOf
from apiflask import Schema

class ConsultaSchema(Schema):
    # dados do paciente
    cpf             = String(required=True, validate=Length(equal=11))
    nome_completo   = String(required=True, validate=Length(min=3, max=200))
    data_nascimento = Date(required=False)
    sexo            = String(required=False, validate=OneOf(["masculino", "feminino", "outro"]))
    telefone        = String(required=False, validate=Length(max=20))
    email           = String(required=False)
    endereco        = String(required=False)
    cidade          = String(required=False)
    estado          = String(required=False, validate=Length(equal=2))
    cep             = String(required=False, validate=Length(max=9))
    convenio        = String(required=False)

    # dados da consulta
    data_consulta   = DateTime(required=True)
    especialidade   = String(required=False)
    motivo          = String(required=False)
    status          = String(required=False, validate=OneOf(["agendada", "realizada", "cancelada"]))
    observacoes     = String(required=False)