-- referencia: https://www.tutorialspoint.com/postgresql/postgresql_using_autoincrement.htm
CREATE TABLE IF NOT EXISTS livros (
    ID SERIAL PRIMARY KEY,

    Titulo VARCHAR(255) NOT NULL,
    Autor VARCHAR(255) NOT NULL,
    AnoPublicacao INTEGER,
    Genero VARCHAR(255)
);