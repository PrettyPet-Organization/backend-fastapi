from sqlalchemy.dialects.postgresql import insert

from core.models.base import Base
from core.models.user_models import RolesBase

from .config import sync_session, sync_test_engine
from .raw_data.new_roles import new_roles_list


def init_databases():

    with sync_session() as session:
        stmt1 = (
            insert(RolesBase)
            .values(new_roles_list)
            .on_conflict_do_nothing(index_elements=["id"])
        )

        session.execute(stmt1)
        session.commit()


if __name__ == "__main__":
    init_databases()
