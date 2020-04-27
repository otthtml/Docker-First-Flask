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
# Não ordenar as respostas de forma alfabética
application.config["JSON_SORT_KEYS"] =  False


def connDB():
    """
    se a origem for a produção (app.linnks), usar o BD produção
    caso contrário, usar o BD teste (app2.linnks)
    """
    origem = str(request.headers.get("origin"))
    referer = str(request.headers.get("referer"))
    if origem.find("app.linnks") != -1 or referer.find("app.linnks") != -1: # PRODUÇÃO
        db_url = "postgresql://postgres:l1nnk$$tecnolog1a$022430#2020*!@postgresql.linnks.com.br/dblinked"
    elif origem.find("app2.linnks") != -1 or referer.find("app2.linnks") != -1: # AMBIENTE DE TESTE
        db_url = "postgresql://postgres:l1nnk$$tecnolog1a$022430#2020*!@postgresteste.linnks.com.br/dblinked"
    else:
        return jsonify({"error": True,
        "mensagem": "Origem inválida."})

    engine = create_engine(db_url)
    db = scoped_session(sessionmaker(bind=engine))
    return db

# Decorator que modifica a função interna (decorated).
def token_required(f):
    # Encapsulamento da função f
    @wraps(f)
    def decorated(*args, **kwargs):
        db = connDB()
        token = ""
        token_db = ""
        try:
            token = str(request.headers.get("Authorization").split()[1])
            query_sql = "SELECT token FROM proof.auth_user WHERE token = :token"
            token_db = str(db.execute(query_sql, {"token": token}).fetchone())
            db.close()
        except:
            db.close()
            return jsonify({"error": True,
            "mensagem": "Token invalido."})

        if len(token_db) > 0:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": True,
            "mensagem": "Token nao encontrado."})
    return decorated


# O trecho abaixo ativa o servidor Flask e realiza a conexão
# com o link fornecido.
@application.route("/", methods=["GET"])
def index():
    return "Linnks Tecnologia COM DOCKER COMPOSE AGORA"

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
    application.run(host="0.0.0.0", port="8085", debug=True) 