from flask import Flask, request, jsonify
import psycopg2
import json
import db.db_utils as db_utils
import datetime

app = Flask(__name__)

# ==================================================
# - - - - - - - - - - - - - - - - - - - - - - - -
@app.route('/')
def hello_world():
    return "Hello, World!"
# - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - PEGAR TODOS OS LIVRO / PEGAR TODOS OS LIVROS COM "x" GÊNERO
@app.route("/livro", methods=["GET"])
def get_books():
    books = None

    if ("genero" in request.args):
        genre = request.args.get("genero")
        books = db_utils.select("livros", ["*"], condition=f"genero = '{genre}'")
    else: 
        books = db_utils.select("livros", ["*"])

    return {"status": "success", "books": books}
# - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - ADICIONAR NOVO LIVRO
@app.route("/livro", methods=["POST"])
def add_book():
    req_data = request.get_json() 

    book_keys = {"titulo": str, "autor": str, "anoPublicacao": int, "genero": str}
    for k in book_keys:
        if (k not in req_data):
            return jsonify({"message": "Faltando informações"})
        
        if (not isinstance(req_data[k], book_keys[k])):
            return jsonify({"message": k + " do tipo invalido"})

        if (req_data[k] == ""):
            return jsonify({"message": k + " invalido"})

    check_exists = db_utils.select("livros", ["id"], f"Titulo = '{req_data['titulo']}'")

    if (len(check_exists) > 0):
        return {"status": "error", "message": "Livro já adicionado ao banco de dados."}

    db_utils.insert(
        "livros", 
        ["titulo", "autor", "anoPublicacao", "genero"], 
        [req_data["titulo"], req_data["autor"], req_data["anoPublicacao"], req_data["genero"]]
    )

    return {"status": "success", "message": "Livro adicionado com sucesso"}
# - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - SELECIONAR LIVRO PELO ID
@app.route("/livro/<int:book_id>", methods=["GET"])
def get_book_by_id(book_id):

    query = db_utils.select("Livros", ["*"], f"ID = {book_id}") 

    if (len(query) == 0):
        return {"status": "error", "message": f"Não foi possível encontrar o livro com id = {book_id}"}

    return {"status": "success", "book": query[0]}
# - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - DELETAR LIVRO PELO ID
@app.route("/livro/<int:book_id>", methods=["DELETE"])
def delete_book_by_id(book_id):
    check_exists = db_utils.select("livros", ["id"], f"ID = {book_id}")

    if (len(check_exists) == 0):
        return {"status": "error", "message": f"Não foi possível encontrar o livro com id = {book_id}."}

    db_utils.delete_by_id("Livros", book_id)

    return {"status": "success", "message": f"Livro com id = {book_id} excluído com succeso."}
# - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - ADICIONAR NOVO USUÁRIO
@app.route("/usuario", methods=["POST"])
def add_user():
    req_data = request.get_json() 

    book_keys = {"nome": str, "email": str}
    for k in book_keys:
        if (k not in req_data):
            return jsonify({"message": "Faltando informações"})
        
        if (not isinstance(req_data[k], book_keys[k])):
            return jsonify({"message": k + " do tipo invalido"})

        if (req_data[k] == ""):
            return jsonify({"message": k + " invalido"})

    check_exists = db_utils.select("usuarios", ["id"], f"email = '{req_data['email']}'")

    if (len(check_exists) > 0):
        return {"status": "error", "message": "Usuário já adicionado ao banco de dados."}

    db_utils.insert(
        "usuarios", 
        ["nome", "email", "dataCadastro"], 
        [req_data["nome"], req_data["email"], datetime.datetime.now()]
    )

    return {"status": "success", "message": "Usuário adicionado com sucesso."}
# - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - SELECIONAR TODOS USUÁRIOS
@app.route("/usuario", methods=["GET"])
def get_users():
    users = db_utils.select("usuarios", ["*"])

    return {"status": "success", "users": users}
# - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - SELECIONAR USUÁRIO PELO ID
@app.route("/usuario/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    query = db_utils.select("usuarios", ["*"], f"ID = {user_id}") 

    if (len(query) == 0):
        return {"status": "error", "message": f"Não foi possível encontrar o usuário com id = {user_id}"}

    return {"status": "success", "user": query[0]}
# - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - EXCLUIR USUÁRIO PELO ID
@app.route("/usuario/<int:user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    check_exists = db_utils.select("usuarios", ["id"], f"ID = {user_id}")

    if (len(check_exists) == 0):
        return {"status": "error", "message": f"Não foi possível encontrar o usuário com id = {user_id}."}

    db_utils.delete_by_id("Usuarios", user_id)

    return {"status": "success", "message": f"Usuário com id = {user_id} excluído com succeso."}
# - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == '__main__':
    app.run(debug=True, port=5500)
