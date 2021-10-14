from app import db


class Usuarios(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    pis = db.Column(db.String(11), unique=True, nullable=False)
    senha = db.Column(db.String(32), nullable=False)
    pais = db.Column(db.String(15), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    municipio = db.Column(db.String(30), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    rua = db.Column(db.String(15), nullable=False)
    numero = db.Column(db.SmallInteger, nullable=False)
    complemento = db.Column(db.String(10), nullable=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, nome, email,cpf, pis, senha, pais, estado,
                        municipio, cep, rua, numero, complemento):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.pis = pis
        self.senha = senha
        self.pais = pais
        self.estado = estado
        self.municipio = municipio
        self.cep = cep
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
    