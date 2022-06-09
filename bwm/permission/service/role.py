from bwm.core.schema import load_schema
from bwm.core.service import Service
from bwm.model import permission
from bwm.permission.schema.role import AddRole
from bwm.type import Data


class RoleService(Service):
    model = permission.Role

    @load_schema(AddRole())
    def add_role(self, data: Data):
        role = self.model(**data)
        self.db.session.add(role)
        self.db.session.commit()
        return role
