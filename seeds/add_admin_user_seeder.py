from flask_seeder import Seeder
from app.models import User, Role


class AddAdmin(Seeder):
    def __init__(self, db=None):
        super().__init__(db)
        self.priority = 2

    def run(self):
        user = User.query.filter_by(email='admin@email.com').first()

        if user is None:
            admin_role = Role.query.filter_by(slug='super-admin').first()

            admin_user = User(
                email='admin@email.com',
                name="Super Admin",
                password='123123',
                role_id=admin_role.id
            )

            self.db.session.add(admin_user)
