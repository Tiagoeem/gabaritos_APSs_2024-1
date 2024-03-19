-- referencia: https://www.tutorialspoint.com/postgresql/postgresql_using_autoincrement.htm
CREATE TABLE IF NOT EXISTS usuarios (
    ID SERIAL PRIMARY KEY,
    Nome TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    DataCadastro TEXT NOT NULL
);
