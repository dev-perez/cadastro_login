from flask import render_template, Response, request, redirect, session, flash, url_for
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
        
        password =  criptografa_senha(form.password.data)
        if usuario and usuario.senha == password:
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
    try:
        if request.method == "POST":
            nome = limpa(request.form.get("nome"))
            email = request.form.get("email")
            cpf = limpa(request.form.get("cpf"))
            pis = limpa(request.form.get("pis"))
            senha = request.form.get("senha")
            pais = limpa(request.form.get("pais"))
            estado = limpa(request.form.get("estado"))
            municipio = limpa(request.form.get("cidade"))
            cep = limpa(request.form.get("cep"))
            rua = limpa(request.form.get("rua"))
            numero = limpa(request.form.get("numero"))
            complemento = limpa(request.form.get("complemento"))

            usuario = Usuarios(nome, email, cpf, pis, senha, pais,
                                estado, municipio, cep, rua, numero, complemento)

            # valida CPF e PIS
            cpf = CPF()
            pis = PIS()
            if cpf.validate(usuario.cpf) == False:
                flash("CPF inválido, digite novamente!")
                return render_template("cadastro.html")
            elif pis.validate(usuario.pis) == False:
                flash("PIS inválido, digite novamente!")
                return render_template("cadastro.html")

            # criptografa senha com md5
            usuario.senha = criptografa_senha(usuario.senha)

            db.session.add(usuario)
            db.session.commit()
            login_user(usuario)

            flash("usuário cadastrado com sucesso!")
            return render_template("logged.html")

    except Exception as e:
        db.session.rollback()
        flash(e)
        return render_template("cadastro.html")
    
# READ
@app.route("/lista")
def lista():
    usuarios = Usuarios.query.all()
    return render_template("lista.html", usuarios=usuarios)

#UPDATE
@app.route("/edicao")
def edicao():
    return render_template("editar.html")  

@app.route("/editar/<int:id>", methods=["POST"])
def editar(id):
    usuario = Usuarios.query.get(id)

    if not usuario:
        flash("Erro")
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            usuario.nome = limpa(request.form.get("nome"))
            usuario.email = request.form.get("email")
            usuario.cpf = limpa(request.form.get("cpf"))
            usuario.pis = limpa(request.form.get("pis"))
            usuario.pais = limpa(request.form.get("pais"))
            usuario.estado = limpa(request.form.get("estado"))
            usuario.municipio = limpa(request.form.get("municipio"))
            usuario.cep = limpa(request.form.get("cep"))
            usuario.rua = limpa(request.form.get("rua"))
            usuario.numero = limpa(request.form.get("numero"))
            usuario.complemento = limpa(request.form.get("complemento"))

            #valida CPF e PIS
            cpf = CPF()
            if cpf.validate(usuario.cpf) == False:
                flash("CPF inválido, digite novamente!")
                return redirect(url_for("edicao"))

            pis = PIS()
            if pis.validate(usuario.pis) == False:
                flash("PIS inválido, digite novamente!")
                return redirect(url_for("edicao"))

            db.session.commit()
            flash("Atualizações salvas com sucesso!")
            return redirect(url_for("logado", usuario=usuario, id=id))
        except Exception as e:
            db.session.rollback()
            flash(e)
            return redirect(url_for("edicao"))

    return redirect(url_for("edicao"))


@app.route("/editar-senha")
def editar_senha():
    return render_template("editar_senha.html")

@app.route("/edita-senha/<int:id>", methods=["POST"])
def edita_senha(id):
    usuario = Usuarios.query.get(id)
    if usuario:
        print(usuario)
        senha_atual = request.form.get("senha-atual")
        senha = request.form.get("senha")

        if senha and senha_atual:
            senha = criptografa_senha(senha)
            senha_atual = criptografa_senha(senha_atual)

            if usuario.senha == senha_atual:
                usuario.senha = senha
                db.session.commit()
            else:
                flash("Senha atual incorreta")
                return render_template("editar_senha.html")
        else:
            flash("É necessário preencher todos os campos")
            return render_template("editar_senha.html")

        flash("Senha alterada com sucesso!")
        return render_template("logged.html")
    else:
        flash("Não foi possível alterar a senha.")
        return render_template("editar_senha.html")
        


#DELETE
@app.route("/excluir/<int:id>")
def excluir(id):
    usuario = Usuarios.query.filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuário deletado com sucesso!")
    return redirect(url_for("index"))
