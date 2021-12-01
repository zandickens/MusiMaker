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
    date DATE
);