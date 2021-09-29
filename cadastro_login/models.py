from app import db

class Usuarios(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    cpf = db.Column(db.String)
    pis = db.Column(db.String)
    senha = db.Column(db.String)
    pais = db.Column(db.String)
    estado = db.Column(db.String)
    municipio = db.Column(db.String)
    cep = db.Column(db.String)
    rua = db.Column(db.String)
    numero = db.Column(db.String)
    complemento = db.Column(db.String)

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
    