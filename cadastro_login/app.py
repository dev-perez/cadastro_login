import json
import os
from flask import Flask, render_template, Response, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_manager
from flask_login.utils import login_required, logout_user
from flask_wtf import FlaskForm
from forms import EditAccountForm, LoginForm, Email
# from flask_script import Manager



project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "cadastro_login.db"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'senha-secreta'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(user_id):
    return Usuarios.query.get(user_id)

@app.route("/logout")
def logout():
    logout_user()
    flash("Logout feito.")
    return redirect(url_for("index"))


class Usuarios(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    cpf = db.Column(db.String, unique=True)
    pis = db.Column(db.String, unique=True)
    senha = db.Column(db.String)

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

    def __init__(self, nome, email,cpf, pis, senha):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.pis = pis
        self.senha = senha

    def _repr__(self):
        return "<Usuário %r>" % self.nome

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "email": self.email,
                "cpf": self.cpf, "pis": self.pis, "senha": self.senha}


class Enderecos(db.Model):
    __tablename__ = "enderecos"

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    pais = db.Column(db.String)
    estado = db.Column(db.String)
    municipio = db.Column(db.String)
    cep = db.Column(db.String)
    rua = db.Column(db.String)
    numero = db.Column(db.String)
    complemento = db.Column(db.String)

    def __init__(self, pais, estado, municipio, cep, rua, numero, complemento, id_usuario):
        self.pais = pais
        self.estado = estado
        self.municipio = municipio
        self.cep = cep
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.id_usuario = id_usuario

    usuario = db.relationship('Usuarios', foreign_keys=id_usuario)

    def _repr__(self):
        return "<Endereço %r>" % self.id


    def to_json(self):
        return {"id": self.id,"id_usuario": self.id_usuario, "pais": self.pais,
                "estado": self.estado, "municipio": self.municipio, "cep": self.cep,
                                    "rua": self.rua, "complemento": self.complemento}


#CRUD

#Selecionar Tudo
@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    usuarios_objetos = Usuarios.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]
    return gera_response(200, "usuarios", usuarios_json, "ok")

#Selecionar Um
@app.route("/usuario/<id>", methods=["GET"])
def seleciona_usuario(id):
    usuario_objeto = Usuarios.query.filter_by(id= id).first()
    usuario_json = usuario_objeto.to_json()
    print(usuario_objeto)
    print(usuario_json)
    return gera_response(200, "usuario", usuario_json, "ok")


#Cadastrar
@app.route("/usuario", methods=["POST"])
def cria_usuario():
    body = request.get_json()

    #Validar se veio os parâmetros
    #Ou utilizar um try catch para gerar erro

    try:
        usuario = Usuarios(nome=body["nome"],
                           email=body["email"],
                           cpf=body["cpf"],
                           pis=body["pis"],
                           senha=body["senha"])
        db.session.add(usuario)
        db.session.commit()

        usuario = Usuarios.query.filter_by(email=usuario.email).first()

        endereco = Enderecos(pais=["pais"],
                             estado=["estado"],
                             municipio=["municipio"],
                             cep=["cep"],
                             rua=["rua"],
                             numero=["numero"],
                             complemento=["complemento"],
                             id_usuario=usuario.id)

        db.session.add(endereco)
        db.session.commit()

        return gera_response(201, "usuario", usuario.to_json(), "Criado com sucesso!")
    except Exception as e:
        print(e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrar" )


#Atualizar
@app.route("/usuario/editar/<id>", methods=["PUT", "POST", "GET"])
def atualiza_usuario(id):
    print("*"*50)
    print(id)
    usuario_objeto = Usuarios.query.get(id)
    print(request.method)

    print(request.get_json())
    body = request.get_json()
    print("-"*50)
    print(body)
    print(usuario_objeto)

    try:
        if("nome") in body:
            usuario_objeto.nome = body["nome"]
        if("email") in body:
            usuario_objeto.email = body["email"]

        print(usuario_objeto)

        db.session.add(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Atualizado com sucesso!")
    except Exception as e:
        print(e)
        return gera_response(400, "usuario", {}, "Erro ao atualizar" )


#Deletar

@app.route("/usuario/<id>", methods=["DELETE"])
def deleta_usuario(id):
    usuario_objeto = Usuarios.query.filter_by(id= id).first()

    try:
        db.session.delete(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Deletado com sucesso!")
    except Exception as e:
        print(e)
        return gera_response(400, "usuario", {}, "Erro ao deletar")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


# @app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuarios.query.filter(
            (Usuarios.email == form.username.data) |
            (Usuarios.cpf == form.username.data) |
            (Usuarios.pis == form.username.data)
            ).first()
        if usuario and usuario.senha == form.password.data:
            login_user(usuario)
            flash(usuario.nome + " logou com sucesso!")
            return render_template('index.html')
        else:
            flash("Login inválido.")

    return render_template('login.html' ,
                            form=form)
    

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.form:
        usuario = Usuarios(
            nome = request.form.get("nome"),
            email = request.form.get("email"),
            cpf = request.form.get("cpf"),
            pis = request.form.get("pis"),
            senha = request.form.get("senha")
        )

        db.session.add(usuario)
        db.session.commit()

        endereco = Enderecos(
            id_usuario = usuario.id ,
            pais = request.form.get("pais"),
            estado = request.form.get("estado"),
            municipio = request.form.get("municipio"),
            cep = request.form.get("cep"),
            rua = request.form.get("rua"),
            numero = request.form.get("numero"),
            complemento = request.form.get("complemento")
        )

        db.session.add(endereco)
        db.session.commit()

    return render_template("cadastro.html")


@app.route("/logged")
def logged():
    return render_template("logged.html")


@app.route("/editar", methods=["GET"])
@login_required
def editar():
    form = EditAccountForm()
    return render_template("editar.html", form=form)



if __name__ == '__main__':
    app.run(debug=True)
