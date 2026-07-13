import uvicorn


def main():
    uvicorn.run(
        "secrets_provisioner.core:app",
        host = "127.0.0.1"
        port=8080
        )


if __name__ == "__main__":
    main()
