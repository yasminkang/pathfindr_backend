from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.database.oracle import get_connection
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class LoginInput(BaseModel):
    email_usuario: EmailStr
    senha_usuario: str

@router.post("/usuarios/login")
async def login_usuario(login_input: LoginInput):
    """
    Faz login do usuário verificando email e senha no banco de dados.
    Retorna erro 401 se as credenciais forem inválidas.
    """
    conn = None
    cursor = None
    try:
        logger.info(f"Tentando fazer login: {login_input.email_usuario}")
        conn = get_connection()
        cursor = conn.cursor()
        
        # Busca o usuário no banco de dados
        cursor.execute(
            "SELECT ID_USUARIO, EMAIL_USUARIO FROM PATHFINDR_USUARIOS WHERE EMAIL_USUARIO = :1 AND SENHA_USUARIO = :2",
            (login_input.email_usuario, login_input.senha_usuario)
        )
        row = cursor.fetchone()
        
        if row:
            # Usuário encontrado e senha correta
            logger.info(f"Login bem-sucedido para usuário ID: {row[0]}")
            return {
                "mensagem": "Login bem-sucedido",
                "id_usuario": row[0],
                "email_usuario": row[1]
            }
        else:
            # Usuário não encontrado ou senha incorreta
            logger.warning(f"Tentativa de login falhou para: {login_input.email_usuario}")
            raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")
            
    except HTTPException:
        # Re-raise HTTPExceptions (como 401)
        raise
    except Exception as e:
        logger.error(f"Erro ao fazer login: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao fazer login: {str(e)}")
    finally:
        # Fecha cursor e conexão
        if cursor:
            cursor.close()
        if conn:
            conn.close()
