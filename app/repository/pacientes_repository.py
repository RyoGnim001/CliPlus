from app.database.supabase_client import supabase
from postgrest.exceptions import APIError

def buscar_por_cpf(cpf: str):
    try:
        response = supabase.table("pacientes")\
            .select("*")\
            .eq("cpf", cpf)\
            .single()\
            .execute()
        return response.data
    except APIError:
        return None
    
def criar_paciente(dados: dict):
    response = supabase.table("pacientes")\
        .insert(dados)\
        .execute()
    return response.data[0]