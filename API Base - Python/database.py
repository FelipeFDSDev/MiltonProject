from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Configuração do banco de dados SQLite
# O caminho abaixo cria o arquivo 'sql_app.db' na pasta raiz do projeto
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Cria o motor de conexão
# check_same_thread=False é necessário apenas para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria a SessionLocal para uso no código
# Essa classe será usada para criar a sessão do DB para cada requisição
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos (classes)
Base = declarative_base()

# ----------------------------------------------------------------------
# Modelo ORM (SQLAlchemy) - Mapeamento para a Tabela do Banco de Dados
# ----------------------------------------------------------------------

class Contact(Base):
    """
    Representa a tabela 'contacts' no banco de dados.
    """
    __tablename__ = "contacts"

    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True) # Opcional no Pydantic, nullable no DB
    codExterno = Column(String, nullable=True, unique=True)
    canalPref = Column(String)
    
    # Foreign Key para Cliente (opcional - se quiser vincular contatos a clientes)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=True)
    
    # Relacionamento com Cliente
    cliente = relationship("Cliente", back_populates="contatos")
# Cria as tabelas no banco de dados (se não existirem)
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)