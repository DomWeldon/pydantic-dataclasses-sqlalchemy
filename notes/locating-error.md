# Where is this error coming from?

Although the error is [raised inside a utility function](https://github.com/sqlalchemy/sqlalchemy/blob/rel_1_4_22/lib/sqlalchemy/util/compat.py#L207) it seems to be constructed [very early on inside `session.add()`](https://github.com/sqlalchemy/sqlalchemy/blob/fb81f9c8d914f9911925dd3f4e77d7fc374b267c/lib/sqlalchemy/orm/session.py#L2566), when SQLAlchemy tries to get the instance state of this newly created instance.

This implies that there should be something inside the `__init__()` method of the dataclass which constructs the instance state.

_Let's compare the init methods created by pydantic and the standard library._


The actual construction of the class appears to be [done inside `_process_class()` inside pydantic](https://github.com/samuelcolvin/pydantic/blob/master/pydantic/dataclasses.py#L109). It looks like there may be scope to manage inheritance using the `cls_` argument.

This seems similar to the [standard library implementation](https://github.com/python/cpython/blob/main/Lib/dataclasses.py#L1150).

## Differences between A and B

```python
>>> from pdsqla import models
>>> a_i = models.A(1, 2)
>>> b_i = models.B(1, 2)
>>> set(dir(a_i)) ^ set(dir(b_i))
{'__processed__', 'b', 'a', '__pydantic_model__', 'b_id', '__post_init__', '__get_validators__', '__initialised__', '_sa_instance_state', '__validate__', 'a_id'}
```

When initialised, B has an attribute `__initialised__` and `__validate__`, which A lacks. A however has a `_sa_instance_state`, which is the cause of this bug.

[These are caused by the `__post_init__()` method attached by pydantic](https://github.com/samuelcolvin/pydantic/blob/master/pydantic/dataclasses.py#L129).

Does SQLAlchemy also use the `__post_init__()` hook?

A search of the repo seems to suggest it doesn't...

There appears to be [a caveat in the dataclass processing logic inside SQLA](https://github.com/sqlalchemy/sqlalchemy/blob/ac0c1aed2b3521393e054fde07f5c6c75153bc50/lib/sqlalchemy/orm/decl_base.py#L362).


## Pydantic assumes it has access to `__dict__` on a model and can change it as required.

https://github.com/samuelcolvin/pydantic/blob/4a54f393ad20ee91b51cd7a49ec46771ba4f8a18/pydantic/dataclasses.py#L101

How does this mess up? `sqlalchemy.orm.instrumentation` and can I use `sqlalchemy.ext.instrumentation` to override it somehow?
