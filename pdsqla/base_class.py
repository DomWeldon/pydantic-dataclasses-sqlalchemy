# Third Party Libraries
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Declarative base for models."""

    pass
