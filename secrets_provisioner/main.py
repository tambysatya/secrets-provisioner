import uvicorn
import argparse



def main():
    parser = argparse.ArgumentParser (
            prog = "A simple secret provisionner",
            description = "Opens a HTTPS server that reads a directory containing single-usage tokens and distribute it"
            )

    parser.add_argument ('--listen_on', help='the IP address to listen on', default="127.0.0.1")
    parser.add_argument ('--port', help='port', default=8080)
    parser.add_argument ('--ssl_cert', help='path to the ssl certificate', required=False)
    parser.add_argument ('--ssl_key', help ='path to the ssl certificate key', required=False)

    args = parser.parse_args()
    if (None == args.ssl_key) or (None == args.ssl_cert):
        print (f"Running HTTP on {args.listen_on}:{args.port}")
        uvicorn.run(
            "secrets_provisioner.core:app",
            host = args.listen_on,
            port= args.port
            )
    else:
        print (f"Running HTTP+TLS on {args.listen_on}:{args.port}")
        uvicorn.run(
            "secrets_provisioner.core:app",
            host = args.listen_on,
            port= args.port,
            ssl_certfile = args.ssl_cert,
            ssl_keyfile = args.ssl_key
            )



if __name__ == "__main__":
    main()
