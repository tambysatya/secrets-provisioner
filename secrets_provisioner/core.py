from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
import os
from cryptography import x509
from cryptography.x509.oid import ExtensionOID

app = FastAPI()

TOKENS = Path(os.environ.get("TOKEN_DIR", "./tokens"))


@app.get("/debug")
async def debug(request: Request):
    return {
        "extensions": request.scope.get("extensions", {}),
        "scope_keys": list(request.scope.keys()),
    }

@app.get("/mtls")
async def whoami(request: Request):
    tls = request.scope.get("extensions", {}).get("tls")
    if not tls:
        raise HTTPException(500, "TLS extension unavailable")

    chain = tls.get("client_cert_chain", [])
    if not chain:
        raise HTTPException(401, "No client certificate")

    cert = x509.load_pem_x509_certificate(chain[0].encode())

    san = cert.extensions.get_extension_for_oid(
        ExtensionOID.SUBJECT_ALTERNATIVE_NAME
    ).value

    dns = san.get_values_for_type(x509.DNSName),
    if dns == []:
        raise HTTPException(401, "No san in the certificate")
    name = dns[0][0].split(".")[0]
    name = name + ".tar.gz"

    path = TOKENS / name
    print (path)

    if not path.is_file():
        raise HTTPException(404)

    data = path.read_bytes()
    path.unlink()




    return Response(data, media_type="application/json")
   # return {
   #     "dns": name,
   #     "uris": [str(uri) for uri in san.get_values_for_type(x509.UniformResourceIdentifier)]
   # }

@app.get("/{token}")
def bootstrap(token: str):
    path = TOKENS / token

    if not path.is_file():
        raise HTTPException(404)

    data = path.read_bytes()
    path.unlink()

    return Response(data, media_type="application/json")
