DROP DATABASE IF EXISTS `raffle_db`;
CREATE DATABASE IF NOT EXISTS `raffle_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `raffle_db`;

DROP TABLE IF EXISTS company;
CREATE TABLE `company` (
    `company_id` VARCHAR(9) NOT NULL,
    `company_name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`company_id`)
);

INSERT INTO company VALUES
    ('GameStop',"443");

DROP TABLE IF EXISTS raffle_entry;
CREATE TABLE `raffle_entry` (
    `phone_number` VARCHAR(10) NOT NULL,
    `raffle_id` int(11) NOT NULL AUTO_INCREMENT,
    `product_id` VARCHAR(9) NOT NULL,
    `company_id` VARCHAR(9) NOT NULL,
    PRIMARY KEY (`raffle_id`, `phone_number`)
  )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO raffle_entry VALUES
    ('6596711823',1,2,443),
    ('6596723823',2,2,443),
    ('6598741823',3,2,443),
    ('6594921823',4,2,443),
    ('6596931823',5,2,443),
    ('6586833096',6,1,443),
    ('6596441823',7,1,443),
    ('6594722823',8,1,443),
    ('6596712223',9,3,443),
    ('6596741623',10,1,443),
    ('6591158048',11,1,443),
    ('6597861196',12,1,443),
    ('6586134493',13,1,443);



DROP TABLE IF EXISTS `raffle_company`;
CREATE TABLE `raffle_company` (
    `raffle_id` VARCHAR(9) NOT NULL,
    `product_id` VARCHAR(9) NOT NULL,
    `company_id` VARCHAR(9) NOT NULL,
    `product_desc` TEXT,
    `no_of_products` INT NOT NULL,
    `amount` FLOAT NOT NULL,
    `product_name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`raffle_id`, `company_id`)
);

INSERT INTO raffle_company VALUES
    (1,1,443,'The Xbox 360 is a home video game console developed by Microsoft. As the successor to the original Xbox, it is the second console in the Xbox series. It competed with Sony\'s PlayStation 3 and Nintendo\'s Wii as part of the seventh generation of video game consoles. It was officially unveiled on MTV on May 12, 2005, with detailed launch and game information announced later that month at the 2005 Electronic Entertainment Expo.',217,600,'XBOX'),
    (2,2,443,'The Witcher 3: Wild Hunt is an action role-playing game with a third-person perspective. Players control Geralt of Rivia, a monster slayer known as a Witcher. Geralt walks, runs, rolls and dodges, and (for the first time in the series) jumps, climbs and swims.',401,600,'Witcher 3'),
    (3,3,443,'The PlayStation 5 (PS5) is a home video game console developed by Sony Interactive Entertainment. ... Other features include the DualSense controller with haptic feedback and backward compatibility with most PlayStation 4 and PlayStation VR games.',163,598,'PS5');

DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
    `phone_number` VARCHAR(10) NOT NULL,
    `raffle_id` VARCHAR(9) NOT NULL,
    `amount` FLOAT NOT NULL,
    `product_id` VARCHAR(9) NOT NULL,
    `company_id` VARCHAR(9) NOT NULL,
    `product_desc` VARCHAR(255) NOT NULL,
    `product_name` VARCHAR(255) NOT NULL,
    `paid` VARCHAR(10) NOT NULL,
    PRIMARY KEY(`raffle_id`)
);

INSERT INTO transactions VALUES
    ('6596711823',1,598,1,443,
    'The PlayStation 5 (PS5) is a home video game console developed by Sony Interactive Entertainment. ... Other features include the DualSense controller with haptic feedback and backward compatibility with most PlayStation 4 and PlayStation VR games.', 'PS4', 'unpaid'),
    ('6596723823',2,598,2,443,
    'The Witcher 3: Wild Hunt is an action role-playing game with a third-person perspective. Players control Geralt of Rivia, a monster slayer known as a Witcher. Geralt walks, runs, rolls and dodges, and (for the first time in the series) jumps, climbs and swims.', 'Witcher 3', 'unpaid'),
    ('6598741823',3,598, 2, 443, 'The Witcher 3: Wild Hunt is an action role-playing game with a third-person perspective. Players control Geralt of Rivia, a monster slayer known as a Witcher. Geralt walks, runs, rolls and dodges, and (for the first time in the series) jumps, climbs and swims.', 'Witcher 3', 'unpaid');


DROP TABLE IF EXISTS `location`;
CREATE TABLE `location` (
	`phone_number` VARCHAR(10) NOT NULL,
    `location_id` int(11) NOT NULL AUTO_INCREMENT,
    `product_id` VARCHAR(9) NOT NULL,
    `company_id` VARCHAR(9) NOT NULL,
    `lat` FLOAT NOT NULL,
    `lng` FLOAT NOT NULL,
    PRIMARY KEY(`location_id`)
);
INSERT INTO location VALUES
	('6586134493',1,2,443,1.30530,103.91501),
    ('6592345678',2,2,443,1.32114,103.90970),
    ('6582224333',3,2,443,1.3432,103.68266),
    ('6593334333',4,3,443,1.2907,103.7727);


DROP TABLE IF EXISTS `clients`;
CREATE TABLE `clients` (
    `username` VARCHAR(255) NOT NULL, 
    `password` VARCHAR(255) NOT NULL,
    `phone_number` VARCHAR(10) NOT NULL,
    PRIMARY KEY(`username`)
);

INSERT INTO clients VALUES
    ("GameStop", "$2b$12$GVJRhx/SoNFs4wOfnzrkCOseV.hjyLyN1ekygcPAH5bPrPN00Cjru", "6567667622");

DROP TABLE IF EXISTS `443_Company_Survey`;
CREATE TABLE `443_Company_Survey` (
    `phone_number` VARCHAR(10) NOT NULL,
    `product_id` VARCHAR(9) NOT NULL,
    `satisfaction` VARCHAR(255) NOT NULL,
    `wish_item` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`phone_number`, `product_id`)
);

INSERT INTO `443_Company_Survey` VALUES 
    ('6596711823', '1', "Very Satisfied", "Cloud Gaming Products"),
    ('6596723823', '2', "Not Satisfied", "Rare Collectables/Accessories"),
    ('6598741823', '1', "Average Satisfaction", "Cloud Gaming Products"),
    ('6594921823', '3', "Very Satisfied", "Rare Collectables/Accessories"),
    ('6596931823', '1', "Average Satisfaction", "Cloud Gaming Products"),
    ('6586833096', '2', "Not Satisfied", "Cloud Gaming Products"),
    ('6596441823', '1', "Average Satisfaction", "Rare Collectables/Accessories"),
    ('6594722823', '3', "Very Satisfied", "Cloud Gaming Products"),
    ('6596741623', '3', "Average Satisfaction", "Rare Collectables/Accessories");

