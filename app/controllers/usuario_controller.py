from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.database.oracle import get_connection

router = APIRouter()

class UsuarioCreate(BaseModel):
    email_usuario: EmailStr
    senha_usuario: str

@router.post("/usuarios/cadastrar")
async def cadastrar_usuario(usuario: UsuarioCreate):
    # Gera novo ID sequencialmente (simples, ideal seria sequence no Oracle)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT NVL(MAX(ID_USUARIO), 0) + 1 FROM PATHFINDR_USUARIOS")
        novo_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO PATHFINDR_USUARIOS (ID_USUARIO, EMAIL_USUARIO, SENHA_USUARIO) VALUES (:1, :2, :3)",
            (novo_id, usuario.email_usuario, usuario.senha_usuario)
        )
        conn.commit()
    except Exception as e:
        # Trata erro de email duplicado
        if 'unique constraint' in str(e).lower():
            raise HTTPException(status_code=400, detail="E-mail já cadastrado")
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar: {e}")
    finally:
        cursor.close()
        conn.close()
    return {"mensagem": "Usuário cadastrado com sucesso"}