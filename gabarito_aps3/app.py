from flask import Flask, request, jsonify
import psycopg2
import json
from db_utils import *

app = Flask("projeto_biblioteca")

#Altere para a sua conexão
conn = psycopg2.connect(
    dbname="dphiojng",
    user="dphiojng",
    password="6sN_BbyIMCnA2EhMrptXDlhhYBj5yGbL",
    host="silly.db.elephantsql.com"
)


############################
########## LIVROS ##########
############################

#Teste basico do flask em andamento
@app.route('/')
def hello_world():
    return {"Sucesso: ": "Web Service em execução"}, 200

#Printa livro pelo seu ID
@app.route('/livros/<int:id>', methods=['GET'])
def filtra_livro_id(id):
    try:
        cursor = conn.cursor()

        book = filter_table(cursor, 'livros', 'id', {id: '=',})
        if book == []:
            return {"Erro: ": 'Livro não encontrado'}, 404

        return book, 200
    
    except psycopg2.Error as e:
        conn.rollback()
        return {"Erro: ": e}, 500

#Apaga um livro a partir do ID
@app.route('/livros/<int:id>', methods=['DELETE'])
def apaga_livro(id):
    try:
        cursor = conn.cursor()

        book = filter_table(cursor, "livros", "id", {id: "="})
        if book == []:
            return {"Erro: ": 'Livro não encontrado'}, 404

        table_remove(cursor, 'livros', id)
        conn.commit()
        return {"Sucesso: ": f"Livro {book} apagado com sucesso"}, 200
    
    except psycopg2.Error as e:
        conn.rollback()
        return {"Erro: ": e}, 500
    
#Printa todos os livros e cadastra novos
@app.route('/livros', methods=['POST', 'GET'])
def cadastra_livro():
    try:
        cursor = conn.cursor()

        #Printa Livros
        if request.method == 'GET':
            genero = request.args.get('genero') #Permite filtragem com url parameters (/livros?genero="genero x")

            #Utiliza um if para interpertar o output dependendo da quarry
            if genero:
                table = filter_table(cursor, 'livros', 'Genero', {genero: '=',})
            else:
                table = print_table(cursor, 'livros')

            if table == []:
                return {"Erro:": 'Nenhum livro encontrado'}, 404

            #Esta etapa é OPCIONAL. Aqui eu crio uma response customizada, só faço isso para manter a ordem do json de retorno.
            #Pois se tentarmos retornar "table" ela vira fora de ordem, e se retornarmos json.dumps(table) o postman interpreta como HTML por algum motivo
            #Então utilizo esse código para especificar que se trata de um json ('application/json'). Totalmente opcional e estético
            response = app.response_class(
                response=json.dumps(table),
                status=200,
                mimetype='application/json'
            )

            return response #Poderia ser "return table, 200" sem problemas

        if request.method == 'POST':
            #Adiciona Livro
            request_data = request.json

            #O Livro deve ser um dicionario contendo um dicionario, para assim validar se o livro foi inserido. Segue exemplo de imput:
            # {
            # "Livro": {
            #     "Titulo": "Diario de um Banana",
            #     "Autor": "Aquele cara la",
            #     "AnoPublicacao": "2007",
            #     "Genero": "Comedia"
            #     }
            # }

            if 'Livro' not in request_data:
                return {"Erro:": 'Dados não puderam ser lidos, verifique as informações'}, 400
            
            #Cria a tupla de items
            livro_info = request_data.get('Livro')

            #Verifica se todas as informações passadas dentro de Livro existem na nossa tabela, para não receber infos faltando, nem excedentes.
            for field in livro_info:
                if column_exists(cursor, "livros", field) == False:
                    return {"Erro:": 'Campos invalidos fornecidos'}, 400


            titulo = livro_info.get('titulo', '')
            autor = livro_info.get('autor', '')
            ano_publicacao = livro_info.get('anopublicacao', '')
            genero = livro_info.get('genero', '')
            items = [(titulo, autor, ano_publicacao, genero),]

            added_item = add_to_table_unique(cursor, 'livros', ['Titulo', 'Autor', 'AnoPublicacao', 'Genero'], items)
            conn.commit()

            if added_item:
                return {"Sucesso: ": f'livro {titulo} adicionado com sucesso'}, 201
            else:
                return {"Erro: ": f'livro {titulo} ja existente'}, 400
            
    except psycopg2.Error as e:
        conn.rollback()
        return {"Erro: ": e}, 500
    

