from flask_login import current_user
from flask_admin.contrib.sqla import ModelView


class Admin_View(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and (
                                            current_user.user_role == 'admin')
