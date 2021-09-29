from flask_login import LoginManager, login_manager, login_user
from models import Usuarios
from app import app


lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(user_id):
    return Usuarios.query.get(user_id)
