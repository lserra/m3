USE mthree;

-- VERIFICA SE EXISTE ALGUMA TABELA VAZIA
SELECT COUNT(*) FROM tAccount;
SELECT COUNT(*) FROM tCategory;
SELECT COUNT(*) FROM tCurrency;
SELECT COUNT(*) FROM tCustomer;
SELECT COUNT(*) FROM tCustomerProject;
SELECT COUNT(*) FROM tExpense;
SELECT COUNT(*) FROM tExpenseDetail;
SELECT COUNT(*) FROM tMatrix;
SELECT COUNT(*) FROM tProject;
SELECT COUNT(*) FROM tSystem;
SELECT COUNT(*) FROM tUser;
SELECT COUNT(*) FROM tWkflUserExp;
SELECT COUNT(*) FROM tWorkflow;

-- VERIFICA O CONTEÚDO DAS TABELAS
SELECT * FROM tAccount;
SELECT * FROM tCategory;
SELECT * FROM tCurrency;
SELECT * FROM tCustomer;
SELECT * FROM tCustomerProject;
SELECT * FROM tExpense;
SELECT * FROM tExpenseDetail;
SELECT * FROM tMatrix;
SELECT * FROM tProject;
SELECT * FROM tSystem;
SELECT * FROM tUser;
SELECT * FROM tWkflUserExp;
SELECT * FROM tWorkflow;

-- VERIFICA OS RELACIONAMENTOS DAS TABELAS
-- CUSTOMER x PROJECT
SELECT 
	a.name_customer, b.name_project
FROM
	tCustomer a,
	tProject b,
	tCustomerProject c
WHERE
	a.id_customer = c.id_customer AND
	b.id_project = c.id_project AND
	c.id_customer = '1' AND
	c.id_project = '1';

-- EXPENSE x DETAIL
SELECT 
	a.period, b.*
FROM
	tExpense a,
	tExpenseDetail b
WHERE
	a.id_expense = b.id_expense AND
	a.id_expense = '2';

-- USER x MATRIX
SELECT 
	b.name_user, b.email_user, a.profile_user, a.task_user
FROM
	tMatrix a,
	tUser b
WHERE
	a.id_user = b.id_user AND
	b.id_user = '1';

-- USER x EXPENSE
SELECT DISTINCTROW
	a.name_user, c.id_expense, c.dt_expense, c.period
FROM
	tUser a,
	tWkflUserExp b,
	tExpense c
WHERE
	a.id_user = b.id_user AND
	b.id_expense = c.id_expense AND
	a.id_user = '1';

-- EXPENSE x STATUS
SELECT
	a.name_user, c.id_expense, c.dt_expense, c.period, d.name_step, b.status
FROM
	tUser a,
	tWkflUserExp b,
	tExpense c,
	tWorkflow d
WHERE
	a.id_user = b.id_user AND
	b.id_expense = c.id_expense AND
	b.id_step = d.id_step AND
	a.id_user = '1' AND
	c.id_expense = '1' AND
	b.id_step = (SELECT MAX(id_step) FROM tWkflUserExp WHERE id_user = '1' AND id_expense = '1');