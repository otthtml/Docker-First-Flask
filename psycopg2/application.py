# coding: utf-8
### Importação bibliotecas ###
import psycopg2
import os

from flask import Flask, jsonify, request, Response
from functools import wraps
from flask_cors import CORS

### Variaveis de ambiente ###
dbname = os.getenv("DBNAME")
user = os.getenv("USER")
pwd = os.getenv("PWD")
host = os.getenv("HOST")
port = os.getenv("PORT")

### Define uma variavel como o principal API do Flask ###
application = Flask(__name__)

### Inclui a segurança com CORS ###
CORS(application)

### Conexão ao servidor e ao banco de dado ###
def connDb():
    """Descomentar somente a linha que interessa para teste. Para produçao, usar somente as variaveis de ambiente para AWS"""

    #conn = psycopg2.connect(f"dbname = {dbname} user = {user} password = {pwd} host = {host} port = {port}") # Produção AWS
    #conn = psycopg2.connect("dbname = dblinked user = usr_sheet password = linnks!@#$ host = postgresql.linnks.com.br port = 5432") #Produção local
    conn = psycopg2.connect("dbname = dblinked user = postgres password = l1nnk$$tecnolog1a$022430#2020*! host = postgresteste.linnks.com.br port = 5432") #Banco teste
    conn.autocommit = True
    return conn.cursor()

### Token ###
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        db = connDb()
        try:
            token = str(request.headers.get("Authorization").split()[1])

        except:
            return jsonify({"error": True, "mensagem": "Token inválido"})
            
        query_sql = "SELECT token FROM proof.auth_user WHERE token = %s"
        db.execute(query_sql, (token, ))
        token_db = db.fetchone()
        db.close()
        if token_db:
            return f(*args, **kwargs)

        else:
            return jsonify({"error": True, "mensagem": "Token inválido"})

        db.close()

    return decorated

### Index route ###
@application.route('/')
def index():
    return jsonify("Coucou les biloutes !")

### Route com POST para chamar uma funçao com retorno usando header###
@application.route('/route/post', methods=['POST'])
@token_required
def routePost():
    db = connDb()
    try:
        #Se passar alguma coisa no header como arguemento
        argumento = request.headers.get("argumento")
        #Pode retornar uma unçao aqui. Nesse exemplo, eu retorno somente o argumento no formato que o Angular lê
        db.close()
        return jsonify({"error": False, "mensagem": argumento})

    except:
        #Se nao passar nada, retorno um erro
        db.close()
        return jsonify({"error": True, "mensagem": "Você tem que passar um argumento no header."})

### Route com GET para baixar um arquivo or exemplo###
@application.route('/route/get', methods=['GET'])
@token_required
def routeGet():
    with open("exemplo.txt", "w") as f:
        f.write("Um arquivo para exemplo.")

    with open("exemplo.txt", "rb") as f:
        data = f.read()

    return Response(data, headers={'Content-Type': 'text/plain', 'Content-Disposition': 'attachment; filename=exemplo.txt;'})

### Roda Flask ###
if __name__ == '__main__':
    #Para produçao, tirar o argumento debug
    application.run(host="0.0.0.0", port="8085", debug=True)