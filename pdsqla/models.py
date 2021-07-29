"""Register our models on the declarative base"""
# Third Party Libraries
import sqlalchemy as sa

# Local Folder
from . import base_class, dcs

Base = base_class.Base

A = Base.registry.mapped(dcs.A)
B = Base.registry.mapped(dcs.B)
D = Base.registry.mapped(dcs.D)


@Base.registry.mapped
class C:
    __tablename__ = "c"

    c_id: int = sa.Column(sa.Integer, primary_key=True)
    c: str = sa.Column(sa.String)


__all__ = ["A", "B", "C", "Base"]
