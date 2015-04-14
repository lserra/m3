SELECT m.id_user, m.profile_user, m.task_user, u.name_user, u.email_user
FROM mthree.tMatrix m
	INNER JOIN mthree.tUser u
	ON m.id_user = u.id_user

	INNER JOIN mthree.tDomain d
	ON d.id_domain = u.id_domain
WHERE d.domain = 'asparona' 
	AND m.task_user = 'A'
	AND m.id_user NOT IN 
	(
		SELECT id_publisher_user
		FROM mthree.tMatrixTaskUser
		WHERE domain = 'asparona'
	)
ORDER BY u.name_user