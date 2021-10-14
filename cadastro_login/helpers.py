from flask.helpers import flash
from flask_login import LoginManager, login_manager, login_user
from models import Usuarios
from app import app
from validate_docbr import CPF, PIS
import hashlib


lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(user_id):
    return Usuarios.query.get(user_id)

def criptografa_senha(senha):
    return (hashlib.md5(senha.encode())).hexdigest()

# Remoção de caracteres especiais
def limpa(dado):
    caracteres = "\"'!@#$%&*()-_=+[]{},.;:/|\<>"
    for c in caracteres:
        dado = dado.replace(c, "")
    return dado
