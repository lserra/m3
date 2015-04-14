DELETE
FROM tUser
WHERE id_user NOT IN
(SELECT id_user FROM tMatrix)