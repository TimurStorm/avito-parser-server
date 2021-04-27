from main.router import setup_routes
from main.settings import *

if __name__ == "__main__":

    setup_routes(app)
    app.run(host=IP, port=PORT)
