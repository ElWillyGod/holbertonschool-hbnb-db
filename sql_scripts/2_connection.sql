USE mysql;

CREATE USER IF NOT EXISTS 'access_level_1'@'localhost'
    IDENTIFIED BY 'f0791818058149d4A1e4f8baf639609e';
GRANT SELECT ON hbnb.*
    TO 'access_level_1'@'localhost';

CREATE USER IF NOT EXISTS 'access_level_2'@'localhost'
    IDENTIFIED BY 'a4432dCac51446219c3878363a82ab4b';
GRANT SELECT ON hbnb.*
    TO 'access_level_2'@'localhost';
GRANT INSERT, UPDATE, DELETE ON hbnb.places
    TO 'access_level_2'@'localhost';
GRANT INSERT, UPDATE, DELETE ON hbnb.reviews
    TO 'access_level_2'@'localhost';

CREATE USER IF NOT EXISTS 'access_level_3'@'localhost'
    IDENTIFIED BY '10c39a28f93d4384aDe3f632d95281ea';
GRANT SELECT, INSERT, UPDATE, DELETE ON hbnb.*
    TO 'access_level_3'@'localhost';

-- UPDATE user SET plugin='auth_socket' WHERE User='access_level_1';

FLUSH PRIVILEGES;