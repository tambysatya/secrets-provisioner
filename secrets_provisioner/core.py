from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
import os
from cryptography import x509
from cryptography.x509.oid import ExtensionOID

app = FastAPI()

TOKENS = Path(os.environ.get("TOKEN_DIR", "./tokens"))



@app.get("/whoami")
async def whoami(request: Request):
    tls = request.scope.get("extensions", {}).get("tls")
    if not tls:
        raise HTTPException(500, "TLS extension unavailable")

    chain = tls.get("client_cert_chain", [])
    if not chain:
        raise HTTPException(401, "No client certificate")

    cert = x509.load_pem_x509_certificate(chain[0])

    san = cert.extensions.get_extension_for_oid(
        ExtensionOID.SUBJECT_ALTERNATIVE_NAME
    ).value

    return {
        "dns": san.get_values_for_type(x509.DNSName),
        "uris": [str(uri) for uri in san.get_values_for_type(x509.UniformResourceIdentifier)]
    }

@app.get("/{token}")
def bootstrap(token: str):
    path = TOKENS / token

    if not path.is_file():
        raise HTTPException(404)

    data = path.read_bytes()
    path.unlink()

    return Response(data, media_type="application/json")
