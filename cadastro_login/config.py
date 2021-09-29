import os


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "cadastro_login.db"))


SECRET_KEY = 'senha-secreta'
SQLALCHEMY_DATABASE_URI = database_file
SQLALCHEMY_TRACK_MODIFICATIONS = True
