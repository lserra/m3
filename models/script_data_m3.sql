USE mthree;

SET FOREIGN_KEY_CHECKS=0;

TRUNCATE tAccount;
TRUNCATE tCategory;
TRUNCATE tCurrency;
TRUNCATE tCustomer;
TRUNCATE tCustomerProject;
TRUNCATE tExpense;
TRUNCATE tExpenseDetail;
TRUNCATE tMatrix;
TRUNCATE tProject;
TRUNCATE tSystem;
TRUNCATE tUser;
TRUNCATE tWkflUserExp;
TRUNCATE tWorkflow;
TRUNCATE tDomain;
TRUNCATE tUserDomain;

SET FOREIGN_KEY_CHECKS=1;

-- INSERT tCategory
INSERT INTO `mthree`.`tCategory` (`name_category`) VALUES ('Airfare');
INSERT INTO `mthree`.`tCategory` (`name_category`) VALUES ('Coffe Shop');
INSERT INTO `mthree`.`tCategory` (`name_category`) VALUES ('Entertainament');
INSERT INTO `mthree`.`tCategory` (`name_category`) VALUES ('Gasoline');
INSERT INTO `mthree`.`tCategory` (`name_category`) VALUES ('Hotel/Motel');
INSERT INTO `mthree`.`tCategory` (`name_category`) VALUES ('Miscelanous');
INSERT INTO `mthree`.`tCategory` (`name_category`) VALUES ('Phone');
INSERT INTO `mthree`.`tCategory` (`name_category`) VALUES ('Lanch');
INSERT INTO `mthree`.`tCategory` (`name_category`) VALUES ('Supermarket');
COMMIT;

-- INSERT tAccount
INSERT INTO `mthree`.`tAccount` (`name_account`) VALUES ('Cash');
INSERT INTO `mthree`.`tAccount` (`name_account`) VALUES ('Check');
INSERT INTO `mthree`.`tAccount` (`name_account`) VALUES ('Credit Card');
INSERT INTO `mthree`.`tAccount` (`name_account`) VALUES ('Voucher');
COMMIT;

-- INSERT tCurrency
INSERT INTO `mthree`.`tCurrency` (`description`, `code`, `sign`) VALUES ('Brazilian Real', 'BRL', 'R$');
INSERT INTO `mthree`.`tCurrency` (`description`, `code`, `sign`) VALUES ('Australian Dollar', 'AUD', '$');
INSERT INTO `mthree`.`tCurrency` (`description`, `code`, `sign`) VALUES ('Canadian Dollar', 'CAD', '$');
INSERT INTO `mthree`.`tCurrency` (`description`, `code`, `sign`) VALUES ('Euro', 'EUR', '$');
INSERT INTO `mthree`.`tCurrency` (`description`, `code`, `sign`) VALUES ('Brithish Pound', 'GBP', '£');
INSERT INTO `mthree`.`tCurrency` (`description`, `code`, `sign`) VALUES ('New Zealand Dollar', 'NZD', '$');
INSERT INTO `mthree`.`tCurrency` (`description`, `code`, `sign`) VALUES ('United Sates Dollar', 'USD', '$');
COMMIT;

-- INSERT tCustomer
INSERT INTO `mthree`.`tCustomer` (`name_customer`) VALUES ('TIVIT');
INSERT INTO `mthree`.`tCustomer` (`name_customer`) VALUES ('Grupo IBMEC');
INSERT INTO `mthree`.`tCustomer` (`name_customer`) VALUES ('Odebrecht Ambiental');
INSERT INTO `mthree`.`tCustomer` (`name_customer`) VALUES ('Rexam');
INSERT INTO `mthree`.`tCustomer` (`name_customer`) VALUES ('Qualicorp');
COMMIT;

-- INSERT tProject
INSERT INTO `mthree`.`tProject` (`name_project`) VALUES ('HPL Controladoria');
INSERT INTO `mthree`.`tProject` (`name_project`) VALUES ('BI RH');
INSERT INTO `mthree`.`tProject` (`name_project`) VALUES ('BI Jurídico');
INSERT INTO `mthree`.`tProject` (`name_project`) VALUES ('Sustentação Hyperion Planning');
INSERT INTO `mthree`.`tProject` (`name_project`) VALUES ('HPL Custeio RH');
INSERT INTO `mthree`.`tProject` (`name_project`) VALUES ('BI Acadêmico');
COMMIT;

