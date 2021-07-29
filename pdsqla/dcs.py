# Standard Library
import dataclasses
import typing

# Third Party Libraries
import pydantic
import sqlalchemy as sa

# Local Folder
from . import constants


def _generate_pydantic_post_init(
    post_init_original: typing.Optional[typing.Callable[..., None]],
    post_init_post_parse: typing.Optional[typing.Callable[..., None]],
) -> typing.Callable[..., None]:
    def _pydantic_post_init(self: "Dataclass", *initvars: typing.Any) -> None:
        if post_init_original is not None:
            post_init_original(self, *initvars)

        if getattr(self, "__has_field_info_default__", False):
            # We need to remove `FieldInfo` values since they are not valid as input
            # It's ok to do that because they are obviously the default values!
            input_data = {
                k: v
                for k, v in self.__dict__.items()
                if not isinstance(v, FieldInfo)
            }
        else:
            input_data = self.__dict__
        d, _, validation_error = pydantic.main.validate_model(
            self.__pydantic_model__, input_data, cls=self.__class__
        )
        if validation_error:
            raise validation_error
        # object.__setattr__(self, '__dict__', d)
        self.__dict__.update(d)
        object.__setattr__(self, "__initialised__", True)
        if post_init_post_parse is not None:
            post_init_post_parse(self, *initvars)

    return _pydantic_post_init


# monkeypatch
pydantic.dataclasses._generate_pydantic_post_init = (
    _generate_pydantic_post_init
)


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


@add_sqla_properties
@pydantic.dataclasses.dataclass()
class D:
    """Let's try and fix it using this class."""

    d_id: int = dataclasses.field(
        metadata={
            constants.SA_DATACLASS_METADATA_KEY: sa.Column(
                sa.Integer, primary_key=True
            )
        }
    )
    d: str = dataclasses.field(
        metadata={constants.SA_DATACLASS_METADATA_KEY: sa.Column(sa.String)}
    )

    # @pydantic.root_validator
    # def keep_sqlalchemy_stuff(self, values)
