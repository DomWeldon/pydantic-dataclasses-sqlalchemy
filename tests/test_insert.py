# Third Party Libraries
import pytest
import sqlalchemy.orm as orm
from pdsqla import models


@pytest.mark.parametrize(
    "model,data",
    [
        (getattr(models, l), {f"{l.lower()}_id": 1, l.lower(): l})
        for l in "ABCD"
    ],
)
def test_insert(model, data, session: orm.Session):
    # arrange
    instance = model(**data)

    # act
    session.add(instance)
    session.commit()

    # assert
    assert instance is not None
    assert instance._sa_instance_state is not None
