import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy import text

# Import router do pacote auth (imports absolutos necessários para execução
# quando `main.py` é carregado como módulo top-level por uvicorn)
from auth.view_auth import router as auth_router
from config.settings import settings
from config.database import Base, engine

logger = logging.getLogger("uvicorn")

app = FastAPI(
    title="Autenticação - Diário de Enxaqueca",
    version="1.0.0",
    debug=settings.DEBUG,
)

# Configurar origens permitidas para CORS
origins = [
    "http://localhost:3000",
    "http://frontend",
]

# Adicionar URL do frontend de produção se configurado
if settings.FRONTEND_URL and settings.FRONTEND_URL not in origins:
    origins.append(settings.FRONTEND_URL)

# Em produção, aceitar origens Railway e Vercel
if settings.ENVIRONMENT == "production":
    origins.extend([
        "https://*.railway.app",
        "https://*.vercel.app",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if settings.ENVIRONMENT != "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])


@app.on_event("startup")
def startup_event():
    """Cria apenas se ausente e loga contagem de registros."""
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT COUNT(*) FROM information_schema.tables "
                    "WHERE table_schema = :db AND table_name = 'usuarios'"
                ),
                {"db": settings.MYSQL_DB},
            ).scalar()
            if result == 0:
                Base.metadata.create_all(bind=conn)
                logger.info("Tabela usuarios criada (ausente)")
            else:
                logger.info("Tabela usuarios já existe; pulando create_all")

            try:
                count = conn.execute(
                    text("SELECT COUNT(*) FROM usuarios")
                ).scalar()
                logger.info("usuarios possui %d registros", count)
            except SQLAlchemyError as inner_exc:
                logger.warning("Falha ao contar usuarios: %s", inner_exc)
    except OperationalError as exc:
        logger.error("Erro ao verificar/criar tabelas: %s", exc)


@app.get("/health")
def health():
    return {"status": "healthy"}
