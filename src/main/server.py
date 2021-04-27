from src.main.router import setup_routes
from src.main.settings import app, IP, PORT

if __name__ == "__main__":
    setup_routes(app)
    app.run(host=IP, port=PORT)