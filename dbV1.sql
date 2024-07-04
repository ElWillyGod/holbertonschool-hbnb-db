CREATE TABLE hbnb;

USE hbnb;

CREATE TABLE `users` (
  `id` varchar(255) UNIQUE PRIMARY KEY NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) UNIQUE NOT NULL,
  `firstName` varchar(255),
  `lastName` varchar(255),
  `role` varchar(255),
  `created_at` datetime NOT NULL,
  `update_at` datetime NOT NULL
);

CREATE TABLE `review` (
  `id` varchar(255) PRIMARY KEY NOT NULL,
  `placeId` varchar(255) NOT NULL,
  `userId` varchar(255) NOT NULL,
  `reating` int NOT NULL,
  `comment` varchar(255),
  `created_at` datetime NOT NULL,
  `update_at` datetime NOT NULL
);

CREATE TABLE `amenity` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255),
  `created_at` datetime NOT NULL,
  `update_at` datetime NOT NULL,
  PRIMARY KEY (`id`, `name`)
);

CREATE TABLE `city` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) UNIQUE,
  `countryCode` varchar(255),
  `created_at` datetime NOT NULL,
  `update_at` datetime NOT NULL,
  PRIMARY KEY (`id`, `countryCode`)
);

CREATE TABLE `place` (
  `id` varchar(255) PRIMARY KEY NOT NULL,
  `userId` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `numberOfRooms` int NOT NULL,
  `numberOfBathrooms` int NOT NULL,
  `maxGues` int NOT NULL,
  `pricePreNigth` float NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `cityId` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `update_at` datetime NOT NULL
);

ALTER TABLE `review` ADD FOREIGN KEY (`placeId`) REFERENCES `place` (`id`);

ALTER TABLE `review` ADD FOREIGN KEY (`userId`) REFERENCES `users` (`id`);

ALTER TABLE `place` ADD FOREIGN KEY (`userId`) REFERENCES `users` (`id`);

ALTER TABLE `place` ADD FOREIGN KEY (`cityId`) REFERENCES `city` (`id`);

CREATE TABLE `amenity_place` (
  `amenity_id` varchar,
  `place_id` varchar,
  PRIMARY KEY (`amenity_id`, `place_id`)
);

ALTER TABLE `amenity_place` ADD FOREIGN KEY (`amenity_id`) REFERENCES `amenity` (`id`);

ALTER TABLE `amenity_place` ADD FOREIGN KEY (`place_id`) REFERENCES `place` (`id`);


