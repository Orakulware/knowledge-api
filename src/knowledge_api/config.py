import os


class AuthCredsConfig:
    access_username: str
    access_password: str

    def __init__(self) -> None:
        login_username = os.getenv("ADMIN_LOGIN") or "admin"
        login_password = os.getenv("ADMIN_PASSWORD") or "admin"

        self.access_username = login_username
        self.access_password = login_password