#Edita um livro a partir do ID
@app.route('/livros/<int:id>', methods=['PUT'])
def edita_livro(id):
    try:
        cursor = conn.cursor()
        request_data = request.json

        #Bloco que verifica se o JSon é valido
        book = filter_table(cursor, "livros", "id", {id: "="})
        if book == []:
            return {"Erro: ": 'Livro não existente'}, 400
        if 'Livro' not in request_data:
                return {"Erro:": 'Dados não puderam ser lidos, verifique as informações'}, 400
        

        #Bloco que edita a DB
        livro_info = request_data.get('Livro')
            #O Livro deve ser um dicionario contendo um dicionario. Segue exemplo de imput:
            # {
            # "Livro": {
            #     "Titulo": "Diario de um Banana",
            #     "Autor": "Aquele cara la",
            #     "AnoPublicacao": "2007",
            #     "Genero": "Comedia"
            #     }
            # }
            
            #Caso o usuario queira editar apenas um campo, ele pode enviar apenas os campos desejados dentro de Livro. O código só retornara erro caso o 
            #mesmo utilize um campo inexistente. A existencias dos campos é verificada por uma função
        
        #Edita campo a campo na DB o livro que teve o ID fornecido. Se nenhum ID for fornecido, muda a DB inteira.
        for field in livro_info:
            if column_exists(cursor, "livros", field):
                table_edit(conn, cursor, 'livros', field, livro_info.get(field, ''), id)
            else:
                return {"Erro: ": 'Coluna ou informação não existente foi passada'}, 400
        conn.commit()

        return {"Sucesso: ": f'Livro {book} editado com sucesso'}, 200
    
    except psycopg2.Error as e:
        conn.rollback()
        return {"Erro: ": e}, 500
    

##############################
########## USUARIOS ##########
##############################

@app.route('/usuarios', methods=['POST', 'GET'])
def cadastra_user():
    try:
        cursor = conn.cursor()

        if request.method == 'GET':
            #Printa Usuarios
            table = print_table(cursor, 'usuarios')

            if table == []:
                return {"Erro:": 'Nenhum usuario encontrado'}, 404

            #Esta etapa é OPCIONAL. Aqui eu crio uma response customizada, só faço isso para manter a ordem do json de retorno.
            #Pois se tentarmos retornar "table" ela vira fora de ordem, e se retornarmos json.dumps(table) o postman interpreta como HTML por algum motivo
            #Então utilizo esse código para especificar que se trata de um json ('application/json'). Totalmente opcional e estético
            response = app.response_class(
                response=json.dumps(table),
                status=200,
                mimetype='application/json'
            )

            return response #Poderia ser "return table, 200" sem problemas

        if request.method == 'POST':
            #Adiciona User
            request_data = request.json

            #O Usuario deve ser um dicionario contendo um dicionario. Segue exemplo de imput:
            # {
            #     "Usuario": {
            #         "nome": "João Pedro Paulo Sarti",
            #         "email": "teste@teste.com",
            #         "cpf": "123.456.789.-00"
            #     }
            # }

            if 'Usuario' not in request_data:
                return {"Erro:": 'Dados não puderam ser lidos, verifique as informações'}, 400
            
            #Verifica se todas as informações passadas dentro de Usuario existem.
            for field in request_data.get('Usuario'):
                if column_exists(cursor, "usuarios", field) == False:
                    return {"Erro:": 'Campos invalidos fornecidos'}, 400

            
            #Cria a tupla de items
            user_info = request_data.get('Usuario')
            nome = user_info.get('nome', '')
            email = user_info.get('email', '')
            data_ingresso = user_info.get('cpf', '')
            items = [(nome, email, data_ingresso)]
                
            #Adiciona item
            added_item = add_to_table_unique(cursor, 'usuarios', ['nome', 'email', 'cpf'], items)
            conn.commit()

            if added_item:
                return {"Sucesso: ": f'Usuario adicionado com sucesso'}, 201
            else:
                return {"Erro: ": f'Usuario ja existente'}, 400
            
    except psycopg2.Error as e:
        conn.rollback()
        return {"Erro: ": e}, 500
    

