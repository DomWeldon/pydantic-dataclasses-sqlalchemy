# Third Party Libraries
import sqlalchemy as sa
import sqlalchemy.orm as orm


def test_db_connection(session: orm.Session):
    # arrange
    q = "SELECT 1;"

    # act
    res = session.execute(sa.text(q))
    one = res.scalar_one()

    # assert
    assert one == 1
