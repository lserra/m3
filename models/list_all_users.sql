SELECT d.domain, u.name_user, u.email_user, m.profile_user, m.task_user 
FROM 
	tDomain d, tUser u, tMatrix m
WHERE 
	d.id_domain = u.id_domain AND
	m.id_user = u.id_user AND
	d.domain='asparona';

