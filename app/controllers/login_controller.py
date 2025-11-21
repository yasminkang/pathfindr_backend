from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.database.oracle import get_connection

router = APIRouter()

class LoginInput(BaseModel):
    email_usuario: EmailStr
    senha_usuario: str

@router.post("/usuarios/login")
async def login_usuario(login_input: LoginInput):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT ID_USUARIO FROM PATHFINDR_USUARIOS WHERE EMAIL_USUARIO = :1 AND SENHA_USUARIO = :2",
        (login_input.email_usuario, login_input.senha_usuario)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return {"mensagem": "Login bem-sucedido", "id_usuario": row[0], "email_usuario": login_input.email_usuario}
    else:
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")