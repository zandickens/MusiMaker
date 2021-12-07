-- psql -f schema.sql -U Aidan postgresql://localhost/postgres

CREATE TABLE users(
    userId SERIAL NOT NULL PRIMARY KEY,
    username VARCHAR,
    password VARCHAR,
    creation_date DATE
);

CREATE TABLE songs(
    songId SERIAL NOT NULL PRIMARY KEY,
    username VARCHAR,
    userId INT REFERENCES users(userId),
    filename VARCHAR,
    classification VARCHAR,
    confidence FLOAT,
    date DATE
);