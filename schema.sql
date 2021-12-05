CREATE TABLE users(
    userId SERIAL NOT NULL PRIMARY KEY,
    username VARCHAR,
    password VARCHAR,
    creation_date DATE
);

CREATE TABLE songs(
    songId INT PRIMARY KEY,
    userId INT REFERENCES users(userId),
    filename VARCHAR,
    classification VARCHAR,
    confidence FLOAT,
    date DATE
);