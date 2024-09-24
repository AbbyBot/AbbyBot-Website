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
  `id` INT NOT NULL,
  `nickname` VARCHAR(255) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `contributions` TEXT NOT NULL,
  `comentary` TEXT NOT NULL,
  `user_image` VARCHAR(255) NOT NULL,
  `custom_nickname` VARCHAR(255) NOT NULL, -- Apodo generado por ti
  PRIMARY KEY (`id`)
);

INSERT INTO contributors (`id`, `nickname`, `username`, `contributions`, `comentary`, `user_image`, `custom_nickname`) 
VALUES 
(1, 'AstronautMarkus', 'astronautmarkus', 'Create AbbyBot Project, AbbyBot GitHub Organization, AbbyBot Discord Bot code, AbbyBot Concept, a few of front-end, AbbyBot-website', 
'AstronautMarkus has launched the AbbyBot project 🚀, building everything from scratch: GitHub organization, Discord bot code, and even the original concept. 🛠️✨ Their contribution is the spark that brought AbbyBot to life 🔥, and they have also done an incredible job on the front-end and website! 🌐 This creator knows no limits 🌟', 
'static/img/contributor/astronautmarkus.png', 'The Code Pioneer'),

(2, '✨Soledad✨', 'soledadlml', 'Create AbbyBot actual image, art style images', 
'✨Soledad✨ has brought AbbyBot to life visually with her amazing artwork 🎨! She created the iconic AbbyBot image and defined the artistic style of the project 🎉. Her contributions have given AbbyBot a face and personality that stands out in every way 🌟. A true artist with a vision that shines! ✨', 
'static/img/contributor/soledadlml.png', 'The Visionary Artist'),

(4, 'anzarkept', 'anzarkept', 'Create AbbyBot Dashboard, Contribute to AbbyBot-website, AbbyBot Dashboard themes system, Discord API implementer in the dashboard', 
'anzarkept has engineered the backbone of AbbyBot\'s functionality 🚀! From building the entire AbbyBot Dashboard to creating the dynamic themes system 🎨, their work has shaped the user experience. Not to mention, they expertly implemented the Discord API into the dashboard 🔧, making everything run smoothly. A technical wizard whose contributions are invaluable 🛠️!', 
'static/img/contributor/anzarkept.png', 'The Dashboard Architect');
