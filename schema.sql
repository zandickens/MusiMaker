-- psql -f schema.sql -U Aidan psql postgresql://localhost/postgres/postgres

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
    top_classification VARCHAR,
    confidence FLOAT,
    blues FLOAT, 
    classical FLOAT, 
    country FLOAT, 
    disco FLOAT, 
    hiphop FLOAT,
    jazz FLOAT,
    metal FLOAT,
    pop FLOAT,
    reggae FLOAT,
    rock FLOAT,
    tempo FLOAT,
    length FLOAT,
    date DATETIME
);