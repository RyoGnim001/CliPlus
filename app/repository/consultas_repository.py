from app.database.supabase_client import supabase

def criar_consulta(dados: dict):
    response = supabase.table("consultas")\
        .insert(dados)\
        .execute()
    return response.data[0]