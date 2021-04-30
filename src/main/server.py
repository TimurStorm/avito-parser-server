from router import setup_vk_mailing
from settings import APP, IP, PORT

if __name__ == "__main__":
    setup_vk_mailing()
    APP.run(host=IP, port=PORT)
