USE hbnb;

INSERT IGNORE INTO `users` (`email`, `first_name`, `id`, `is_admin`, `last_name`, `password`)
VALUES
('manuelantognazza@gmail.com', 'Wilson', '337b2b8483b94c37984531bc6d9f3f0b', 1, 'Antognazza', '$2b$16$TRopVnwem7uiy9Yv1p8RB.OYcWrAJYZdt7wtzBpHcJFf/UvUH9DK6'),
('matiasdavezac@gmail.com', 'Matias', '5d3a299561694fd88ff8916af047b4f6', 1, 'Davezac', '$2b$16$GTIzRsOB8pwaZfuvnEaFreKRQWQ7tyqUM9JSLFzAJpEhQ0.Yn5LWK'),
('alisonalvez05@gmail.com', 'Alison', 'c47d328c33334319811f4e40a9de0cfc', 1, 'Alvez', '$2b$16$tgZHRWnbXLN341TCY.iRbOvcpmG0nEqRAaCoAwSHeXCd0M9zk2dfW');