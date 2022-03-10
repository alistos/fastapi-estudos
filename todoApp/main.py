from fastapi import FastAPI, Depends
import models
from database import engine
from routers import auth, todos
from company import companyapis, dependencies

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
#routing externo
app.include_router(
    companyapis.router,
    prefix="/companyapis",
    tags=["companyapis"],
    dependencies=[Depends(dependencies.getTokenHeader)],
    responses={418: {"descricao": "Acesso apenas para usuários internos"}}
)

