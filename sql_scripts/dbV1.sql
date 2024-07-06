-- Currently ignored

CREATE TABLE `users` (
  `id` varchar(255) UNIQUE PRIMARY KEY NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) UNIQUE NOT NULL,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `role` varchar(255),
  `created_at` datetime NOT NULL,
  `update_at` datetime NOT NULL
);

CREATE TABLE `review` (
  `id` varchar(255) PRIMARY KEY NOT NULL,
  `place_id` varchar(255) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `rating` int NOT NULL,
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
  `country_code` varchar(255),
  `created_at` datetime NOT NULL,
  `update_at` datetime NOT NULL,
  PRIMARY KEY (`id`, `country_code`)
);

CREATE TABLE `place` (
  `id` varchar(255) PRIMARY KEY NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `number_of_rooms` int NOT NULL,
  `number_of_bathrooms` int NOT NULL,
  `max_guest` int NOT NULL,
  `price_per_night` float NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `city_id` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `update_at` datetime NOT NULL
);

ALTER TABLE `review` ADD FOREIGN KEY (`place_id`) REFERENCES `place` (`id`);

ALTER TABLE `review` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `place` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `place` ADD FOREIGN KEY (`city_id`) REFERENCES `city` (`id`);

CREATE TABLE `amenity_place` (
  `amenity_id` varchar,
  `place_id` varchar,
  PRIMARY KEY (`amenity_id`, `place_id`)
);

ALTER TABLE `amenity_place` ADD FOREIGN KEY (`amenity_id`) REFERENCES `amenity` (`id`);

ALTER TABLE `amenity_place` ADD FOREIGN KEY (`place_id`) REFERENCES `place` (`id`);

