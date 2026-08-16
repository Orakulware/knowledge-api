import os
from dataclasses import dataclass


class ConfigError(ValueError):
    def __init__(self, variable_name: str) -> None:
        self._variable_name = variable_name

    def __str__(self) -> str:
        return f"Have you specified the variable {self._variable_name}?"


def _get_str_from_env(key: str) -> str:
    if value := os.getenv(key):
        return value
    raise ConfigError(variable_name=key)


class AuthCredsConfig:
    access_username: str
    access_password: str

    def __init__(self) -> None:
        login_username = os.getenv("ADMIN_LOGIN") or "admin"
        login_password = os.getenv("ADMIN_PASSWORD") or "admin"

        self.access_username = login_username
        self.access_password = login_password


@dataclass(frozen=True, slots=True)
class PostgresConfig:
    host: str
    port: str
    user: str
    password: str
    db: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @staticmethod
    def from_env() -> PostgresConfig:
        env_variables: dict[str, str] = {
            "host": _get_str_from_env("POSTGRES_HOST_ENV"),
            "port": _get_str_from_env("POSTGRES_PORT_ENV"),
            "user": _get_str_from_env("POSTGRES_USER_ENV"),
            "password": _get_str_from_env("POSTGRES_PASSWORD_ENV"),
            "db": _get_str_from_env("POSTGRES_DB_NAME_ENV"),
        }

        return PostgresConfig(**env_variables)


@dataclass(frozen=True, slots=True)
class RabbitMQConfig:
    host: str
    port: str
    user: str
    password: str
    vhost: str

    @property
    def url(self) -> str:
        return (
            f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}"
        )

    @staticmethod
    def from_env() -> RabbitMQConfig:
        env_variables: dict[str, str] = {
            "host": _get_str_from_env("RABBITMQ_HOST_ENV"),
            "port": _get_str_from_env("RABBITMQ_PORT_ENV"),
            "user": _get_str_from_env("RABBITMQ_USER_ENV"),
            "password": _get_str_from_env("RABBITMQ_PASSWORD_ENV"),
            "vhost": _get_str_from_env("RABBITMQ_VHOST_ENV"),
        }

        return RabbitMQConfig(**env_variables)


@dataclass(frozen=True, slots=True)
class RedisConfig:
    host: str
    port: str
    password: str
    db: str

    @property
    def url(self) -> str:
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"

    @staticmethod
    def from_env() -> RedisConfig:
        env_variables: dict[str, str] = {
            "host": _get_str_from_env("REDIS_HOST_ENV"),
            "port": _get_str_from_env("REDIS_PORT_ENV"),
            "password": _get_str_from_env("REDIS_PASSWORD_ENV"),
            "db": _get_str_from_env("REDIS_DB_ENV"),
        }

        return RedisConfig(**env_variables)
