from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from infrastructure.driven_adapters.sqlite_adapter.base import Base

_URLS_EN_MEMORIA = ("sqlite://", "sqlite:///:memory:")


def crear_engine(url: str = "sqlite:///:memory:") -> Engine:
    args = {"check_same_thread": False}
    if url in _URLS_EN_MEMORIA:
        return create_engine(url, connect_args=args, poolclass=StaticPool)
    return create_engine(url, connect_args=args)


def crear_session_factory(engine: Engine) -> sessionmaker:
    return sessionmaker(bind=engine, expire_on_commit=False)


def crear_tablas(engine: Engine) -> None:
    from infrastructure.driven_adapters.sqlite_adapter import dbo  # noqa: F401

    Base.metadata.create_all(engine)
