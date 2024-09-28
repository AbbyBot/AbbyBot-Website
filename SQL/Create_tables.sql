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
  `commentary` TEXT NOT NULL,
  `user_image` VARCHAR(255) NOT NULL,
  `custom_nickname` VARCHAR(255) NOT NULL, -- Custom nickname like "Pull Request King, Legendary programmer, etc."
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS contributions (
  `id` INT NOT NULL AUTO_INCREMENT,
  `contributor_id` INT NOT NULL, -- Relationship with the contributors table
  `contribution` TEXT NOT NULL, -- Each individual contribution
  PRIMARY KEY (`id`),
  FOREIGN KEY (`contributor_id`) REFERENCES contributors(`id`) ON DELETE CASCADE
);

CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