@app.route('/usuarios/<int:id>', methods=['GET'])
def filtra_user_id(id):
    try:
        cursor = conn.cursor()
        user = filter_table(cursor, 'usuarios', 'id', {id: '=',})
        if user == []:
            return {"Erro: ": 'Usuario não encontrado'}, 404
        return user, 200
    
    except psycopg2.Error as e:
        conn.rollback()
        return {"Erro: ": e}, 500

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def apaga_user(id):
    try:
        cursor = conn.cursor()
        usuario = filter_table(cursor, 'usuarios', 'id', {id: '='})
        if usuario == []:
            return {"Erro: ": 'Usuario não encontrado'}, 404

        table_remove(cursor, 'usuarios', id)
        conn.commit()
        return {"Sucesso: ": f"Usuario de ID {id} apagado com sucesso"}, 200
    
    except psycopg2.Error as e:
        conn.rollback()
        return {"Erro: ": e}, 500
    

#Edita um user a partir do ID
@app.route('/usuarios/<int:id>', methods=['PUT'])
def edita_user(id):
    try:
        cursor = conn.cursor()
        request_data = request.json
        #Bloco que verifica se o JSon é valido
        user = filter_table(cursor, "usuarios", "id", {id: "="})
        if user == []:
            return {"Erro: ": 'Usuario não encontrado'}, 404
        if 'Usuario' not in request_data:
            return {"Erro:": 'Dados não puderam ser lidos, verifique as informações'}, 400
        

        #Bloco que edita a DB
        user_info = request_data.get('Usuario')
            #O Usuario deve ser um dicionario contendo um dicionario. Segue exemplo de imput:
            # {
            #     "Usuario": {
            #         "Nome": "Ricardo Batista",
            #         "Email": "teste@teste.com",
            #         "cpf": "123.456.789.-00"
            #     }
            # }
            
            #Caso o usuario queira editar apenas um campo, ele pode enviar apenas os campos desejados dentro de Livro. O código só retornara erro caso o 
            # mesmo utilize um campo inexistente. A existencias dos campos é verificada por uma função
        
        #Edita campo a campo na DB o user que teve o ID fornecido. Se nenhum ID for fornecido, muda a DB inteira.
        for field in user_info:
            #Verifica se todas as colunas existem e edita caso existam
            if column_exists(cursor, "usuarios", field):

                #Verifica se o email(novo) e cpf(novo) ja existe e suspende as edições caso exista
                if field == 'Email':
                    email_existente = filter_table(cursor, 'usuarios', 'Email', {user_info[field]: "="})
                    if email_existente != []:
                        return {"Erro: ": 'O email fornecido ja existe, portanto as edições foram suspensas'}, 400
                    
                if field == 'cpf':
                    email_existente = filter_table(cursor, 'usuarios', 'cpf', {user_info[field]: "="})
                    if email_existente != []:
                        return {"Erro: ": 'O cpf fornecido ja existe, portanto as edições foram suspensas'}, 400

                #Segue as edições normalmente caso não ative o if ou o email seja novo
                table_edit(conn, cursor, 'usuarios', field, user_info.get(field, ''), id)
            else:
                return {"Erro: ": 'Coluna ou informação não existente foi passada'}, 400
        conn.commit()
        return {"Sucesso: ": f'Usuario de ID {id} editado com sucesso'}, 200
    
    except psycopg2.Error as e:
        conn.rollback()
        return {"Erro: ": e}, 500


##############################
######## flask_config ########
##############################

if __name__ == '__main__':
    app.run(debug=True)