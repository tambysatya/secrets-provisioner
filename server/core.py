from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
import os

TOKENS = Path(os.environ.get("TOKEN_DIR", "./tokens"))

app = FastAPI()

@app.get("/{token}")
def bootstrap(token: str):
    path = TOKENS / token

    if not path.is_file():
        raise HTTPException(404)

    data = path.read_bytes()
    path.unlink()

    return Response(data, media_type="application/json")
