import unittest
import os
import sqlalchemy

from app import app, db
from models import Usuarios
from helpers import *


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cadastro_login_test.db"))
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_database(self):
        """
        Verifica existência do db
        """
        test = os.path.exists('cadastro_login_test.db')
        self.assertTrue(test)

    def test_criar_usuario(self):
        """
            Insere usuário e verifica se:
            1- Existe um dado a mais na tabela de usuários
            2- Se os dados do usuário do banco batem com os usados para a criação dele
        """
        qtd_usuarios = len(Usuarios.query.all())

        usuario = Usuarios(
            nome = "Michael Gary Scott",
            email = "michael@email.com",
            cpf = "19325084066",
            pis = "86525397822",
            senha = "1234",
            pais = "Brasil",
            estado = "SP",
            municipio = "São Paulo",
            cep = "04334080",
            rua = "Rua Alberto Hertzer",
            numero = 18,
            complemento = "apto 101"        
        )

        db.session.add(usuario)
        db.session.commit()

        nova_qtd_usuarios = len(Usuarios.query.all())
        
        assert nova_qtd_usuarios == (qtd_usuarios + 1)

        usuario_db = Usuarios.query.filter_by(email="michael@email.com").first()

        assert usuario_db.nome == "Michael Gary Scott"
        assert usuario_db.email == "michael@email.com"
        assert usuario_db.cpf == "19325084066"
        assert usuario_db.pis == "86525397822"
        assert usuario_db.senha == "1234"
        assert usuario_db.pais == "Brasil"
        assert usuario_db.estado == "SP"
        assert usuario_db.municipio == "São Paulo"
        assert usuario_db.cep == "04334080"
        assert usuario_db.rua == "Rua Alberto Hertzer"
        assert usuario_db.numero == 18
        assert usuario_db.complemento == "apto 101"

    
    def test_editar_usuario(self):
        """
            Testa se o usuário foi editado corretamente
        """
        usuario = Usuarios(
            nome = "Michael Gary Scott",
            email = "michael@email.com",
            cpf = "19325084066",
            pis = "86525397822",
            senha = "1234",
            pais = "Brasil",
            estado = "SP",
            municipio = "São Paulo",
            cep = "04334080",
            rua = "Rua Alberto Hertzer",
            numero = 18,
            complemento = "apto 101"        
        )

        db.session.add(usuario)
        db.session.commit()

        usuario.nome = "Jim Halpert"
        usuario.email = "jim@email.com"
        usuario.cpf = "1234567890"
        usuario.pis = "123456789"
        usuario.senha = "4321"
        usuario.pais = "Brasil"
        usuario.estado = "MG"
        usuario.municipio = "Belo Horizonte"
        usuario.cep = "30660140"
        usuario.rua = "Rua Vicente Dutra"
        usuario.numero = 1139
        usuario.complemento = "casa 2"        
        
        db.session.commit()

        usuario_db = Usuarios.query.get(usuario.id)

        assert usuario_db.nome == "Jim Halpert"
        assert usuario_db.email == "jim@email.com"
        assert usuario_db.cpf == "1234567890"
        assert usuario_db.pis == "123456789"
        assert usuario_db.senha == "4321"
        assert usuario_db.pais == "Brasil"
        assert usuario_db.estado == "MG"
        assert usuario_db.municipio == "Belo Horizonte"
        assert usuario_db.cep == "30660140"
        assert usuario_db.rua == "Rua Vicente Dutra"
        assert usuario_db.numero == 1139
        assert usuario_db.complemento == "casa 2"        


    def test_usuario_duplicado(self):
        """
        Testa se inserir um usuário duplicado gera exceção
        """
        qtd_usuarios = len(Usuarios.query.all())

        usuario = Usuarios(
            nome = "Michael Gary Scott",
            email = "michael@email.com",
            cpf = "19325084066",
            pis = "86525397822",
            senha = "1234",
            pais = "Brasil",
            estado = "SP",
            municipio = "São Paulo",
            cep = "04334080",
            rua = "Rua Alberto Hertzer",
            numero = 18,
            complemento = "apto 101"        
        )

        db.session.add(usuario)
        db.session.commit()

        with self.assertRaises(Exception) as e:
            usuario_duplicado = Usuarios(
                nome = "Michael Gary Scott",
                email = "michael@email.com",
                cpf = "19325084066",
                pis = "86525397822",
                senha = "1234",
                pais = "Brasil",
                estado = "SP",
                municipio = "São Paulo",
                cep = "04334080",
                rua = "Rua Alberto Hertzer",
                numero = 18,
                complemento = "apto 101"        
            )

            db.session.add(usuario_duplicado)
            db.session.commit()

        # Exceção de duplicado
        self.assertEqual(sqlalchemy.exc.IntegrityError, type(e.exception))

        with self.assertRaises(Exception) as e:
            Usuarios.query.all()

        # Exceção de rollback faltando
        self.assertEqual(sqlalchemy.exc.PendingRollbackError, type(e.exception))
        
        db.session.rollback()

        # Testa se realmente apenas um usuário foi criado
        nova_qtd_usuarios = len(Usuarios.query.all())
        assert nova_qtd_usuarios == (qtd_usuarios + 1)


    #testando rotas
   

    def test_index(self):
        """
        Espera uma resposta de status_code 200, indicando que nossa requisição ocorreu com sucesso
        """
        test = app.test_client(self)
        response = test.get("/", content_type="html/text")
        self.assertEqual(response.status_code, 200)


    def test_404(self):
        """
        Faz uma requisição para uma rota inexistente na aplicação, gerando um erro 404
        """
        response = self.app.get("/contato")
        self.assertEqual(response.status, "404 NOT FOUND")


if __name__ == '__main__':
    unittest.main()
