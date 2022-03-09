from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    descricao = Column(String)
    prioridade = Column(Integer)
    completo = Column(Boolean, default=False)