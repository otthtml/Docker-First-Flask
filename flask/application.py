# Author: Octávio Telles
# Date: 20/04/2020

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps


application = Flask(__name__)
CORS(application)
application.config["JSON_SORT_KEYS"] =  False


def connDB():
    # function that initiates connection to DB, directing to the correct one.
    origin = str(request.headers.get("origin"))
    referer = str(request.headers.get("referer"))
    if origin.find("url-of-production") != -1 or referer.find("url-of-production") != -1: # PRODUCTION
        db_url = ""
    elif origin.find("url-of-test") != -1 or referer.find("url-of-test") != -1: # TEST
        db_url = ""
    elif origin.find("localhost") != -1 or referer.find("localhost") != -1: # LOCAL
        db_url = ""
    else:
        return jsonify({"error": True,
        "msg": "invalid origin."})

    engine = create_engine(db_url)
    db = scoped_session(sessionmaker(bind=engine))
    return db

# Decorator for token that blocks access.
def token_required(f):
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
            "msg": "invalid token."})

        if len(token_db) > 0:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": True,
            "msg": "token not found."})
    return decorated



@application.route("/", methods=["GET"])
def index():
    return "index route"

@application.route("/parameter/<int:some_number>", methods = ["GET"])
def parameterRoute(some_number):
   """
   parameterRoute returns the integer.
   """
   return str(some_number)

@application.route("/postroute/", methods = ["POST"])
def postRoute():
   """
   postRoute
   """
   requisicao = request.get_json()
   return jsonify(requisicao.get("test"))   


@application.route("/protectedroute/", methods = ["POST"])
@token_required
def protectedRoute():
   """
   protectedRoute uses token to limit access
   """
   requisicao = request.get_json()
   return jsonify(requisicao.get("test"))

if (__name__ == "__main__"):
    application.run(host="0.0.0.0", port="8085", debug=True) 