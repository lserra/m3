def put_assoc_matrix(name_user, profile):
    """
    # Funcão que inclui o novo associado para ter acesso ao sistema
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de insert no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param name_user: 'Laercio Serra'
    :param profile: 'S'
    :return:is_domain, s_iddomain
    """
    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            (is_assoc, id_assoc) = verify_assoc_id(name_user)  # verifica a existência do associado informado
            if is_assoc:
                s_sql = "INSERT INTO tMatrix (id_user, profile_user, task_user) " + \
                        "VALUES ('" + str(id_assoc) + "', '" + name_user + "', '" + profile + "');"

                bd.execute(s_sql)

                # Confirma a transação de inserção de registro no banco de dados
                msg_err = commit_bd()
                if msg_err != '' and msg_err is not None:
                    return False, msg_err
                else:
                    return True, msg_err
            else:
                return False, 'The \'Domain\' that has been informed does not exist. Please, try again or contact ' \
                              'your System Administrator!'

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn:
            fechar_bd()
