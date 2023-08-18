from asyncio import current_task
from functools import lru_cache

from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


database_connection_string = "mysql+aiomysql://root:password@localhost:3306/dev"
engine = create_async_engine(database_connection_string, pool_size=3)
async_session_factory = sessionmaker(bind=engine, class_=AsyncSession)

session = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=current_task,
)
Base = declarative_base()
load_dotenv()


async def get_session() -> AsyncSession:
    db = session()
    try:
        yield db
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    finally:
        await db.close()


class Settings(BaseSettings):
    secret_key: str
    model_config = SettingsConfigDict(env_file='.env')


@lru_cache()
def get_setting():
    return Settings()