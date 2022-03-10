from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def getNomeCompania():
    return {"nomeCompania": "Exemplo Compania, LLC"}

@router.get("/empregados")
async def numeroEmpregados():
    return 162