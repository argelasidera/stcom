from flask_seeder import Seeder
from app.models import Permission, Role


class AddPermissions(Seeder):
    def __init__(self, db=None):
        super().__init__(db)
        self.priority = 1

    def run(self):
        permissions = Permission.query.all()

        if not permissions:
            raw_permissions = [
                # Role CRUD
                Permission('Add Role'),
                Permission('Edit Role'),
                Permission('Delete Role'),
                Permission('View Role'),
                # User CRUD
                Permission('Add User'),
                Permission('Edit User'),
                Permission('Delete User'),
                Permission('View User'),
                # Category CRUD
                Permission('Add Category'),
                Permission('Edit Category'),
                Permission('Delete Category'),
                Permission('View Category'),
            ]

            self.db.session.add_all(raw_permissions)

            permissions = Permission.query.all()

            admin_role = Role('Super Admin')

            for permission in permissions:
                admin_role.permissions.append(permission)
                self.db.session.add(admin_role)
