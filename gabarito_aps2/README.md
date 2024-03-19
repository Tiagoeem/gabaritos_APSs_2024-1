[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/GGVUwZHN)
# Exercício de Web Services (não REST, ainda...) com Flask e PostgreSQL

O objetivo deste exercício é criar um serviço web simples para gerenciar uma biblioteca. A aplicação terá a capacidade de cadastrar livros e usuários da biblioteca. A ideia é que os alunos explorem a criação de endpoints que interajam com um banco de dados PostgreSQL na nuvem (ElephantSQL), abrangendo as operações de CRUD (Create, Read, Update, Delete).

## Fonte de Informação

### Ajuda com a plataforma ElephantSQL

- Introdução e Configurações Iniciais: https://www.elephantsql.com/blog/databases-for-beginners-what-is-a-database-what-is-postgresql.html

- Conectando o pgAdmin ao seu server Elephant: https://www.elephantsql.com/docs/pgadmin.html

- Documentação oficial: https://www.elephantsql.com/docs/index.html

### Ajuda com pgAdmin

- Introdução ao pgAdmin: https://www.w3schools.com/postgresql/postgresql_pgadmin4.php

- Documentação oficial: https://www.pgadmin.org/docs/pgadmin4/8.3/index.html

### Ajuda com o Python utilizando a base PostgreSql (psycog2)

- Tutorial excelente sobre psycog2: https://www.tutorialspoint.com/postgresql/postgresql_python.htm

- Documentação oficial: https://www.psycopg.org/docs/

### Ajuda com Flask

- Intro: https://www.tutorialspoint.com/flask/flask_application.htm

- Recebendo JSON via requisição: https://stackabuse.com/how-to-get-and-parse-http-post-body-in-flask-json-and-form-data/

- Variáveis na URL (urls dinâmicas): https://www.geeksforgeeks.org/generating-dynamic-urls-in-flask/

- Query Parameters: https://stackabuse.com/get-request-query-parameters-with-flask/

- Documentação oficial: https://flask.palletsprojects.com/en/3.0.x/

### Ajuda com Postman

- Intro: https://learning.postman.com/docs/getting-started/first-steps/sending-the-first-request/

- Importando uma collection: https://learning.postman.com/docs/getting-started/importing-and-exporting/importing-data/


### Busque outras fontes

Fique a vontade para procurar vídeos no youtube caso ache necessário, muitas pessoas aprendem melhor com vídeos.

O ChatGPT usado corretamente pode se tornar um grande parceiro de aprendizado, e te ajudar com conceitos que talvez ainda não estejam tão claros para você, pergunte sobre as ferramentas, integrações e papel de cada um dos elementos presentes nesta tarefa, só não peça por código. Não tome o caminho mais fácil, isso irá te prejudicar mais do que você imagina.


## Requisitos:

1. **Estrutura de Pastas**:
    * app.py: Arquivo principal contendo sua aplicação Flask.
    
2. **Criação da Base de Dados**:
    * As tabelas serão criadas via SQL, executando script de criação na via interface web do ElephantSQL ou via pgAdmin.
    * Este script será executado apenas uma vez durante o projeto.

3. **Tabelas**:
    * **Livros**: ID (chave primária), Título, Autor, Ano de Publicação, Gênero.
    * **Usuários**: ID (chave primária), Nome, Email, Data de Cadastro.

4. **Endpoints**:
    * **GET** `/`: Deve retornar "Hello, World!".
    * **POST** `/livro`: Cadastro de um novo livro.
    * **GET** `/livro`: Lista todos os livros. Deve suportar um query param para filtrar livros por gênero.
    * **GET** `/livro/<int:id>`: Retorna detalhes de um livro específico pelo ID.
    * **DELETE** `/livro/<int:id>`: Exclui um livro pelo ID.
    * **POST** `/usuario`: Cadastro de um novo usuário.
    * **GET** `/usuario`: Lista todos os usuários.
    * **GET** `/usuario/<int:id>`: Retorna detalhes de um usuário específico pelo ID.
    * **DELETE** `/usuario/<int:id>`: Exclui um usuário pelo ID.

5. **Requisitos Adicionais**:
    * Ao cadastrar um novo livro ou usuário via POST, os dados devem ser enviados como JSON no corpo da requisição.
    * Ao listar livros, deve ser possível filtrar por gênero usando um query param. Exemplo de requisição com query param: `GET /livro?genero=Fantasia`. Esta requisição retornaria todos os livros do gênero "Fantasia".
    * Implemente tratamento de erros adequado para situações como tentar excluir um livro ou usuário que não existe.

6. **Testando e Completando a Collection no Postman**:
    * Dentro da pasta do projeto, você encontrará uma subpasta chamada `postman` que contém uma collection inicial para o Postman.
    * Para importar a collection:
        1. Abra o Postman.
        2. Clique em "File" > "Import".
        3. Navegue até a pasta `postman` do seu projeto e selecione o arquivo JSON da collection.
        4. Clique em "Open".
    * **ATENÇÃO**: É fundamental que você adicione TODOS os métodos e endpoints na collection do Postman. Completar esta collection é uma parte essencial do exercício e vale pontos. Certifique-se de que cada endpoint esteja funcionando corretamente e que as requisições estejam configuradas de forma adequada.
    * Após completar a collection:
        1. No Postman, clique com o botão direito na collection "Biblioteca".
        2. Selecione "Export".
        3. Escolha a versão do formato (recomendamos a versão 2.1).
        4. Clique em "Export" e salve o arquivo na pasta `postman` do projeto.
    * **Observação**: Não se preocupe se o arquivo exportado tiver o mesmo nome do arquivo original. Você pode sobrescrever o arquivo existente.