-- INSERT tCustomerProject
INSERT INTO `mthree`.`tCustomerProject` (`id_customer`, `id_project`) VALUES ('1', '1');
INSERT INTO `mthree`.`tCustomerProject` (`id_customer`, `id_project`) VALUES ('1', '2');
INSERT INTO `mthree`.`tCustomerProject` (`id_customer`, `id_project`) VALUES ('1', '3');
INSERT INTO `mthree`.`tCustomerProject` (`id_customer`, `id_project`) VALUES ('1', '5');
INSERT INTO `mthree`.`tCustomerProject` (`id_customer`, `id_project`) VALUES ('5', '4');
INSERT INTO `mthree`.`tCustomerProject` (`id_customer`, `id_project`) VALUES ('3', '4');
INSERT INTO `mthree`.`tCustomerProject` (`id_customer`, `id_project`) VALUES ('2', '6');
INSERT INTO `mthree`.`tCustomerProject` (`id_customer`, `id_project`) VALUES ('4', '4');
COMMIT;

-- INSERT tUser
INSERT INTO `mthree`.`tUser` (`name_user`, `email_user`, `password`) VALUES ('Laercio Serra', 'laercio.serra@neotrend.com.br', 'Y3ljbGVjbHVi');
INSERT INTO `mthree`.`tUser` (`name_user`, `email_user`, `password`) VALUES ('Bruno Fontes', 'bfontes@neotrend.com.br', 'Y3ljbGVjbHVi');
INSERT INTO `mthree`.`tUser` (`name_user`, `email_user`, `password`) VALUES ('Victor Souza', 'vsouza@neotrend.com.br', 'Y3ljbGVjbHVi');
INSERT INTO `mthree`.`tUser` (`name_user`, `email_user`, `password`) VALUES ('Leonardo Coppelli', 'lcoppelli@neotrend.com.br', 'Y3ljbGVjbHVi');
COMMIT;

-- INSERT tSystem
INSERT INTO `mthree`.`tSystem` (`dt_close_report`, `email_alert`, `dt_default`, `dt_format`) VALUES ('2014/09/05', 'S', '2014/09/05', 'yyyy/mm/dd');
COMMIT;

-- INSERT tWorkflow
INSERT INTO `mthree`.`tWorkflow` (`name_step`) VALUES ('Create');
INSERT INTO `mthree`.`tWorkflow` (`name_step`) VALUES ('Submit to Aproval');
INSERT INTO `mthree`.`tWorkflow` (`name_step`) VALUES ('Analyze & Aproval');
INSERT INTO `mthree`.`tWorkflow` (`name_step`) VALUES ('Submit to Payment');
INSERT INTO `mthree`.`tWorkflow` (`name_step`) VALUES ('Payment');
COMMIT;

-- INSERT tMatrix
INSERT INTO `mthree`.`tMatrix` (`id_user`, `profile_user`, `task_user`) VALUES ('1', 'S', 'S');
INSERT INTO `mthree`.`tMatrix` (`id_user`, `profile_user`, `task_user`) VALUES ('2', 'U', 'C');
INSERT INTO `mthree`.`tMatrix` (`id_user`, `profile_user`, `task_user`) VALUES ('3', 'U', 'A');
INSERT INTO `mthree`.`tMatrix` (`id_user`, `profile_user`, `task_user`) VALUES ('4', 'U', 'P');
COMMIT;

-- INSERT tExpense
INSERT INTO `mthree`.`tExpense` (`dt_expense`, `period`, `total_expense`, `comments`) VALUES ('2014/07/31', 'julho/2014', '78.5', 'despesas realizadas com atividades comerciais');
INSERT INTO `mthree`.`tExpense` (`dt_expense`, `period`, `total_expense`, `comments`) VALUES ('2014/06/30', 'junho/2014', '72.34', 'despesas realizadas com atividades comerciais');
COMMIT;

