from flask_seeder import Seeder
from app.models.user import User


class AddAdmin(Seeder):
    # run() will be called by Flask-Seeder
    def run(self):
        admin_user = User(
            email='admin@email.com',
            name="Super Admin",
            password='123123'
        )

        user = User.query.filter_by(email=admin_user.email).first()

        if user is None:
          self.db.session.add(admin_user)


