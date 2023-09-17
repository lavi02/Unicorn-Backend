import json
import os
from dependency_injector import providers, containers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from pydantic import Field
import redis


class DatabaseSettings(BaseSettings):
    host: str = Field(default="localhost", env="DB_HOST")
    host_real: str = Field(default="localhost", env="DB_HOST_REAL")
    port: int = Field(default=3306, env="DB_PORT")
    name: str = Field(default="develop", env="DB_NAME")
    username: str = Field(default="dev", env="DB_USER")
    password: str = Field(default="localplayer0", env="DB_PASSWORD")
    password_real: str = Field(default="localplayer0", env="DB_PASSWORD_REAL")


class RedisSettings(BaseSettings):
    host: str = Field(default="localhost", env="REDIS_HOST")
    port: int = Field(default=6379, env="REDIS_PORT")
    name: int = Field(default=0, env="REDIS_NAME")

#########################################################################################


class ApplicationSettings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()


class BaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_dict(ApplicationSettings().model_dump())

    engine = providers.Singleton(
    create_engine,
    url=providers.Callable(
        lambda config: f"mysql+pymysql://{config['db']['username']}:{config['db']['password']}@{config['db']['host']}:{config['db']['port']}/{config['db']['name']}",
        config=config 
    ),
    echo=True,
)

    SessionLocal = providers.Singleton(
        sessionmaker,
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    redis_client = providers.Singleton(
        redis.StrictRedis,
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.name
    )


dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, '../../config.json'), "r") as f:
    config_data = json.load(f)

app_settings = ApplicationSettings(**config_data)
container = BaseContainer()
container.config.from_dict(app_settings.model_dump())

redis_client = container.redis_client()

def get_db():
    db = container.SessionLocal()
    try:
        yield db
    except Exception as e:
        db().rollback()
    finally:
        db().close()
