CREATE DATABASE `mthree` /*!40100 DEFAULT CHARACTER SET utf8 */;

CREATE TABLE `tAccount` (
  `id_account` int(11) NOT NULL AUTO_INCREMENT,
  `name_account` varchar(45) NOT NULL,
  PRIMARY KEY (`id_account`),
  UNIQUE KEY `name_account_UNIQUE` (`name_account`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='table account';

CREATE TABLE `tCategory` (
  `id_category` int(11) NOT NULL AUTO_INCREMENT,
  `name_category` varchar(45) NOT NULL,
  PRIMARY KEY (`id_category`),
  UNIQUE KEY `name_category_UNIQUE` (`name_category`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COMMENT='table category';

CREATE TABLE `tCurrency` (
  `id_currency` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(45) NOT NULL COMMENT '(ex.: Brazilian Real)',
  `code` varchar(10) NOT NULL COMMENT '(ex.: BRL)',
  `sign` varchar(5) NOT NULL COMMENT '(ex.: R$)',
  PRIMARY KEY (`id_currency`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='table currency';

CREATE TABLE `tCustomer` (
  `id_customer` int(11) NOT NULL AUTO_INCREMENT,
  `name_customer` varchar(45) NOT NULL,
  PRIMARY KEY (`id_customer`),
  UNIQUE KEY `name_customer_UNIQUE` (`name_customer`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COMMENT='table customer';

CREATE TABLE `tCustomerProject` (
  `id_customer` int(11) NOT NULL,
  `id_project` int(11) NOT NULL,
  PRIMARY KEY (`id_customer`,`id_project`),
  KEY `fk_tCustomerProject_2` (`id_project`),
  CONSTRAINT `fk_tCustomerProject_1` FOREIGN KEY (`id_customer`) REFERENCES `tCustomer` (`id_customer`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_tCustomerProject_2` FOREIGN KEY (`id_project`) REFERENCES `tProject` (`id_project`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='table customer - project';

CREATE TABLE `tDomain` (
  `id_domain` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(20) NOT NULL,
  `company` varchar(45) NOT NULL,
  `street` varchar(45) NOT NULL,
  `city` varchar(25) NOT NULL,
  `state` varchar(25) NOT NULL,
  `zipcode` varchar(10) NOT NULL,
  `website` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `phone` varchar(15) NOT NULL,
  PRIMARY KEY (`id_domain`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='table domain - list of companies';

CREATE TABLE `tExpense` (
  `id_expense` int(11) NOT NULL AUTO_INCREMENT,
  `dt_expense` date NOT NULL COMMENT 'date input expenses',
  `period` varchar(25) NOT NULL COMMENT 'month/year (period) expenses (ex.: janeiro/2014)',
  `total_expense` double NOT NULL DEFAULT '0',
  `comments` text,
  `documents` blob,
  PRIMARY KEY (`id_expense`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='table expenses report';

CREATE TABLE `tExpenseDetail` (
  `id_expense` int(11) NOT NULL,
  `number_expense` int(11) NOT NULL AUTO_INCREMENT,
  `dt_expense` date NOT NULL,
  `category` varchar(45) NOT NULL,
  `account` varchar(15) NOT NULL DEFAULT 'CASH',
  `description` varchar(45) NOT NULL,
  `amount` double NOT NULL DEFAULT '0',
  `document` blob,
  PRIMARY KEY (`number_expense`,`id_expense`),
  KEY `fk_tExpenseDetail_1_idx` (`id_expense`),
  CONSTRAINT `fk_tExpenseDetail_1` FOREIGN KEY (`id_expense`) REFERENCES `tExpense` (`id_expense`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COMMENT='table expense details';

CREATE TABLE `tExpenseOLD` (
  `id_expense` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `id_step` int(11) NOT NULL,
  `dt_expense` date NOT NULL COMMENT 'date input expenses',
  `period` varchar(25) NOT NULL COMMENT 'month/year (period) expenses (ex.: janeiro/2014)',
  `total_expense` double NOT NULL DEFAULT '0',
  `comments` text,
  PRIMARY KEY (`id_expense`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='table expenses report';

CREATE TABLE `tMatrix` (
  `id_user` int(11) NOT NULL,
  `profile_user` varchar(1) DEFAULT NULL COMMENT 'U = user / S = supervisor',
  `task_user` varchar(1) DEFAULT NULL COMMENT 'C = create expense report / A = approval expense report / P = payment expense report / S = all tasks',
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='table matrix security';

CREATE TABLE `tProject` (
  `id_project` int(11) NOT NULL AUTO_INCREMENT,
  `name_project` varchar(45) NOT NULL,
  PRIMARY KEY (`id_project`),
  UNIQUE KEY `name_project_UNIQUE` (`name_project`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COMMENT='table project';

CREATE TABLE `tSystem` (
  `id_domain` int(11) NOT NULL,
  `dt_close_report` date DEFAULT NULL,
  `email_alert` varchar(5) DEFAULT NULL COMMENT 'T = True / F = False',
  `dt_default` date DEFAULT NULL COMMENT 'default date value - use current date when adding an entry',
  PRIMARY KEY (`id_domain`),
  CONSTRAINT `fk_tSystem_1` FOREIGN KEY (`id_domain`) REFERENCES `tDomain` (`id_domain`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='table system';

CREATE TABLE `tUser` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `id_domain` int(11) NOT NULL,
  `name_user` varchar(45) NOT NULL,
  `email_user` varchar(45) NOT NULL,
  `password` varchar(25) NOT NULL,
  `new_user` varchar(1) DEFAULT NULL COMMENT 'S = new user',
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `email_user_UNIQUE` (`email_user`),
  KEY `fk_tUser_1_idx` (`id_domain`),
  CONSTRAINT `fk_tUser_1` FOREIGN KEY (`id_domain`) REFERENCES `tDomain` (`id_domain`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8 COMMENT='table user';

CREATE TABLE `tWkflUserExp` (
  `id_user` int(11) NOT NULL,
  `id_expense` int(11) NOT NULL,
  `id_step` int(11) NOT NULL,
  `status` varchar(1) NOT NULL DEFAULT 'A' COMMENT 'A = Accepted / R = Rejected',
  `dt_record` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_user`,`id_expense`,`id_step`),
  KEY `fk_tWkflUserExp_2_idx` (`id_expense`),
  KEY `fk_tWkflUserExp_3_idx` (`id_step`),
  CONSTRAINT `fk_tWkflUserExp_1` FOREIGN KEY (`id_user`) REFERENCES `tUser` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_tWkflUserExp_2` FOREIGN KEY (`id_expense`) REFERENCES `tExpense` (`id_expense`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_tWkflUserExp_3` FOREIGN KEY (`id_step`) REFERENCES `tWorkflow` (`id_step`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='table workflow - user - expense';

CREATE TABLE `tWorkflow` (
  `id_step` int(11) NOT NULL AUTO_INCREMENT,
  `name_step` varchar(45) NOT NULL,
  PRIMARY KEY (`id_step`),
  UNIQUE KEY `name_step_UNIQUE` (`name_step`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COMMENT='table workflow';
