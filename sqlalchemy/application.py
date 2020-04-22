# Este código contém os primeiros passos para executar código Python
# em uma integração com o Flask, o Banco de Dados da Linnks Tecnologia
# e o Angular.
# Autores: Octávio Telles, Renan Souza
# Data: 20/04/2020

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps


application = Flask(__name__)
CORS(application)
db_url = "postgresql://postgres:l1nnk$$tecnolog1a$022430#2020*!@postgresteste.linnks.com.br/dblinked"
engine = create_engine(db_url)
db = scoped_session(sessionmaker(bind=engine))

# Não ordenar as respostas de forma alfabética
application.config["JSON_SORT_KEYS"] =  False

# Decorator que modifica a função interna (decorated).
def token_required(f):
    # Encapsulamento da função f
    @wraps(f)
    def decorated(*args, **kwargs):
        token = ""
        token_db = ""
        try:
            token = str(request.headers.get("Authorization").split()[1])
            query_sql = "SELECT token FROM proof.auth_user WHERE token = :token"
            token_db = str(db.execute(query_sql, {"token": token}).fetchone())
            db.close()
        except:
            return jsonify({"mensagem": "erro",
            "erro": "Token invalido."})

        if len(token_db) > 0:
            return f(*args, **kwargs)
        else:
            return jsonify({"mensagem": "erro",
            "erro": "Token nao encontrado."})
    return decorated


# O trecho abaixo ativa o servidor Flask e realiza a conexão
# com o link fornecido.
@application.route("/", methods=["GET"])
def index():
    return "Linnks Tecnologia"

# O trecho abaixo ativa a função que utiliza o método GET
@application.route("/parametro/<int:numerinho>", methods = ["GET"])
def rotaComParametro(numerinho):
   """
   rotaComParametro é um exemplo de rota que usa parâmetro no endereço
   """
   return str(numerinho)

# O trecho abaixo ativa a função que utiliza o método POST
@application.route("/rotapost/", methods = ["POST"])
def rotaPost():
   """
   rotaPost é um exemplo de rota que aceita apenas requisições POST
   """
   requisicao = request.get_json()
   return jsonify(requisicao.get("test"))   

# O trecho abaixo ativa a função que faz a conexão com o Banco de Dados
@application.route("/rotaprotegida/", methods = ["POST"])
@token_required
def rotaProtegida():
   """
   rotaProtegida é um exemplo de rota que aceita apenas requisições POST
   """
   requisicao = request.get_json()
   return jsonify(requisicao.get("test"))

if (__name__ == "__main__"):
    application.run(host="127.0.0.1", port="8085", debug=True) 