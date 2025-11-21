from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Game Starter API",
    description="API para sistema de login com auditoria",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://*.vercel.app",
    "https://banco-de-dados-human-exe-5l9x.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    from app.controllers.usuario_controller import router as usuario_router
    from app.controllers.login_controller import router as login_router
    
    app.include_router(usuario_router)
    app.include_router(login_router)
    logger.info("✅ Rotas de controllers registradas com sucesso!")
except Exception as e:
    logger.error(f"❌ Falha ao importar rotas: {str(e)}", exc_info=True)
    raise

@app.get("/")
async def root():
    return {
        "message": "Game Starter API ativa!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    logger.info(f"🚀 Iniciando servidor na porta: {port}")
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0", 
            port=port,
            log_level="info",
            reload=False,
            workers=1 
        )
    except Exception as e:
        logger.error(f"❌ Falha ao iniciar servidor: {str(e)}", exc_info=True)
        raise