from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.usuario_controller import router as usuario_router
from app.controllers.login_controller import router as login_router
import os
from fastapi.responses import Response

# 1. 先创建 app 实例（必须在所有 @app.xxx 装饰器之前）
app = FastAPI(
    title="Game Starter API",
    description="API para sistema de login com auditoria",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 2. 再定义 favicon 接口（现在 app 已存在，不会报错）
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

# 3. 后续配置不变
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

app.include_router(usuario_router)
app.include_router(login_router)

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
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info" 
    )