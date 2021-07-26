# Standard Library
import dataclasses
import typing

# Third Party Libraries
import pydantic
import sqlalchemy as sa

# Local Folder
from . import constants


def add_sqla_properties(cls: typing.Type) -> typing.Type:
    """Add table name for SQL Alchemy"""
    cls.__tablename__ = cls.__name__.lower()
    cls.__sa_dataclass_metadata_key__ = constants.SA_DATACLASS_METADATA_KEY
    # cls.__table_args__ = (
    #     sa.PrimaryKeyConstraint(
    #         f"{cls.__name__.lower()}_id"
    #     ),
    # )

    return cls


@add_sqla_properties
@dataclasses.dataclass()
class A:
    """A very simple model using stlib dataclasses."""

    a_id: int = dataclasses.field(
        metadata={
            constants.SA_DATACLASS_METADATA_KEY: sa.Column(
                sa.Integer, primary_key=True
            )
        }
    )
    a: str = dataclasses.field(
        metadata={constants.SA_DATACLASS_METADATA_KEY: sa.Column(sa.String)}
    )


@add_sqla_properties
@pydantic.dataclasses.dataclass()
class B:
    """A very simple model using pydantic dataclasses."""

    b_id: int = dataclasses.field(
        metadata={
            constants.SA_DATACLASS_METADATA_KEY: sa.Column(
                sa.Integer, primary_key=True
            )
        }
    )
    b: str = dataclasses.field(
        metadata={constants.SA_DATACLASS_METADATA_KEY: sa.Column(sa.String)}
    )
