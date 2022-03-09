from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Todo(BaseModel):
    titulo: str
    descricao: Optional[str] 
    prioridade: int = Field(gt=0, lt=6, description="A prioridade deve estar entre 1-5")
    completo: bool   

#Ler todos os todos
@app.get("/")
async def lerTodos(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()

#Encontrar todo pelo id
@app.get("/todo/{todoId}")
async def lerTodo(todoId: int, db: Session = Depends(get_db)):
    todoModel = db.query(models.Todos).filter(models.Todos.id == todoId).first

    if todoModel is not None:
        return todoModel

    raise http_exception

#Adicionar Todo para o db
@app.post("/")
async def criarTodo(todo: Todo, db: Session = Depends(get_db)):
    todoModel = models.Todos()
    todoModel.titulo = todo.titulo
    todoModel.descricao = todo.descricao
    todoModel.prioridade = todo.prioridade
    todoModel.completo = todo.completo

    db.add(todoModel)
    db.commit()

    succesful_response(201)

#Atualizar todo no db
@app.put("/{todoID}")
async def atualizarTodo(todoId: int, todo: Todo, db: Session = Depends(get_db)):
    todoModel = db.query(models.Todos).filter(models.Todos.id == todoId).first()

    if todoModel is None:
        raise http_exception()

    todoModel.titulo = todo.titulo
    todoModel.descricao = todo.descricao
    todoModel.prioridade = todo.prioridade
    todoModel.completo = todo.completo

    db.add(todoModel)
    db.commit()

    succesful_response(200)

#deleter todo no db
@app.delete("/{todoId}")
async def deletarTodo(todoId: int, db: Session = Depends(get_db)):
    todoModel = db.query(models.Todos).filter(models.Todos.id == todoId).first()

    if todoModel is None:
        raise http_exception()

    db.query(models.Todos).filter(models.Todos.id).delete()
    db.commit()

    succesful_response(200)

def http_exception():
    return HTTPException(status_code=404, detail="Todo não encontrado")

def succesful_response(status_code: int):
    return{
        'status': status_code,
        'transaction': 'Successful'
    }
