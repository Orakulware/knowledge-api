from config import AuthCredsConfig, PostgresConfig, RabbitMQConfig, RedisConfig
from dependency_injector import containers, providers


class ApplicationConfigProvider(containers.DeclarativeContainer):
    postgres = providers.Singleton(PostgresConfig.from_env)
    rabbitmq = providers.Singleton(RabbitMQConfig.from_env)
    redis = providers.Singleton(RedisConfig.from_env)
    auth_creds = providers.Singleton(AuthCredsConfig)
