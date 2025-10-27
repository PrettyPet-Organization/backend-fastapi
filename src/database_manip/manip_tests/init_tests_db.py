from sqlalchemy import insert

from core.models.base import Base
from core.models.user_models import (
    ProjectBase,
    ProjectRolesBase,
    ProjectRoleSkillsAssociation,
    RoleTypesBase,
    SkillsBase,
    UsersBase,
)

from .config import sync_session, sync_test_engine
from .raw_data.new_skill_role_assosiation import new_skill_role_connection
from .raw_data.projects_to_insert import new_projects
from .raw_data.role_types_to_insert import new_role_types
from .raw_data.roles_to_insert import new_roles
from .raw_data.skills_to_insert import new_skills_list
from .raw_data.users_to_insert import new_users_list


def init_databases():
    Base.metadata.drop_all(sync_test_engine)
    Base.metadata.create_all(sync_test_engine)

    with sync_session() as session:
        stmt1 = insert(UsersBase).values(new_users_list)
        stmt2 = insert(SkillsBase).values(new_skills_list)
        stmt3 = insert(RoleTypesBase).values(new_role_types)
        stmt4 = insert(ProjectBase).values(new_projects)
        stmt5 = insert(ProjectRolesBase).values(new_roles)
        stmt6 = insert(ProjectRoleSkillsAssociation).values(new_skill_role_connection)
        session.execute(stmt1)
        session.execute(stmt2)
        session.execute(stmt3)
        session.execute(stmt4)
        session.execute(stmt5)
        session.execute(stmt6)

        session.commit()
    print("Data has been renewed in the test database")


if __name__ == "__main__":
    init_databases()
