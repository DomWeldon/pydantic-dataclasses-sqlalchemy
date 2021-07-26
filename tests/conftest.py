# Third Party Libraries
import pytest
import sqlalchemy as sa
import sqlalchemy.orm as orm
from pdsqla import models


@pytest.fixture(scope="function")
def engine() -> sa.engine.Engine:
    """Create a SQLite in-memory db engine"""
    return sa.create_engine("sqlite://")


@pytest.fixture(scope="function")
def tables(engine):
    """Create and destroy tables for each test"""
    models.Base.metadata.create_all(engine)
    yield
    models.Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def session(tables, engine) -> orm.Session:
    """Scoped session for each test"""
    SessionLocal = orm.sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    session = SessionLocal()

    yield session

    session.close()
