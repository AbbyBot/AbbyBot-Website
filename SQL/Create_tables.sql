CREATE TABLE IF NOT EXISTS wishlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    discord_username VARCHAR(255),
    reason TEXT,
    how_learned TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);




CREATE TABLE IF NOT EXISTS contributors (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nickname` VARCHAR(255) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `comentary` TEXT NOT NULL,
  `user_image` VARCHAR(255) NOT NULL,
  `custom_nickname` VARCHAR(255) NOT NULL, -- Apodo generado por ti
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS contributions (
  `id` INT NOT NULL AUTO_INCREMENT,
  `contributor_id` INT NOT NULL, -- Relación con la tabla contributors
  `contribution` TEXT NOT NULL, -- Cada contribución individual
  PRIMARY KEY (`id`),
  FOREIGN KEY (`contributor_id`) REFERENCES contributors(`id`) ON DELETE CASCADE
);


INSERT INTO contributors (`nickname`, `username`, `comentary`, `user_image`, `custom_nickname`) 
VALUES 
('AstronautMarkus', 'astronautmarkus', 
 'AstronautMarkus has launched the AbbyBot project 🚀, building everything from scratch: GitHub organization, Discord bot code, and even the original concept. 🛠️✨ Their contribution is the spark that brought AbbyBot to life 🔥, and they have also done an incredible job on the front-end and website! 🌐 This creator knows no limits 🌟', 
 'static/img/contributor/astronautmarkus.png', 'The Code Pioneer'),

('✨Soledad✨', 'soledadlml', 
 '✨Soledad✨ has brought AbbyBot to life visually with her amazing artwork 🎨! She created the iconic AbbyBot image and defined the artistic style of the project 🎉. Her contributions have given AbbyBot a face and personality that stands out in every way 🌟. A true artist with a vision that shines! ✨', 
 'static/img/contributor/soledadlml.png', 'The Visionary Artist'),

('anzarkept', 'anzarkept', 
 'anzarkept has engineered the backbone of AbbyBot\'s functionality 🚀! From building the entire AbbyBot Dashboard to creating the dynamic themes system 🎨, their work has shaped the user experience. Not to mention, they expertly implemented the Discord API into the dashboard 🔧, making everything run smoothly. A technical wizard whose contributions are invaluable 🛠️!', 
 'static/img/contributor/anzarkept.png', 'The Dashboard Architect');



INSERT INTO contributions (`contributor_id`, `contribution`)
VALUES
-- Contribuciones de AstronautMarkus (contributor_id = 1)
(1, 'Create AbbyBot Project'),
(1, 'AbbyBot GitHub Organization'),
(1, 'AbbyBot Discord Bot code'),
(1, 'AbbyBot Concept'),
(1, 'A few of front-end'),
(1, 'AbbyBot-website'),

-- Contribuciones de ✨Soledad✨ (contributor_id = 2)
(2, 'Create AbbyBot actual image'),
(2, 'Art style images'),

-- Contribuciones de anzarkept (contributor_id = 3)
(3, 'Create AbbyBot Dashboard'),
(3, 'Contribute to AbbyBot-website'),
(3, 'AbbyBot Dashboard themes system'),
(3, 'Discord API implementer in the dashboard');
