from msilib.schema import Error
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from starlette.responses import JSONResponse

class NumeroNegativoException(Exception):
    def __init__(self, livrosParaRetornar):
        self.livrosParaRetornar = livrosParaRetornar

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

class LivroSemNota(BaseModel):
    id: UUID
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1, max_length=100)
    descricao: Optional[str] = Field(title="Descrição do livro",
     max_length=100,
     min_length=1)

livros = []

@app.exception_handler(NumeroNegativoException)
async def numeroNegativoExceptionHandler(request: Request,
    exception: NumeroNegativoException):
    return JSONResponse(status_code=418,
    content={"message": f'Ei, por que você quer {exception.livrosParaRetornar} livros? Você precisa ler mais!'})

@app.post("/livros/login")
async def livroLogin(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}

@app.get("/header")
async def lerHeader(randomHeader: Optional[str] = Header(None)):
    return {"Random-Header": randomHeader}

@app.get("/")
async def lerTodosLivros(livrosParaRetornar: Optional[int] = None):
    if livrosParaRetornar and livrosParaRetornar < 0:
        raise NumeroNegativoException(livrosParaRetornar=livrosParaRetornar)

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
    raise raiseLivroNaoEncontradoException()

@app.get("/livro/nota/{livroId}", response_model=LivroSemNota)
async def lerLivroSemNota(livroId:UUID):
    for x in livros:
        if x.id == livroId:
            return x
    raise raiseLivroNaoEncontradoException()

@app.post("/", status_code=status.HTTP_201_CREATED)
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
    raise raiseLivroNaoEncontradoException()

@app.delete("/{livroId}")
async def deletarLivro(livroId: UUID):
    cont = 0
    for x in livros:
        cont += 1
        if x.id == livroId:
            del livros[cont - 1]
            return f'ID:{livroId} deletado'
    raise raiseLivroNaoEncontradoException()

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

def raiseLivroNaoEncontradoException():
    return HTTPException(status_code=404,
    detail="Livro não encontrado",
    headers={"X-Header-Error":"UUID nãon está presente na base"})