import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

# O sqlite precisa dessa configuração extra
connect_args = {}
if "sqlite" in database_url:
    connect_args["check_same_thread"] = False

engine = create_engine(
    database_url, 
    echo=True, 
    connect_args=connect_args
)

def get_session():
    """Dependency para obter sessão do banco de dados"""
    with Session(engine) as session:
        yield session