-- Things to consider:
-- Might be better to setup with flask sqlalchemy.
-- I don't know how or if it's a good idea at this point.

CREATE DATABASE IF NOT EXISTS hbnb;
USE hbnb;

-- COUNTRY
CREATE TABLE IF NOT EXISTS `countries` (
    `code` VARCHAR(2) PRIMARY KEY,
    `name` VARCHAR(128) NOT NULL
);

-- AMENITY
CREATE TABLE IF NOT EXISTS `amenities` (
    `id` VARCHAR(32) PRIMARY KEY,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    `name` VARCHAR(64) NOT NULL
);

-- USER
CREATE TABLE IF NOT EXISTS `users` (
    `id` VARCHAR(32) PRIMARY KEY,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    `email` VARCHAR(128) UNIQUE NOT NULL,
    `first_name` VARCHAR(64) NOT NULL,
    `last_name` VARCHAR(64) NOT NULL,
    `password` VARCHAR(256) NOT NULL,
    `is_admin` BOOLEAN NOT NULL DEFAULT FALSE
);

-- CITY
CREATE TABLE IF NOT EXISTS `cities` (
    `id` VARCHAR(32) PRIMARY KEY,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    `name` VARCHAR(128) NOT NULL,
    `country_code` VARCHAR(2) NOT NULL
);

-- PLACE
CREATE TABLE IF NOT EXISTS `places` (
    `id` VARCHAR(32) PRIMARY KEY,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    `name` VARCHAR(128) NOT NULL,
    `description` VARCHAR(1024) NOT NULL,
    `number_of_rooms` INT NOT NULL,
    `number_of_bathrooms` INT NOT NULL,
    `max_guests` INT NOT NULL,
    `latitude` FLOAT NOT NULL,
    `longitude` FLOAT NOT NULL,
    `price_per_night` FLOAT NOT NULL,
    `host_id` VARCHAR(32) NOT NULL,
    FOREIGN KEY (`host_id`) REFERENCES users(`id`),
    `city_id` VARCHAR(32) NOT NULL,
    FOREIGN KEY (`city_id`) REFERENCES cities(`id`)
);

-- REVIEW
CREATE TABLE IF NOT EXISTS `reviews` (
    `id` VARCHAR(32) PRIMARY KEY,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    `comment` VARCHAR(1024) NOT NULL,
    `user_id` VARCHAR(32) NOT NULL,
    FOREIGN KEY (`user_id`) REFERENCES users(`id`),
    `place_id` VARCHAR(32) NOT NULL,
    FOREIGN KEY (`place_id`) REFERENCES places(`id`)
);

-- RELATION TABLE FOR places AND amenities
CREATE TABLE IF NOT EXISTS `place_amenities` (
    `place_id` VARCHAR(32) NOT NULL,
    `amenity_id` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`place_id`, `amenity_id`),
    FOREIGN KEY (`place_id`) REFERENCES places(`id`),
    FOREIGN KEY (`amenity_id`) REFERENCES amenities(`id`)
);
