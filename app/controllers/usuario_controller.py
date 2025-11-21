from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.database.oracle import get_connection

router = APIRouter()

class UsuarioCreate(BaseModel):
    email_usuario: EmailStr
    senha_usuario: str

@router.post("/usuarios/cadastrar")
async def cadastrar_usuario(usuario: UsuarioCreate):
    """
    Cadastra um novo usuário em PATHFINDR_USUARIOS.
    O ID é gerado de forma sequencial.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Gera novo ID sequencialmente
        cursor.execute("SELECT NVL(MAX(ID_USUARIO), 0) + 1 FROM PATHFINDR_USUARIOS")
        novo_id = cursor.fetchone()[0]
        
        # Insere o novo usuário
        cursor.execute(
            "INSERT INTO PATHFINDR_USUARIOS (ID_USUARIO, EMAIL_USUARIO, SENHA_USUARIO) VALUES (:1, :2, :3)",
            (novo_id, usuario.email_usuario, usuario.senha_usuario)
        )
        conn.commit()
        
        return {"mensagem": "Usuário cadastrado com sucesso", "id_usuario": novo_id}
        
    except Exception as e:
        # Rollback em caso de erro
        if conn:
            conn.rollback()
        
        error_msg = str(e).lower()
        
        # Trata erro de email duplicado
        if 'unique constraint' in error_msg or 'ora-00001' in error_msg:
            raise HTTPException(status_code=400, detail="E-mail já cadastrado")
        
        # Trata outros erros do Oracle
        if 'ora-' in error_msg:
            raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
        
        # Erro genérico
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar usuário: {str(e)}")
        
    finally:
        # Fecha cursor e conexão
        if cursor:
            cursor.close()
        if conn:
            conn.close()