from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ..config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def create_session():
    session = Session(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

    return session


def get_session():
    session = Session(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

    try:
        yield session
    finally:
        session.close()
