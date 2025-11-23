from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

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
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="contatos")
    mensagens_agendadas = relationship("MensagemAgendada", back_populates="contato", cascade="all, delete-orphan")

# Tabela de Clientes
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento com contatos
    contatos = relationship("Contact", back_populates="cliente")

# Tabela de Histórico de Mensagens
class HistoricoMensagem(Base):
    __tablename__ = "historico_mensagens"
    
    id = Column(Integer, primary_key=True, index=True)
    canal = Column(String, nullable=False)
    destinatario = Column(String, nullable=False)
    conteudo = Column(Text, nullable=False)
    status = Column(String, default="PENDENTE")
    data_envio = Column(DateTime, default=datetime.utcnow)

# Tabela de Mensagens Agendadas
class MensagemAgendada(Base):
    __tablename__ = "mensagens_agendadas"
    
    id = Column(Integer, primary_key=True, index=True)
    contato_id = Column(Integer, ForeignKey('contacts.id'), nullable=False)
    canal = Column(String, nullable=False)
    destinatario = Column(String, nullable=False)
    assunto = Column(String, nullable=True)
    conteudo = Column(Text, nullable=False)
    data_agendamento = Column(DateTime, nullable=False)
    status = Column(String, default="AGENDADO")
    criado_em = Column(DateTime, default=datetime.utcnow)
    enviado_em = Column(DateTime, nullable=True)
    erro_mensagem = Column(Text, nullable=True)
    
    # Relacionamento com Contato
    contato = relationship("Contact", back_populates="mensagens_agendadas")

# Tabela de Usuários
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

def create_db_and_tables():
    """Cria todas as tabelas no banco de dados se não existirem."""
    Base.metadata.create_all(bind=engine)