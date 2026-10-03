import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config
from pathlib import Path
import os
import argparse

from .core import app

LISTEN = Path(os.environ.get("LISTEN_ADDR", "0.0.0.0:8000"))

def main():
    parser = argparse.ArgumentParser (
            prog = "A simple secret provisionner",
            description = "Opens a HTTPS server that reads a directory containing single-usage tokens and distribute it"
            )
    parser.add_argument ('--listen_on', help='the IP address to listen on', default="0.0.0.0")
    parser.add_argument ('--port', default="8080")
    parser.add_argument ('--ssl_cert', help='path to the ssl certificate')
    parser.add_argument ('--ssl_key', help ='path to the ssl certificate key')
    parser.add_argument ('--ssl_ca', help ='path to the ssl authority (mandatory for mTLS)', required=False)
    args = parser.parse_args()

    config = Config ()

    config.bind = [args.listen_on + ":" + args.port]

    config.certfile = args.ssl_cert
    config.keyfile = args.ssl_key

    if args.ssl_ca != None:
        config.ca_certs = args.ssl_ca
        config.very_mode = ssl.CERT_REQUIRED

    asyncio.run(serve(app, config))

