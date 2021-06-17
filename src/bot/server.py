import sanic
from settings import APP, PORT, IP
from router import setup_router

if __name__ == "__main__":
    setup_router()
    APP.run(host=IP, port=PORT)
