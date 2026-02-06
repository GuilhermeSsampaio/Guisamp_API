import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True, # true para mostrar as queries no console
    connect_args={"client_encoding": "utf8"},
    pool_pre_ping=True # verificar se está ativo antes de conectar

)


def create_db_and_tables():
    """"
    Cria as tabelas conforme os models definidos
    Deve ser chamada uma vez ao iniciar o projeto ou atualizar modelos
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """"
    Cria uma sessão de conexão com o banco
    Usada para trabalhas o crud dentro dos endpoints, deve ser usado 
    como dependência das rotas para acessar o banco de forma segura e automática
    """
    with Session(engine) as session:
        yield session
