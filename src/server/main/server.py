from router import setup_router
from settings import APP, IP, PORT

if __name__ == "__main__":
    setup_router()
    APP.run(host=IP, port=PORT)
