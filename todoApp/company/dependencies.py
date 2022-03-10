from fastapi import Header, HTTPException

async def getTokenHeader(tokenInterno: str = Header(...)):
    if tokenInterno != "allowed":
        raise HTTPException(status_code=400, detail="header de token interno inválido")