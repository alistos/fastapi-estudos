from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

app = FastAPI()

class Livro(BaseModel):
    id: UUID
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1, max_length=100)
    descricao: Optional[str] = Field(title="Descrição do livro",
     max_length=100,
     min_length=1)
    nota: int = Field(gt=-1, lt=101)

    class Config:
        schemaExtra = {
            "exemplo": {"id": "11163899-b103-4239-92eb-dddb8ebc19da",
            "titulo": "Computer Science Pro",
            "autor": "Codingwithroby",
            "descricao": "A very nice description of a book",
            "nota": 75
            }
        }

livros = []

@app.get("/")
async def lerTodosLivros(livrosParaRetornar: Optional[int] = None):
    if len(livros) < 1:
        criarLivrosSemApi()
    if livrosParaRetornar and len(livros) >= livrosParaRetornar > 0:
        i = 1
        novosLivros = []
        while i <= livrosParaRetornar:
            novosLivros.append(livros[i-1])
            i += 1
        return novosLivros
    return livros

@app.get("/livro/{livroId}")
async def lerLivro(livroId:UUID):
    for x in livros:
        if x.id == livroId:
            return x

@app.post("/")
async def criarLivro(livro: Livro):
    livros.append(livro)
    return livro

@app.put("/{livroId}")
async def atualizarLivro(livroId: UUID, livro: Livro):
    cont = 0
    for x in livros:
        cont += 1
        if x.id == livroId:
            livros[cont - 1] = livro
            return livros[cont-1]

@app.delete("/{livroId}")
async def deletarLivro(livroId: UUID):
    cont = 0
    for x in livros:
        cont += 1
        if x.id == livroId:
            del livros[cont - 1]
            return f'ID:{livroId} deletado'

def criarLivrosSemApi():
    livro1 = Livro(id="e1163899-b103-4239-92eb-dddb8ebc19da",
        titulo = "titulo1",
        autor = "autor1",
        descricao = "descricao1",
        nota=60)
    livro2 = Livro(id="f99f3704-149e-449f-b69f-f90bb3dc1bfd",
        titulo = "titulo2",
        autor = "autor2",
        descricao = "descricao2",
        nota=65)
    livro3 = Livro(id="c4add45b-4d2b-47bf-a356-e55a78b37eab",
        titulo = "titulo3",
        autor = "autor3",
        descricao = "descricao3",
        nota=63)
    livro4 = Livro(id="b447fe3f-500a-44fd-9d8b-ff758068a8f7",
        titulo = "titulo4",
        autor = "autor4",
        descricao = "descricao4",
        nota=45)
    livros.append(livro1)
    livros.append(livro2)
    livros.append(livro3)
    livros.append(livro4)