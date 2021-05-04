class User:
    def __init__(self, email: str, password: str, username: str, vk_id=None, vk_token=None):
        self.user_id = id
        self.email = email
        self.password = password
        self.username = username
        self.vk_id = vk_id
        self.vk_token = vk_token

    def __repr__(self):
        return "User(id='{}')".format(self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}
