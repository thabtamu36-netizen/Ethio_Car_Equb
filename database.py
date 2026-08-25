from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL


# =========================================================
# DATABASE ENGINE
# =========================================================

engine = create_engine(
    DATABASE_URL,
    echo=False
)


# =========================================================
# BASE
# =========================================================

Base = declarative_base()


# =========================================================
# SESSION
# =========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


# =========================================================
# GET DATABASE SESSION
# =========================================================

def get_db():

    return SessionLocal()


# =========================================================
# CREATE TABLES
# =========================================================

def init_db():

    from models import User, Payment

    Base.metadata.create_all(
        bind=engine
    )