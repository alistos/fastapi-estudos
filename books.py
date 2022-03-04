from ast import Delete
from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

livros = {
    'livro 1': {'titulo': 'Titulo 1', 'autor': 'Autor 1'},
    'livro 2': {'titulo': 'Titulo 2', 'autor': 'Autor 2'},
    'livro 3': {'titulo': 'Titulo 3', 'autor': 'Autor 3'},
    'livro 4': {'titulo': 'Titulo 4', 'autor': 'Autor 4'},
    'livro 5': {'titulo': 'Titulo 5', 'autor': 'Autor 5'},
}

class NomeDirecao(str, Enum):
    norte = "Norte"
    sul = "Sul"
    leste = "Leste"
    oeste = "Oeste"

#@app.get("/")
#async def lerTodosLivros():
#    return livros

#ler todos os livros com query
@app.get("/")
async def lerTodosLiros(pularLivro: Optional[str] = None):
    if pularLivro:
        novosLivros = livros.copy()
        del novosLivros[pularLivro]
        return novosLivros
    return livros

@app.get("/livros/meuLivro")
async def lerLivroFavorito():
    return {"tituloLivro": "Meu Livro Favorito"}

#Versão melhorada do get acima
@app.get("/{nomeLivro}")
async def lerLivro(nomeLivro: str):
    return livros[nomeLivro]

#parametros precisam estar sempre abaixo de rotas com caminhos que passam pelo mesmo lugar
@app.get("/livros/{livroId}")
async def lerLivro(livroId: int):
    return {"tituloLivro": livroId}

#Paramêtros enum
@app.get("/direcoes/{nomeDirecao}")
async def getDirecao(nomeDirecao: NomeDirecao):
    if nomeDirecao == NomeDirecao.norte:
        return {"Direcao": nomeDirecao, "sub": "Cima"}
    if nomeDirecao == NomeDirecao.sul:
        return {"Direcao": nomeDirecao, "sub": "Baixo"}
    if nomeDirecao == NomeDirecao.leste:
        return {"Direcao": nomeDirecao, "sub": "Direita"}
    if nomeDirecao == NomeDirecao.oeste:
        return {"Direcao": nomeDirecao, "sub": "Esquerda"}

#Post request
@app.post("/")
async def criarLivro(tituloLivro, autorLivro):
    idLivroAtual = 0
    if len(livros) > 0:
        for livro in livros:
            x = int(livro.split(' ')[-1])
            if x > idLivroAtual:
                idLivroAtual = x

    livros[f'livro {idLivroAtual+1}'] = {'titulo': tituloLivro, 'autor': autorLivro}
    return livros[f'livro {idLivroAtual}']

#Put request (update)
@app.put("/{nomaLivro}")
async def atualizarLivro(nomeLivro: str, tituloLivro: str, autorLivro: str):
    informacaoLivro = {'titulo': tituloLivro, 'autor': autorLivro}
    livros[nomeLivro] = informacaoLivro
    return informacaoLivro

#Delete request
@app.delete("/{nomeLivro}")
async def deletarLivro(nomeLivro):
    del livros[nomeLivro]
    return f'Livro {nomeLivro} deletado'