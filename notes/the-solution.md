I think I need to have a way to alter a pydantic dataclass such that its instrumentation is managed using a custom InstrumentationManager. This class should accommodate the behaviour of pydantic to ensure that a moidel is intrumented.


A class _cannot_ be both a sqlalchemy model and a pydantic base. That would be mad and not useful. However, a pydantic dataclass should also be able to behave as a sqlalchemy model because that is the purpose of a dataclass, it should be unobtrusive and allow extensibiliy.

So, what is clashing in the implementation of SQLAlchemy and pydantic's handling of dataclasses which is causing the issue where instrumentation is messed up by SQLAlchemy.

I _think_ it's this line in pydantic.

https://github.com/samuelcolvin/pydantic/blob/4a54f393ad20ee91b51cd7a49ec46771ba4f8a18/pydantic/dataclasses.py#L101

I argue that pydantic should respect the nature of a dataclass and not prevent it being used in other ways as another class.
