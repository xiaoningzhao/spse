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

INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Ethical','AAPL','Apple',80);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Ethical','ADBE','Adobe',70);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Ethical','NSRGY','Nestle',67);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Growth','ATVI','Activision Blizzard',90);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Growth','FB','Facebook',65);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Growth','WORK','Slack Technologies',97);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Index','ILTB','iShares Core 10+ Year USD Bond',69);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Index','IXUS','iShares Core MSCI Total Intl Stk',75);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Index','VTI','Vanguard Total Stock Market ETF',84);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Quality','KRTX','Karuna Therapeutics Inc',47);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Quality','MSFT','Microsoft',88);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Quality','PLMR','Palomar Holdings Inc',70);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Value','GE','General Electric',79);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Value','T','ATT',62);
INSERT INTO `spse`.`strategy` (`strategy`,`ticker`,`ticker_name`,`rating`) VALUES ('Value','XOM','Exxon Mobil Corporation',91);

