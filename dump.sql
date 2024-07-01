CREATE DATABASE IF NOT EXISTS hbnb;
USE hbnb;
-- AMENITY
CREATE TABLE IF NOT EXISTS amenity (
    id VARCHAR(256) NOT NULL,
    created_at VARCHAR(256) NOT NULL,
    updated_at VARCHAR(256) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id),
    cname VARCHAR(256) NOT NULL
);
-- USER
CREATE TABLE IF NOT EXISTS user (
    id VARCHAR(256) NOT NULL,
    created_at VARCHAR(256) NOT NULL,
    updated_at VARCHAR(256) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id),
    first_name VARCHAR(256) NOT NULL,
    last_name VARCHAR(256) NOT NULL,
    email VARCHAR(256) NOT NULL,
    UNIQUE (email),
    password VARCHAR(256) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);
-- CITY
CREATE TABLE IF NOT EXISTS city (
    id VARCHAR(256) NOT NULL,
    created_at VARCHAR(256) NOT NULL,
    updated_at VARCHAR(256) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id),
    cname VARCHAR(256) NOT NULL,
    country_code VARCHAR(3) NOT NULL
);
-- PLACE
CREATE TABLE IF NOT EXISTS place (
    id VARCHAR(256) NOT NULL,
    created_at VARCHAR(256) NOT NULL,
    updated_at VARCHAR(256) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id),
    host_id VARCHAR(256) NOT NULL,
    FOREIGN KEY (host_id) REFERENCES user(id),
    city_id VARCHAR(256) NOT NULL,
    FOREIGN KEY (city_id) REFERENCES place(id),
    cname VARCHAR(256) NOT NULL,
    description VARCHAR(1024) NOT NULL,
    number_of_rooms INT NOT NULL,
    number_of_bathrooms INT NOT NULL,
    max_guests INT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    price_per_night FLOAT NOT NULL
);
-- REVIEW
CREATE TABLE IF NOT EXISTS review (
    id VARCHAR(256) NOT NULL,
    created_at VARCHAR(256) NOT NULL,
    updated_at VARCHAR(256) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id),
    user_id VARCHAR(256) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    place_id VARCHAR(256) NOT NULL,
    FOREIGN KEY (place_id) REFERENCES place(id),
    comment VARCHAR(1024) NOT NULL
);

-- UNION FOR place AND amenity
CREATE TABLE IF NOT EXISTS place_amenities (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    UNIQUE (id),
    place_id VARCHAR(256) NOT NULL,
    FOREIGN KEY (place_id) REFERENCES place(id),
    amenity_id VARCHAR(256) NOT NULL,
    FOREIGN KEY (amenity_id) REFERENCES amenity(id)
);
