"""Register our models on the dataclass"""
# Local Folder
from . import base_class, dcs

A = base_class.Base.registry.mapped(dcs.A)
B = base_class.Base.registry.mapped(dcs.B)
Base = base_class.Base

__all__ = ["A", "B", "Base"]
