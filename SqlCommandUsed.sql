--ONLY FOR REFERENCE


--login validate
SELECT passhash FROM users WHERE username=:username
---isUserUnique
SELECT * FROM users WHERE username=:username
--insert new user
INSERT INTO users (username,passhash) values(:username,:passhash)