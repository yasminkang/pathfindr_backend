from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.database.oracle import get_connection
import logging

logger = logging.getLogger(__name__)
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
        logger.info(f"Tentando cadastrar usuário: {usuario.email_usuario}")
        conn = get_connection()
        cursor = conn.cursor()
        
        # Gera novo ID sequencialmente
        logger.info("Gerando novo ID de usuário...")
        cursor.execute("SELECT NVL(MAX(ID_USUARIO), 0) + 1 FROM PATHFINDR_USUARIOS")
        novo_id = cursor.fetchone()[0]
        logger.info(f"Novo ID gerado: {novo_id}")
        
        # Insere o novo usuário
        logger.info("Inserindo usuário no banco...")
        cursor.execute(
            "INSERT INTO PATHFINDR_USUARIOS (ID_USUARIO, EMAIL_USUARIO, SENHA_USUARIO) VALUES (:1, :2, :3)",
            (novo_id, usuario.email_usuario, usuario.senha_usuario)
        )
        conn.commit()
        logger.info(f"Usuário cadastrado com sucesso! ID: {novo_id}")
        
        return {"mensagem": "Usuário cadastrado com sucesso", "id_usuario": novo_id}
        
    except Exception as e:
        # Log do erro completo
        logger.error(f"Erro ao cadastrar usuário: {str(e)}", exc_info=True)
        
        # Rollback em caso de erro
        if conn:
            try:
                conn.rollback()
            except:
                pass
        
        error_msg = str(e).lower()
        
        # Trata erro de email duplicado
        if 'unique constraint' in error_msg or 'ora-00001' in error_msg:
            logger.warning(f"Tentativa de cadastrar email duplicado: {usuario.email_usuario}")
            raise HTTPException(status_code=400, detail="E-mail já cadastrado")
        
        # Trata outros erros do Oracle
        if 'ora-' in error_msg:
            logger.error(f"Erro Oracle: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro no banco de dados Oracle: {str(e)}")
        
        # Erro genérico - retorna mensagem mais detalhada
        logger.error(f"Erro genérico: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar usuário: {type(e).__name__}: {str(e)}")
        
    finally:
        # Fecha cursor e conexão
        if cursor:
            cursor.close()
        if conn:
            conn.close()