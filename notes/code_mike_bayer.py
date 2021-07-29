"""this is getting close but SQLAlchemy is still not instrumenting __init__ such
that it can intercept Pydantic's operations, in particular that list coming
in which it wants to convert to instrumented list.

this probably could be made to work with some more effort but it will
be quite hacky in the end, not really worth it unless there was
some explicit support in pydantic.

"""

# Standard Library
from typing import List, Optional

# Third Party Libraries
from pydantic import BaseModel, constr
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.engine.create import create_engine
from sqlalchemy.ext.instrumentation import InstrumentationManager
from sqlalchemy.orm import registry, relationship
from sqlalchemy.orm.attributes import (
    del_attribute,
    get_attribute,
    set_attribute,
)
from sqlalchemy.orm.instrumentation import is_instrumented
from sqlalchemy.orm.session import Session

reg = registry()


class MyClassState(InstrumentationManager):
    def install_state(self, class_, instance, state):
        object.__setattr__(instance, "_sa_custom_instrumentation", state)

    def manager_getter(self, class_):
        def get(cls):
            return cls._default_class_manager

        return get

    def state_getter(self, class_):
        def find(instance):
            return object.__getattribute__(
                instance, "_sa_custom_instrumentation"
            )

        return find


class PydanticAdapter(BaseModel):
    __slots__ = ("__weakref__", "_sa_custom_instrumentation")
    __sa_instrumentation_manager__ = MyClassState

    def __getattr__(self, key):
        if is_instrumented(self, key):
            return get_attribute(self, key)
        else:
            return super().__getattr__(self, key)

    def __setattr__(self, key, value):
        if is_instrumented(self, key):
            set_attribute(self, key, value)
        else:
            super().__setattr__(self, key, value)

    def __delattr__(self, key):
        if is_instrumented(self, key):
            del_attribute(self, key)
        else:
            super().__delattr__(key)


@reg.mapped
class CompanyModel(PydanticAdapter):

    __table__ = Table(
        "companies",
        reg.metadata,
        Column("id", Integer, primary_key=True, nullable=False),
        Column(
            "public_key", String(20), index=True, nullable=False, unique=True
        ),
        Column("name", String(63), unique=True),
    )

    id: Optional[int]
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]
    employees: "List[Employee]"

    __mapper_args__ = {"properties": {"employees": relationship("Employee")}}


@reg.mapped
class Employee(PydanticAdapter):
    __table__ = Table(
        "employees",
        reg.metadata,
        Column("id", Integer, primary_key=True, nullable=False),
        Column("company_id", ForeignKey("companies.id")),
        Column("name", String(63), unique=True),
    )
    id: Optional[int]
    name: constr(max_length=63)


CompanyModel.update_forward_refs()

reg.configure()

co_model = CompanyModel(
    public_key="foobar",
    name="Testing",
    domains=["example.com", "foobar.com"],
)
co_model.employees = []

print(co_model)
co_model.employees.append(Employee(name="spongebob"))

e = create_engine("sqlite://", echo=True)
reg.metadata.create_all(e)

s = Session(e)

s.add(co_model)
s.commit()
