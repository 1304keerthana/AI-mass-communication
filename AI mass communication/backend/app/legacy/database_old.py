from pathlib import Path
from typing import Generator

from sqlmodel import SQLModel, Session, create_engine

DB_FILE = Path(__file__).resolve().parent.parent / "comm.db"
engine = create_engine(f"sqlite:///{DB_FILE}", echo=False, connect_args={"check_same_thread": False})


def init_db() -> None:
    from . import models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
