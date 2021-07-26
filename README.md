# Cannot use Pydantic Dataclasses with delcarative mapping in SQLAlchemy

## Some basics

```toml
python = "3.9.5"
pydantic = "1.8.2"
SQLAlchemy = "1.4.22"
```

## The problem

The popular python ORM SQLAlchemy allows [users to declare models as dataclasses using the declarative interface](https://docs.sqlalchemy.org/en/14/orm/mapping_styles.html#example-two-dataclasses-with-declarative-table).

Users should thus be able to write a dataclass and register it on their base as below.

```python

import dataclasses

import sqlalchemy as sa

# declarative base imported from elsewhere

@Base.registry.mapped
@dataclasses.dataclass()
class A:
    """A very simple model using stlib dataclasses."""
    # some required properties for SQLAlchemy
    __tablename__ = "a"
    __sa_dataclass_metadata_key__ = "sa"

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

```

This works just fine for a standard library dataclass, but a pydantic dataclass, define din just the same way, such as the class below, will fail when you try to instrument it (i.e., use it to manage your data).

```python
import pydantic

@Base.registry.mapped
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
```

Now try to use it.

```python

# construct your session etc.

b = B(b_id=1, b="I won't work.")
session.add(b)
```

Uh oh. A `sqlalchemy.orm.exc.UnmappedInstanceError` error is raised. The message complains that our class _"`pdsqla.dcs.B` is mapped, but this instance lacks instrumentation.  This occurs when the instance is created before sqlalchemy.orm.mapper(pdsqla.dcs.B) was called."_

The full error message is below.

```python
def raise_(
    exception, with_traceback=None, replace_context=None, from_=False
):
    r"""implement "raise" with cause support.

    :param exception: exception to raise
    :param with_traceback: will call exception.with_traceback()
    :param replace_context: an as-yet-unsupported feature.  This is
     an exception object which we are "replacing", e.g., it's our
     "cause" but we don't want it printed.    Basically just what
     ``__suppress_context__`` does but we don't want to suppress
     the enclosing context, if any.  So for now we make it the
     cause.
    :param from\_: the cause.  this actually sets the cause and doesn't
     hope to hide it someday.

    """
    if with_traceback is not None:
        exception = exception.with_traceback(with_traceback)

    if from_ is not False:
        exception.__cause__ = from_
    elif replace_context is not None:
        # no good solution here, we would like to have the exception
        # have only the context of replace_context.__context__ so that the
        # intermediary exception does not change, but we can't figure
        # that out.
        exception.__cause__ = replace_context

    try:
>           raise exception
E           sqlalchemy.orm.exc.UnmappedInstanceError: Class 'pdsqla.dcs.B' is mapped, but this instance lacks instrumentation.  This occurs when the instance is created before sqlalchemy.orm.mapper(pdsqla.dcs.B) was called.
```

## Can I test this?

You sure can. Run `make test` in this repository, or just see [the unit test inserting a row of B](/tests/test_insert.py#L11). This test will work for A (stdlib) but not B.

## What's going on?

This seems to suggest that something in the way pydantic dataclasses are constructed prevents the standard instrumentation for SQLAlchemy from working properly.

I intend to try and get to the bottom of this in this repository.
