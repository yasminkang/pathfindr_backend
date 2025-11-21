import oracledb
from app.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SID

dsn = f"{DB_HOST}:{DB_PORT}/{DB_SID}"

def obter_conexao():
    try:
        conexao = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=dsn,
            ssl_server_dn_match=False, 
            ssl_version=oracledb.SSLVersion.TLSv1_2,
            timeout=10 
        )
        print(f"✅ Conexão com o banco de dados bem-sucedida! Usuário: {DB_USER}, Host: {DB_HOST}")
        return conexao
    except oracledb.Error as e:
        erro, = e.args
        mensagem_erro = (
            f"Código do erro: {erro.code}\n"
            f"Mensagem do erro: {erro.message}\n"
            f"Configurações de conexão: Usuário={DB_USER}, Host={DB_HOST}, Porta={DB_PORT}, SID={DB_SID}"
        )
        print(f"❌ Falha ao conectar ao banco de dados:\n{mensagem_erro}")
        raise Exception(f"Erro ao conectar ao banco de dados: {erro.message}") from e
    except Exception as e:
        print(f"❌ Erro inesperado ao conectar ao banco de dados: {str(e)}")
        raise Exception(f"Erro inesperado ao conectar ao banco de dados: {str(e)}") from e

if __name__ == "__main__":
    try:
        conn = obter_conexao()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM DUAL")
            resultado = cursor.fetchone()
            print(f"✅ Teste de conexão bem-sucedido! Resultado da consulta: {resultado}")
        conn.close()
        print("✅ Conexão fechada com sucesso")
    except Exception as e:
        print(f"❌ Teste de conexão falhou: {str(e)}")