-- INSERT tExpenseDetail
INSERT INTO `mthree`.`tExpenseDetail` (`id_expense`, `number_expense`, `dt_expense`, `category`, `account`, `description`, `amount`) VALUES ('2', '1', '2014/06/10', 'Miscelanous', 'Cash', 'Táxi para o Aeroporto S. Dumont', '10');
INSERT INTO `mthree`.`tExpenseDetail` (`id_expense`, `number_expense`, `dt_expense`, `category`, `account`, `description`, `amount`) VALUES ('2', '2', '2014/06/10', 'Lanch', 'Cash', 'Refeição (Noite)', '10.01');
INSERT INTO `mthree`.`tExpenseDetail` (`id_expense`, `number_expense`, `dt_expense`, `category`, `account`, `description`, `amount`) VALUES ('2', '3', '2014/06/10', 'Lanch', 'Cash', 'Refeição (Noite)', '19.1');
INSERT INTO `mthree`.`tExpenseDetail` (`id_expense`, `number_expense`, `dt_expense`, `category`, `account`, `description`, `amount`) VALUES ('2', '4', '2014/06/11', 'Lanch', 'Cash', 'Refeição (Noite)', '24.53');
INSERT INTO `mthree`.`tExpenseDetail` (`id_expense`, `number_expense`, `dt_expense`, `category`, `account`, `description`, `amount`) VALUES ('2', '5', '2014/06/12', 'Lanch', 'Cash', 'Refeição (Manhã)', '8.7');

INSERT INTO `mthree`.`tExpenseDetail` (`id_expense`, `number_expense`, `dt_expense`, `category`, `account`, `description`, `amount`) VALUES ('1', '1', '2014/07/12', 'Miscelanous', 'Credit Card', 'Gasolina - Visita a Cliente', '70');
INSERT INTO `mthree`.`tExpenseDetail` (`id_expense`, `number_expense`, `dt_expense`, `category`, `account`, `description`, `amount`) VALUES ('1', '2', '2014/07/16', 'Miscelanous', 'Cash', 'Autopista Fluminense S/A (Ida)', '1.7');
INSERT INTO `mthree`.`tExpenseDetail` (`id_expense`, `number_expense`, `dt_expense`, `category`, `account`, `description`, `amount`) VALUES ('1', '3', '2014/07/16', 'Miscelanous', 'Cash', 'Autopista Fluminense S/A (Ida)', '1.7');
INSERT INTO `mthree`.`tExpenseDetail` (`id_expense`, `number_expense`, `dt_expense`, `category`, `account`, `description`, `amount`) VALUES ('1', '4', '2014/07/16', 'Miscelanous', 'Cash', 'Autopista Fluminense S/A (Ida)', '1.7');
INSERT INTO `mthree`.`tExpenseDetail` (`id_expense`, `number_expense`, `dt_expense`, `category`, `account`, `description`, `amount`) VALUES ('1', '5', '2014/07/16', 'Miscelanous', 'Cash', 'Autopista Fluminense S/A (Volta)', '1.7');
INSERT INTO `mthree`.`tExpenseDetail` (`id_expense`, `number_expense`, `dt_expense`, `category`, `account`, `description`, `amount`) VALUES ('1', '6', '2014/07/16', 'MIscelanous', 'Cash', 'Autopista Fluminense S/A (Volta)', '1.7');
COMMIT;

-- INSERT tWkflUserExp
INSERT INTO `mthree`.`tWkflUserExp` (`id_step`, `status`, `id_user`, `id_expense`) VALUES ('1', 'A', '1', '1');
INSERT INTO `mthree`.`tWkflUserExp` (`id_step`, `status`, `id_user`, `id_expense`) VALUES ('1', 'A', '1', '2');
INSERT INTO `mthree`.`tWkflUserExp` (`id_step`, `status`, `id_user`, `id_expense`) VALUES ('2', 'A', '1', '1');
INSERT INTO `mthree`.`tWkflUserExp` (`id_step`, `status`, `id_user`, `id_expense`) VALUES ('2', 'A', '1', '2');
INSERT INTO `mthree`.`tWkflUserExp` (`id_step`, `status`, `id_user`, `id_expense`) VALUES ('3', 'R', '1', '1');
INSERT INTO `mthree`.`tWkflUserExp` (`id_step`, `status`, `id_user`, `id_expense`) VALUES ('3', 'A', '1', '2');
INSERT INTO `mthree`.`tWkflUserExp` (`id_step`, `status`, `id_user`, `id_expense`) VALUES ('4', 'A', '1', '2');
INSERT INTO `mthree`.`tWkflUserExp` (`id_step`, `status`, `id_user`, `id_expense`) VALUES ('5', 'A', '1', '2');
COMMIT;