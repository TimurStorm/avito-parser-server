class User:
    def __init__(self, username: str, login: str, password: str, email: str):
        self.username = username
        self.login = login
        self.password = password
        self.email = email

    def __str__(self):
        return f"User with login: {self.login}"
