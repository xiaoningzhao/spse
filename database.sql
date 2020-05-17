DROP DATABASE IF EXISTS spse;
CREATE DATABASE spse;
USE spse;

CREATE TABLE `user` (
    user_id INTEGER NOT NULL AUTO_INCREMENT,
    password VARCHAR(50) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE portfolio (
	user_id INTEGER,
    ticker VARCHAR(50) NOT NULL,
    ticker_name VARCHAR(255),
    share DOUBLE,
    purchase_price DOUBLE,
    PRIMARY KEY (user_id, ticker)
);

CREATE TABLE strategy (
	strategy VARCHAR(100) NOT NULL,
    ticker VARCHAR(50) NOT NULL,
    ticker_name VARCHAR(255),
    rating INTEGER,
    PRIMARY KEY (strategy, ticker)
);

INSERT INTO `spse`.`user` (`password`, `username`) VALUES ('698d51a19d8a121ce581499d7b701668', 'Bob');
INSERT INTO `spse`.`user` (`password`, `username`) VALUES ('698d51a19d8a121ce581499d7b701668', 'Sam');

INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Ethical', 'AAPL', 'Apple', 80);
INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Ethical', 'ADBE', 'Adobe', 70);
INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Ethical', 'NSRGY', 'Nestle', 67);

INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Growth', 'VTI', 'Vanguard Total Stock Market ETF', 84);
INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Growth', 'IXUS', 'iShares Core MSCI Total Intl Stk', 75);
INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Growth', 'ILTB', 'iShares Core 10+ Year USD Bond', 69);

INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Index', 'VTI', 'Vanguard Total Stock Market ETF', 84);
INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Index', 'IXUS', 'iShares Core MSCI Total Intl Stk', 75);
INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Index', 'ILTB', 'iShares Core 10+ Year USD Bond', 69);

INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Quality', 'VTI', 'Vanguard Total Stock Market ETF', 84);
INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Quality', 'IXUS', 'iShares Core MSCI Total Intl Stk', 75);
INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Quality', 'ILTB', 'iShares Core 10+ Year USD Bond', 69);

INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Value', 'VTI', 'Vanguard Total Stock Market ETF', 84);
INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Value', 'IXUS', 'iShares Core MSCI Total Intl Stk', 75);
INSERT INTO `spse`.`strategy` (`strategy`, `ticker`, `ticker_name`, `rating`) VALUES ('Value', 'ILTB', 'iShares Core 10+ Year USD Bond', 69);

INSERT INTO `spse`.`portfolio` (`user_id`, `ticker`, `ticker_name`, `share`, `purchase_price`) VALUES ('1', 'VMW', 'Wmware', '10', '100.23');
INSERT INTO `spse`.`portfolio` (`user_id`, `ticker`, `ticker_name`, `share`, `purchase_price`) VALUES ('1', 'AAPL', 'Apple', '12', '221.56');
INSERT INTO `spse`.`portfolio` (`user_id`, `ticker`, `ticker_name`, `share`, `purchase_price`) VALUES ('2', 'ADBE', 'Adobe', '8', '30.56');

