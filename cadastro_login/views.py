from flask import render_template, Response, request, redirect, session, flash, url_for
from flask.globals import current_app
from flask_login.utils import login_required, logout_user
from forms import LoginForm, Email
from models import Usuarios
from helpers import *
from flask_wtf import FlaskForm
from app import db, app


#LOGIN
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
            return render_template('logged.html')
        else:
            flash("Login inválido.")

    return render_template('login.html' ,
                            form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Nenhum usuário logado.")
    return redirect(url_for("index"))


@app.route("/logado")
def logado():
    return render_template("logged.html")
    

#CRUD

#CREATE
@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")  


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        cpf = request.form.get("cpf")
        pis = request.form.get("pis")
        senha = request.form.get("senha")
        pais = request.form.get("pais")
        estado = request.form.get("estado")
        municipio = request.form.get("municipio")
        cep = request.form.get("cep")
        rua = request.form.get("rua")
        numero = request.form.get("numero")
        complemento = request.form.get("complemento")

        if nome and email and cpf and pis and senha and pais and estado \
            and municipio and cep and rua and numero:

            usuario = Usuarios(nome, email, cpf, pis, senha, pais,
                                estado, municipio, cep, rua, numero,complemento)

            db.session.add(usuario)
            db.session.commit()
            login_user(usuario)

            flash("usuário cadastrado com sucesso!")
            return render_template("logged.html")

        else:
            flash("Erro")
            return render_template("cadastro.html")
            
    
# READ
@app.route("/lista")
def lista():
    usuarios = Usuarios.query.all()
    return render_template("lista.html", usuarios=usuarios)



# #UPDATE
@app.route("/edicao")
def edicao():
    return render_template("editar.html")  


@app.route("/editar/<int:id>", methods=["POST"])
def editar(id):
    usuario = Usuarios.query.filter_by(id=id).first()

    if not usuario:
        flash("Erro")
        return redirect(url_for("index"))

    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        cpf = request.form.get("cpf")
        pis = request.form.get("pis")
        senha = request.form.get("senha")
        pais = request.form.get("pais")
        estado = request.form.get("estado")
        municipio = request.form.get("municipio")
        cep = request.form.get("cep")
        rua = request.form.get("rua")
        numero = request.form.get("numero")
        complemento = request.form.get("complemento")

        if nome and email and cpf and pis and senha and pais and estado \
            and municipio and cep and rua and numero:

            usuario.nome = nome
            usuario.email = email
            usuario.cpf = cpf
            usuario.pis = pis
            usuario.senha = senha
            usuario.pais = pais
            usuario.estado = estado
            usuario.municipio = municipio
            usuario.cep = cep
            usuario.rua = rua
            usuario.numero = numero
            usuario.complemento = complemento

            db.session.commit()

            flash("Atualizações salvas com sucesso!")
            return redirect(url_for("logado", usuario=usuario, id=id))

    return render_template("editar.html",  usuario=usuario, id=id)


#DELETE
@app.route("/excluir/<int:id>")
def excluir(id):
    usuario = Usuarios.query.filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuário deletado com sucesso!")
    return redirect(url_for("index"))
