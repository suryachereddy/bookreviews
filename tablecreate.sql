--ONLY FOR REFERENCE
CREATE TABLE books(
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);

ALTER TABLE books 
    ALTER COLUMN isbn TYPE VARCHAR;


CREATE TABLE users(
    userid SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    passhash VARCHAR NOT NULL
    
);

--aler unique username
ALTER TABLE users
ADD CONSTRAINT order_unique UNIQUE (username);


