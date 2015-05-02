#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

"""
Created on 27/05/2014
@author: Laércio Serra (laercio.serra@gmail.com)
"""

# Classe que realiza a conexão com o banco de dados MySQL
import MySQLdb
# Classe que realiza operações de expressões regulares
import re
# Classe que realiza a conexão com o servidor de e-mail
import smtplib
# Classe que realiza operações com data/hora
import datetime


def abrir_bd():
    """
    # Esta função utiliza o módulo Mysqldb que contem a API de comunicação com o Mysql.
    # É preciso informar o usuário e senha que foi configurado no Mysql nesse momento.
    """
    global conn, bd

    try:
        conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="mthree")
        bd = conn.cursor()
    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return error_msg


def add_newuser(domain, name, email, pwd, profile, task):
    """
    # Função que retorna se os dados do novo usuário foi gravado  na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain: 'asparona'
    :param name: 'Laercio Serra'
    :param email: 'laercio.serra@asparona.com'
    :param pwd: 'q12we34!' (criptografada)
    :param profile: 'U'
    :param profile: 'A'
    :return user_added: 'True/False'
    :return erro_msg: 'Usuário já existe na base de dados'
    """
    # 1- criptografar a senha
    pwd_newuser = assoc_pwd_crypto(pwd)

    # 2- INSERT VALUES na tbUser
    (user_added, error_msg) = put_assoc_from_id(domain, name, email, pwd_newuser)

    # verifica se o bd não retornou algum erro, então INSERT VALUES na tbMatrix
    if user_added is True:
        # 3- INSERT VALUES na tbMatrix
        (matrix_added, error_msg) = put_assoc_matrix(name, profile, task)
        # verifica se o bd não retornou algum erro
        if matrix_added is True:
            user_added = matrix_added
            return user_added, error_msg
        else:
            user_added = matrix_added
            return user_added, error_msg
    else:
        return user_added, error_msg


def add_newwkflw(domain, publisher, approver, payer):
    """
    # Função que retorna se os dados do novo workflow foi gravado  na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain: 'asparona'
    :param publisher: '33'
    :param approver: '28'
    :param payer: '12'
    :return wklw_added: 'True/False'
    :return erro_msg: 'Usuário já existe na base de dados'
    """
    global p_id, p_email, p_name, a_id, a_email, a_name, y_id, y_email, y_name
    s_domain = str.lower(domain)

    try:
        msg_err = abrir_bd()

        if msg_err != '' and msg_err is not None:
            raise MySQLdb.Error(msg_err)
        else:
            # 1- Pegar dados do PUBLISHER
            p_sql = "SELECT u.id_user, u.email_user, u.name_user " \
                    "FROM tUser u INNER JOIN tDomain d ON u.id_domain = d.id_domain " \
                    "INNER JOIN tMatrix m ON u.id_user = m.id_user " \
                    "WHERE d.domain = '" + str(s_domain) + "' AND u.id_user = '" + str(publisher) + \
                    "' AND m.task_user = 'C';"

            bd.execute(p_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                p_id, p_email, p_name = bd.fetchone()

            # 2- Pegar dados do APPROVER
            a_sql = "SELECT u.id_user, u.email_user, u.name_user " \
                    "FROM tUser u INNER JOIN tDomain d ON u.id_domain = d.id_domain " \
                    "INNER JOIN tMatrix m ON u.id_user = m.id_user " \
                    "WHERE d.domain = '" + str(s_domain) + "' AND u.id_user = '" + str(approver) + \
                    "' AND m.task_user = 'A';"

            bd.execute(a_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                a_id, a_email, a_name = bd.fetchone()

            # 3- Pegar dados do PAYER
            y_sql = "SELECT u.id_user, u.email_user, u.name_user " \
                    "FROM tUser u INNER JOIN tDomain d ON u.id_domain = d.id_domain " \
                    "INNER JOIN tMatrix m ON u.id_user = m.id_user " \
                    "WHERE d.domain = '" + str(s_domain) + "' AND u.id_user = '" + str(payer) + \
                    "' AND m.task_user = 'P';"

            bd.execute(y_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                y_id, y_email, y_name = bd.fetchone()

            # 4- INSERT VALUES na tMatrixTaskUser
            s_sql = "INSERT INTO tMatrixTaskUser(domain, id_publisher_user, publisher_name, publisher_email, " \
                    "id_approver_user, approver_name, approver_email, id_payer_user, payer_name, payer_email) " \
                    "VALUES('" + s_domain + "','" + str(p_id) + "','" + p_name + "','" + p_email + "','" + str(a_id) + \
                    "','" + a_name + "','" + a_email + "','" + str(y_id) + "','" + y_name + "','" + y_email + "');"

            bd.execute(s_sql)

            # Confirma a transação de inserção de registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                raise MySQLdb.Error(msg_err)
            else:
                return True, msg_err

    except MySQLdb.IntegrityError, e:
        if conn:
            rollback_bd()

        error_msg = " %d - %s" % (e.args[0], e.args[1])
        return False, error_msg

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def assoc_pwd_crypto(s_pwd):
    """
    # codifica a senha do associado
    :param s_pwd: '1234'
    :return: %$(@!
    """
    cipher_text = s_pwd.encode('base64', 'strict')

    return cipher_text


def assoc_pwd_decrypto(s_pwd):
    """
    # decodifica a senha do associado
    :param s_pwd: %$(@!
    :return: '1234'
    """
    cipher_text = s_pwd.decode('base64', 'strict')

    return cipher_text


def auth_assoc(email, pwd):
    """
    # Função que valida o acesso do associado ao sistema (autenticação)
    # valida o e-mail e a senha do associado
    :param email: 'laercio.serra@gmail.com'
    :param pwd: '1234'
    :return: True
    """
    decrypt = assoc_pwd_decrypto(pwdassoc)
    decrypt = unicode(decrypt, 'utf-8')

    if email == emailassoc and pwd == decrypt:
        return True
    else:
        return False


def commit_bd():
    """
    # Esta função utiliza o módulo Mysqldb que contem a API de comunicação com o Mysql.
    """
    try:
        conn.commit()
    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return error_msg


def delete_user(iddomain_ue, email_ue):
    """
    # Função que exclui os dados do associado no sistema
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param iddomain_ue: 'asparona'
    :param email_ue: 'name@domain.com'
    :return: True, msg_err
    """
    s_sqlu = "DELETE FROM tUser WHERE id_domain = '" + str(iddomain_ue) + "' AND email_user = '" + email_ue + "';"
    s_sqlm = "DELETE FROM tMatrix WHERE id_user IN (SELECT id_user FROM tUser WHERE " \
             "id_domain = '" + str(iddomain_ue) + "' AND email_user = '" + email_ue + "');"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            # exclui os dados do associado na table Matrix
            bd.execute(s_sqlm)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                commit_bd()
                # exclui os dados do associado na table User
                bd.execute(s_sqlu)
                # Pega o número de linhas no resultset
                numrows = int(bd.rowcount)

                if numrows > 0:
                    commit_bd()
                    return True, None
                else:
                    return False, ' None user was deleted!'
            else:
                return False, ' None user was deleted!'

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def delete_wkflw(domain, wdel):
    """
    # Função que exclui os dados do workflow no sistema
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain: 'asparona'
    :param wdel: 'name@domain.com'
    :return: True, msg_err
    """
    s_sql = "DELETE FROM tMatrixTaskUser WHERE domain = '" + domain + "' AND id_matrix_task_user = '" + str(wdel) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            # exclui os dados do workflow
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                # Confirma a transação de exclusão do workflow no banco de dados
                msg_err = commit_bd()
                if msg_err != '' and msg_err is not None:
                    raise MySQLdb.Error(msg_err)
                else:
                    return True, None
            else:
                return False, ' None workflow was deleted!'

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def edit_user(domain_ue, email_ue):
    """
    # Função que retorna os dados do associado cadastrado para edição
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain_ue: 'asparona'
    :param email_ue: 'name@domain.com'
    :return: s_domain_ue, s_name_ue, s_email_ue, s_profile_ue, s_task_user
    """
    s_sql = "SELECT d.domain, u.name_user, u.email_user, m.profile_user, m.task_user " + \
            "FROM tDomain d, tUser u, tMatrix m WHERE d.id_domain = u.id_domain AND " + \
            "m.id_user = u.id_user AND " + \
            "d.domain='" + domain_ue + "' AND " + \
            "u.email_user = '" + email_ue + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                d_ue, n_ue, e_ue, p_ue, t_ue = bd.fetchone()
                return d_ue, n_ue, e_ue, p_ue, t_ue
            else:
                return None, None, None, None, None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def edit_wkflw(domain_we, num_we):
    """
    # Função que retorna os dados do workflow para edição
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain_we: 'asparona'
    :param num_we: 'Laercio Serra'
    :return: id_p, name_p
    """
    s_sql = "SELECT id_publisher_user, publisher_name, id_approver_user, approver_name, id_payer_user, payer_name " \
            "FROM tMatrixTaskUser WHERE domain = '" + domain_we + "' AND id_matrix_task_user = '" + num_we + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                id_p, name_p, id_a, name_a, id_y, name_y = bd.fetchone()
                return id_p, name_p, id_a, name_a, id_y, name_y
            else:
                return None, None, None, None, None, None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def fechar_bd():
    """
    # Esta função utiliza o módulo Mysqldb que contem a API de comunicação com o Mysql.
    """
    conn.close()


def get_all_approver(domain_name):
    """
    # Função que retorna todos os users com o perfil de approver
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain_name: 'asparona'
    :return: {rs_dt_table}
    """
    s_sql = "SELECT m.id_user, u.name_user " + \
            "FROM tMatrix m INNER JOIN tUser u ON m.id_user = u.id_user " + \
            "INNER JOIN tDomain d ON d.id_domain = u.id_domain " + \
            "WHERE d.domain='" + str(domain_name) + "' AND m.task_user = 'A' " \
            "ORDER BY u.name_user;"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                rs_dt_table = bd.fetchall()
                return rs_dt_table, msg_err
            else:
                rs_dt_table = None
                return rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_all_approver_cb(domain_name, approver):
    """
    # Função que retorna todos os users com o perfil de approver para popular a combo box
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain_name: 'asparona'
    :param approver: '32'
    :return: {rs_dt_table}
    """
    s_sql = "SELECT m.id_user, u.name_user " + \
            "FROM tMatrix m INNER JOIN tUser u ON m.id_user = u.id_user " + \
            "INNER JOIN tDomain d ON d.id_domain = u.id_domain " + \
            "WHERE d.domain='" + str(domain_name) + "' AND m.task_user = 'A' " \
            "AND m.id_user <> '" + str(approver) + "' ORDER BY u.name_user;"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                rs_dt_table = bd.fetchall()
                return rs_dt_table, msg_err
            else:
                rs_dt_table = None
                return rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_all_acct(domain):
    """
    # Função que retorna os accounts cadastrados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain: 'asparona'
    :return: {fields, rs_dt_table}
    """
    s_sql = "SELECT name_account FROM tAccount WHERE domain = '" + domain + "';"

    fields = ('Account',)

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return fields, None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                rs_dt_table = bd.fetchall()
                return fields, rs_dt_table, msg_err
            else:
                rs_dt_table = None
                return fields, rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return fields, None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_all_assoc(domain_name):
    """
    # Função que retorna os associados cadastrados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain_name: 'asparona'
    :return: {fields, rs_dt_table}
    """
    s_sql = "SELECT u.name_user, u.email_user, m.profile_user, m.task_user " + \
            "FROM tDomain d, tUser u, tMatrix m WHERE d.id_domain = u.id_domain AND m.id_user = u.id_user AND " + \
            "d.domain='" + str(domain_name) + "';"

    fields = ('Name', 'Email', 'Profile', 'Task')

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return fields, None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                rs_dt_table = bd.fetchall()
                return fields, rs_dt_table, msg_err
            else:
                rs_dt_table = None
                return fields, rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return fields, None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_all_payer(domain_name):
    """
    # Função que retorna todos os users com o perfil de payer
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain_name: 'asparona'
    :return: {rs_dt_table}
    """
    s_sql = "SELECT m.id_user, u.name_user " + \
            "FROM tMatrix m INNER JOIN tUser u ON m.id_user = u.id_user " + \
            "INNER JOIN tDomain d ON d.id_domain = u.id_domain " + \
            "WHERE d.domain='" + str(domain_name) + "' AND m.task_user = 'P' " \
            "ORDER BY u.name_user;"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                rs_dt_table = bd.fetchall()
                return rs_dt_table, msg_err
            else:
                rs_dt_table = None
                return rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_all_payer_cb(domain_name, payer):
    """
    # Função que retorna todos os users com o perfil de payer para popular a combo box
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain_name: 'asparona'
    :param payer: 'asparona'
    :return: {rs_dt_table}
    """
    s_sql = "SELECT m.id_user, u.name_user " + \
            "FROM tMatrix m INNER JOIN tUser u ON m.id_user = u.id_user " + \
            "INNER JOIN tDomain d ON d.id_domain = u.id_domain " + \
            "WHERE d.domain='" + str(domain_name) + "' AND m.task_user = 'P' AND m.id_user <> '" + str(payer) + \
            "' ORDER BY u.name_user;"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                rs_dt_table = bd.fetchall()
                return rs_dt_table, msg_err
            else:
                rs_dt_table = None
                return rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_all_publisher(domain_name):
    """
    # Função que retorna todos os users com o perfil de publisher
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain_name: 'asparona'
    :return: {rs_dt_table}
    """
    s_sql = "SELECT m.id_user, u.name_user " + \
            "FROM tMatrix m INNER JOIN tUser u ON m.id_user = u.id_user " + \
            "INNER JOIN tDomain d ON d.id_domain = u.id_domain " + \
            "WHERE d.domain='" + str(domain_name) + "' AND m.task_user = 'C' AND m.id_user NOT IN " + \
            "(SELECT id_publisher_user FROM tMatrixTaskUser WHERE domain='" + str(domain_name) + "') " + \
            "ORDER BY u.name_user;"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                rs_dt_table = bd.fetchall()
                return rs_dt_table, msg_err
            else:
                rs_dt_table = None
                return rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_all_publisher_cb(domain_name, publisher):
    """
    # Função que retorna todos os users com o perfil de publisher para popular a combo box
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain_name: 'asparona'
    :param publisher: '32'
    :return: {rs_dt_table}
    """
    s_sql = "SELECT m.id_user, u.name_user " + \
            "FROM tMatrix m INNER JOIN tUser u ON m.id_user = u.id_user " + \
            "INNER JOIN tDomain d ON d.id_domain = u.id_domain " + \
            "WHERE d.domain='" + str(domain_name) + "' AND m.task_user = 'C' " \
            "AND m.id_user <> '" + str(publisher) + "' ORDER BY u.name_user;"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                rs_dt_table = bd.fetchall()
                return rs_dt_table, msg_err
            else:
                rs_dt_table = None
                return rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_all_matrix(domain_name):
    """
    # Função que retorna a matrix task user
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain_name: 'asparona'
    :return: {fields, rs_dt_table}
    """
    s_sql = "SELECT id_matrix_task_user, m.publisher_name, m.approver_name, m.payer_name " + \
            "FROM tMatrixTaskUser m WHERE m.domain='" + str(domain_name) + "';"

    fields = ('#', 'Publisher', 'Approver', 'Payer')

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return fields, None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                rs_dt_table = bd.fetchall()
                return fields, rs_dt_table, msg_err
            else:
                rs_dt_table = None
                return fields, rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return fields, None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_approver_from_id(domain, approver):
    """
    # Função que retorna os dados do approver a partir do id
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain: 'asparona'
    :param approver: '12'
    :return id_approver: '12'
    :return name_approver: 'Laercio Serra'
    :return email_approver: 'laercio.serra@asparona.com'
    """
    s_sql = "SELECT m.id_user, u.name_user, u.email_user " \
            "FROM tMatrix m INNER JOIN tUser u ON m.id_user = u.id_user " \
            "INNER JOIN tDomain d ON d.id_domain = u.id_domain " \
            "WHERE d.domain='" + domain + "' AND m.task_user='A' AND " \
                                          "m.id_user='" + str(approver) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                (id_approver, name_approver, email_approver) = bd.fetchone()
                return id_approver, name_approver, email_approver
            else:
                return None, None, None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_acct_from_id(idacct):
    """
    # Função que retorna o account cadastrado
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param idacct: '1'
    :return: s_acct_new
    """
    s_sql = "SELECT name_account FROM tAccount WHERE id_account = '" + idacct + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                s_account = bd.fetchone()
                return s_account[0], msg_err
            else:
                return None, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_assoc_from_id(email):
    """
    # Função que verifica se o associado existe e retorna os seus dados a partir do email
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param email: 'laercio.serra@gmail.com'
    :return:idassoc, iddomain, nameuser, emailassoc, pwdassoc
    """
    global idassoc, iddomain, nameuser, emailassoc, pwdassoc

    s_sql = "SELECT id_user, id_domain, name_user, email_user, password FROM tUser WHERE email_user='" + \
            str(email) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                (idassoc, iddomain, nameuser, emailassoc, pwdassoc) = bd.fetchone()
                return True, msg_err
            else:
                return False, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_domain_assoc(id_domain, email):
    """
    # Função que verifica se o associado pertence ao dominio informado
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param id_domain: '2'
    :param email: 'laercio.serra@gmail.com'
    :return: True, msg_err
    """
    s_sql = "SELECT id_user, id_domain, name_user, email_user, password FROM tUser WHERE id_domain = '" + \
            str(id_domain) + "' AND email_user = '" + email + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                return True, msg_err
            else:
                return False, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_payer_from_id(domain, payer):
    """
    # Função que retorna os dados do payer a partir do id
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain: 'asparona'
    :param payer: '12'
    :return id_payer: '12'
    :return name_payer: 'Laercio Serra'
    :return email_payer: 'laercio.serra@asparona.com'
    """
    s_sql = "SELECT m.id_user, u.name_user, u.email_user " \
            "FROM tMatrix m INNER JOIN tUser u ON m.id_user = u.id_user " \
            "INNER JOIN tDomain d ON d.id_domain = u.id_domain " \
            "WHERE d.domain='" + domain + "' AND m.task_user='P' AND " \
                                          "m.id_user='" + str(payer) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                (id_payer, name_payer, email_payer) = bd.fetchone()
                return id_payer, name_payer, email_payer
            else:
                return None, None, None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_publisher_from_id(domain, publisher):
    """
    # Função que retorna os dados do publisher a partir do id
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain: 'asparona'
    :param publisher: '12'
    :return id_publisher: '12'
    :return name_publisher: 'Laercio Serra'
    :return email_publisher: 'laercio.serra@asparona.com'
    """
    s_sql = "SELECT m.id_user, u.name_user, u.email_user " \
            "FROM tMatrix m INNER JOIN tUser u ON m.id_user = u.id_user " \
            "INNER JOIN tDomain d ON d.id_domain = u.id_domain " \
            "WHERE d.domain='" + domain + "' AND m.task_user='C' AND " \
                                          "m.id_user='" + str(publisher) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                (id_publisher, name_publisher, email_publisher) = bd.fetchone()
                return id_publisher, name_publisher, email_publisher
            else:
                return None, None, None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_assoc_supervisor(domain):
    """
    # Funcão que verifica se já existe um associado com o perfil de Supervisor
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de insert no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param domain: 'asparona'
    :return:False
    """
    s_domain = str.lower(domain)

    s_sql = "SELECT d.domain, u.name_user, u.email_user, m.profile_user, m.task_user " + \
            "FROM " + \
            "tDomain d, tUser u, tMatrix m " + \
            "WHERE " + \
            "d.id_domain = u.id_domain AND " + \
            "m.id_user = u.id_user AND " + \
            "d.domain='" + s_domain + "' AND " + \
            "m.profile_user = 'S';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                return True
            else:
                return False

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_profile_assoc(email):
    """
    # Função que verifica e retorna o perfil do associado
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param email: 'laercio.serra@gmail.com'
    :return: 'S' (supervisor)
    """
    s_sql = "SELECT m.profile_user FROM tMatrix m INNER JOIN tUser u ON m.id_user = u.id_user" + \
            " WHERE u.email_user='" + str(email) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                profile = bd.fetchone()
                return profile[0]
            else:
                return None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_setsys(id_domain):
    """
    # Função que retorna os settings system armazenado no banco de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param id_domain: 1
    :return: s_iddomain, s_dtrep, s_alrep
    """
    global s_iddomain, s_dtrep, s_alrep

    s_sql = "SELECT id_domain, dt_close_report, email_alert FROM tSystem WHERE id_domain = '" + str(id_domain) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                (s_iddomain, s_dtrep, s_alrep) = bd.fetchone()
                return s_iddomain, s_dtrep, s_alrep
            else:
                return 'None', 'None', 'None'

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def list_expenses_payments_accepted(id_assoc):
    """
    # Função que pega o id do associado e retorna os 12 últimos expenses report que já foram pagos (result set)
    # são passados para a query os valores de identificação do associado e o domínio a que ele pertence
    # id_step = '5' -> Payment / status = 'A' -> (aprovado)
    :param id_assoc: 1
    :return:fields, rs_dt_table, msg_err
    """
    s_sql = "SELECT DISTINCTROW c.id_expense, c.dt_expense, c.period, c.total_expense, d.name_step, " \
            "b.status FROM tUser a, tWkflUserExp b, tExpense c, tWorkflow d WHERE a.id_user = b.id_user AND " \
            "b.id_expense = c.id_expense AND d.id_step = '5' AND b.status = 'A' AND a.id_user = '" + str(id_assoc) + \
            "' ORDER by 2 desc;"

    fields = ('Number', 'Date', 'Period', 'Total', 'Step', 'Status')

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                # Limita o resultset para os 12 últimos expenses
                rs_dt_table = bd.fetchmany(12)
                return fields, rs_dt_table, msg_err
            else:
                return fields, None, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def put_assoc_from_id(domain, name_user, email, pwd):
    """
    # Funcão que inclui o novo associado para ter acesso ao sistema
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de insert no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param domain: 'asparona'
    :param name_user: 'Laercio Serra'
    :param email: 'laercio.serra@gmail.com'
    :param pwd: '1234'
    :return:False, msg_error
    """
    s_domain = str.lower(domain)
    s_email = str.lower(email)

    try:
        (is_domain, id_domain) = verify_domain(s_domain)  # verifica a existência do domínio informado
        if is_domain:
            s_sql = "INSERT INTO tUser (id_domain, name_user, email_user, password, new_user) " + \
                    "VALUES ('" + str(id_domain) + "', '" + name_user + "', '" + s_email + "', '" + \
                    pwd + "', 'S');"

            msg_err = abrir_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
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

    except MySQLdb.IntegrityError, e:
        if conn:
            rollback_bd()

        error_msg = " %d - %s" % (e.args[0], e.args[1])
        return False, error_msg

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def put_assoc_matrix(name_user, profile, task):
    """
    # Funcão que inclui o novo associado para ter acesso ao sistema
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de insert no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param name_user: 'Laercio Serra'
    :param profile: 'S'
    :param task: 'A'
    :return:False, msg_error
    """
    try:
        (is_assoc, id_assoc) = verify_assoc_id(name_user)  # verifica a existência do associado informado
        if is_assoc:
            s_sql = "INSERT INTO tMatrix (id_user, profile_user, task_user) " + \
                    "VALUES ('" + str(id_assoc) + "', '" + profile + "', '" + task + "');"

            msg_err = abrir_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
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

    except MySQLdb.IntegrityError, e:
        if conn:
            rollback_bd()

        error_msg = " %d - %s" % (e.args[0], e.args[1])
        return False, error_msg

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def return_data_assoc():
    """
    # Função que retorna os dados do associado
    :return: idassoc, iddomain, nameuser, emailassoc, pwdassoc
    """
    return idassoc, iddomain, nameuser, emailassoc, pwdassoc


def return_domain_id(domain_name):
    """
    # Função que retorna o ID do domínio a partir do nome
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain_name:'asparona'
    :return: id_domain
    """
    s_sql = "SELECT id_domain FROM tDomain WHERE domain = '" + domain_name + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                (id_domain) = bd.fetchone()
                return id_domain
            else:
                return None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def return_domain_name(id_domain):
    """
    # Função que retorna o nome do domínio a partir do id
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param id_domain:'asparona'
    :return: domain_name
    """
    s_sql = "SELECT id_domain, domain FROM tDomain WHERE id_domain = '" + str(id_domain) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                (id_domain, dname) = bd.fetchone()
                return dname
            else:
                return None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def rollback_bd():
    """
    # Esta função utiliza o módulo Mysqldb que contem a API de comunicação com o Mysql.
    """
    try:
        conn.rollback()
    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return error_msg


def send_login_assoc(s_email, s_pwd):
    """
    # Função que envia os dados de login do associado por email
    # conecta-se a um servidor do gmail para enviar os dados de login
    # do associado por e-mail
    :param s_email:'laercio.serra@gmail.com'
    :param s_pwd:'1234'
    :return: True, msg_err
    """
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = '587'
        msg_err = ''

        sender = 'laercio.serra@neotrend.com.br'  # trocar pelo endereço de email: admin@mthree.com

        subject = '[M3]-Login'

        header = 'To:' + s_email + '\n' + 'From: ' + sender + '\n' + 'Subject:' + subject + '\n'

        body = 'Dear Associated,\n\n'
        body += 'We are sending your login to access the M3-My Expenses Report.\r\n\r\n'
        body += 'Login = ' + s_email + '\r\n'
        body += 'Password = ' + s_pwd + '\r\n\r\n'
        body += 'Best regards,\n\n'
        body += 'M3 Team\r'
        body += '---------------------------------------------------------------------------------\r'
        body += 'If you did not request this verification, please you must to ignore this message!'

        msg = header + '\n' + body

        session = smtplib.SMTP(smtp_server, smtp_port)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login('laercio.serra@neotrend.com.br', 'lS071134')  # trocar pelo endereço de email: admin@mthree.com
        session.sendmail(sender, s_email, msg)
        session.quit()

        return True, msg_err

    except smtplib.SMTPException:
        error_msg = "Fail to sending email."
        return False, error_msg


def send_message(nome, email, motivo, descmotivo):
    """
    # Função que envia uma mensagen registrada pelo associado deixada através da página 'contato.html'
    # conecta-se a um servidor do gmail para enviar a mensagem
    :param nome:'Laercio Serra'
    :param email:'laercio.serra@gmail.com'
    :param motivo:'Reclamação'
    :param descmotivo:'problema de autenticação'
    :return: True, msg_err
    """
    s_nome = nome
    s_email = email
    s_motivo = motivo

    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = '587'
        msg_err = ''

        sender = 'laercio.serra@neotrend.com.br'  # trocar pelo endereço de email: admin@mthree.com

        subject = '[M3]-' + s_motivo

        header = 'To:' + 'laercio.serra@gmail.com' + '\n' + 'From: ' + s_email + '\n' + 'Subject:' + subject + '\n'

        body = descmotivo + '\r\n\n'
        body += 'Att,\r\n\n'
        body += s_nome + '\r\n'
        body += s_email

        msg = header + '\n' + body

        session = smtplib.SMTP(smtp_server, smtp_port)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login('laercio.serra@neotrend.com.br', 'lS071134')  # trocar pelo endereço de email: admin@mthree.com
        session.sendmail(sender, 'laercio.serra@gmail.com', msg)
        session.quit()

        return True, msg_err

    except smtplib.SMTPException:
        error_msg = "Fail to sending email."
        return False, error_msg


def update_login_assoc(s_email, s_pwd):
    """
    # Função que atualiza os dados de login do associado na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de update no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param s_email:'laercio.serra@gmail.com'
    :param s_pwd:'teste1234'
    :return:True, msg_err
    """
    login = s_email
    new_pwd = s_pwd
    s_sql = "UPDATE TB_ASSOC SET pwdassoc='" + str(new_pwd) + "' WHERE emailassoc='" + login + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Confirma a transação de update do registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                return True, msg_err

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def update_profile_assoc(d_eduser, id_eduser, n_eduser, e_eduser, p_eduser, t_eduser):
    """
    # Função que atualiza os dados do associado na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de update no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param d_eduser: 'asparona'
    :param n_eduser: 'Laercio Serra'
    :param e_eduser: 'laercio.serra@asparona.com'
    :param p_eduser: 'S'
    :param t_eduser: 'S'
    :return:True, msg_err
    """
    # instrução de UPDATE na tabela USERS
    s_sql_u = "UPDATE tUser SET name_user = '" + n_eduser + "', email_user = '" + e_eduser + "' " + \
              "WHERE id_user = '" + str(id_eduser) + "' AND id_domain = '" + str(d_eduser) + "';"
    # instrução de UPDATE na tabela MATRIX
    s_sql_m = "UPDATE tMatrix SET profile_user = '" + p_eduser + "', task_user = '" + t_eduser + "' " + \
              "WHERE id_user = '" + str(id_eduser) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql_u)
            # Confirma a transação de update do registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                bd.execute(s_sql_m)
                # Confirma a transação de update do registro no banco de dados
                msg_err = commit_bd()
                if msg_err != '' and msg_err is not None:
                    return False, msg_err
                else:
                    return True, msg_err

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def update_pwd_assoc(s_id_domain, s_email, s_pwd1):
    """
    # Função que atualiza a senha do associado na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de update no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param s_id_domain:'asparona'
    :param s_email:'laercio.serra@gmail.com'
    :param s_pwd1:'teste1234'
    :return: True, msg_err
    """
    s_sql = "UPDATE tUser SET password = '" + s_pwd1 + "' " \
            "WHERE id_domain = '" + str(s_id_domain[0]) + "' AND email_user = '" + s_email + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Confirma a transação de update do registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                return True, msg_err

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def update_setsys(id_domain, alrep, dtrep):
    """
    # Função que atualiza os settings system na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de update no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param id_domain:
    :param alrep:
    :param dtrep:
    :return:True, msg_err
    """
    s_sql = "UPDATE tSystem SET email_alert = '" + alrep + "', dt_close_report = '" + dtrep + "', "
    s_sql += "dt_default = '" + dtrep + "' WHERE id_domain = '" + str(id_domain) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Confirma a transação de update do registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                return True, msg_err

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def update_status_assoc(s_id, s_regra="S"):
    """
    # Função que atualiza o status do associado em relação as regras e o termo de contrato
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de update no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param s_id: '17'
    :param s_regra: 'Concordo'
    :return:True, msg_err
    """
    id_assoc = s_id
    regra = s_regra
    s_sql = "UPDATE TB_ASSOC SET regra='" + regra + "' WHERE idassoc='" + str(id_assoc) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Confirma a transação de update do registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                return True, msg_err

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def update_wkflw(wkflw, domain, id_p, name_p, email_p, id_a, name_a, email_a, id_y, name_y, email_y):
    """
    # Função que atualiza os dados do workflow na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de update no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param wkflw: '12'
    :param domain: 'asparona'
    :param id_p: '12'
    :param name_p: 'Laercio Serra'
    :param email_p: 'laercio.serra@asparona.com'
    :param id_a: '32'
    :param name_a: 'Dilma Roussef'
    :param email_a: 'dilma.r@asparona.com'
    :param id_y: '33'
    :param name_y: 'Luiz Inacio da Silva'
    :param email_y: 'lula@asparona.com'
    :return wkflw_edited: 'True'
    :return s_erromsg: error_msg
    """
    s_sql = "UPDATE tMatrixTaskUser SET " \
            "id_publisher_user = '" + str(id_p) + "', publisher_name = '" + name_p + "', " \
            "publisher_email = '" + email_p + "', " + "id_approver_user = '" + str(id_a) + "', " \
            "approver_name = '" + name_a + "', approver_email = '" + email_a + "', " \
            "id_payer_user = '" + str(id_y) + "', payer_name = '" + name_y + "', " \
            "payer_email = '" + email_y + "' WHERE domain = '" + domain + "' AND " \
            "id_matrix_task_user = '" + str(wkflw) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Confirma a transação de update do registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                return True, msg_err

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def validate_date(date_text):
    """
    # Função que verifica se o valor informado é uma data válida
    :param date_text: 2015-01-26 (YYYY-MM-DD)
    :return: True/False
    """
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        # s_erromsg = None
        return True
    except ValueError:
        # s_erromsg = "Incorrect data format, should be YYYY-MM-DD"
        return False


def validate_email(address):
    """
    # Função que valida se o e-mail informado pelo usuário é válido
    :param address:'laercio.serra@gmail.com'
    :return:True
    """
    if address == '' or address is None:
        address = "-@-"

    """ from http://www.regular-expressions.info/email.html """
    pattern = r"\b[a-zA-Z0-9._%+-]*[a-zA-Z0-9_%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b"
    if re.match(pattern, address):
        return True
    else:
        return False


def validate_newpwd(pwd1, pwd2):
    """
    # Função que valida a nova senha do associado
    # verifica se os valores informados possuem mais do que 8 caracteres,
    # em seguida verifica as novas senhas e compara estes valores
    # se os valores forem iguais a nova senha está correta
    # senão envia uma mensagem para o usuário
    :param pwd1:'teste1234'
    :param pwd2:'teste1234'
    :return:True, msg_err
    """
    msg_err = None

    if (len(pwd1) >= 8) and (len(pwd2) >= 8):
        if pwd1 == pwd2:
            return True, msg_err
        else:
            msg_err = ' The password is invalid. Please, try again!'
            return False, msg_err
    else:
        msg_err = ' The password must have more than 8 characters. Please, try again!'
        return False, msg_err


def validate_pwd(pwd):
    """
    # Função que valida a senha do associado
    # verifica se os valores informados possuem mais do que 8 caracteres,
    # senão envia uma mensagem para o usuário
    :param pwd:'teste1234'
    :return:True
    """
    if len(pwd) >= 8:
        return True
    else:
        return False


def verify_domain(s_domain):
    """
    # Função que verifica se existe o domínio informado pelo associado e retorna o id
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param s_domain:'asparona'
    :return: True, iddomain
    """
    domain = s_domain
    s_sql = "SELECT id_domain, domain FROM tDomain WHERE domain = '" + str(domain) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                (id_domain, domain) = bd.fetchone()
                return True, id_domain
            else:
                return False, None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def verify_assoc_id(name_user):
    """
    # Função que verifica se existe o associado informado pelo nome e retorna o id
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param name_user:'Laercio Serra'
    :return: True, idassoc
    """
    assoc = name_user
    s_sql = "SELECT id_user FROM tUser WHERE name_user = '" + assoc + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                (id_assoc) = bd.fetchone()
                return True, id_assoc[0]
            else:
                return False, None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def add_newacct(acct, domain):
    """
    # Função que retorna se os dados do novo account foi gravado  na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param acct: 'Cash'
    :param domain: 'asparona'
    :return acct_added: 'True/False'
    :return erro_msg: 'Account já existe na base de dados'
    """
    try:
        msg_err = abrir_bd()

        if msg_err != '' and msg_err is not None:
            raise MySQLdb.Error(msg_err)
        else:
            # INSERT VALUES na tAccount
            s_sql = "INSERT INTO tAccount(name_account, domain) VALUES('" + acct + "','" + domain + "');"

            bd.execute(s_sql)

            # Confirma a transação de inserção de registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                raise MySQLdb.Error(msg_err)
            else:
                return True, msg_err

    except MySQLdb.IntegrityError, e:
        if conn:
            rollback_bd()

        error_msg = " %d - %s" % (e.args[0], e.args[1])
        return False, error_msg

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def delete_acct(adel):
    """
    # Função que exclui os dados do account no sistema
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param adel: 'Cash'
    :return: True, msg_err
    """
    s_sql = "DELETE FROM tAccount WHERE name_account = '" + str(adel) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            # exclui os dados do account
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                # Confirma a transação de exclusão do account no banco de dados
                msg_err = commit_bd()
                if msg_err != '' and msg_err is not None:
                    raise MySQLdb.Error(msg_err)
                else:
                    return True, None
            else:
                return False, ' None account was deleted!'

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def edit_acct(acct):
    """
    # Função que retorna o id do account para edição
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param acct: 'Cash'
    :return: name_account
    """
    s_sql = "SELECT id_account " \
            "FROM tAccount WHERE name_account = '" + acct + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                id_account = bd.fetchone()
                return id_account[0]
            else:
                return None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def update_acct(idacct, acct):
    """
    # Função que atualiza os dados do account na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de update no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param idacct: '12'
    :param acct: 'Cash'
    :return acct_edited: 'True'
    :return s_erromsg: error_msg
    """
    s_sql = "UPDATE tAccount SET " \
            "name_account = '" + acct + "' WHERE id_account = '" + str(idacct) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Confirma a transação de update do registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                return True, msg_err

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_all_cat(domain):
    """
    # Função que retorna as categorias cadastradas
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain: 'asparona'
    :return: {fields, rs_dt_table}
    """
    s_sql = "SELECT name_category FROM tCategory WHERE domain = '" + domain + "';"

    fields = ('Category',)

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return fields, None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                rs_dt_table = bd.fetchall()
                return fields, rs_dt_table, msg_err
            else:
                rs_dt_table = None
                return fields, rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return fields, None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def add_newcat(cat, domain):
    """
    # Função que retorna se os dados do novo category foi gravado na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param cat: 'Restaurant'
    :param domain: 'asparona'
    :return cat_added: 'True/False'
    :return erro_msg: 'Category já existe na base de dados'
    """
    try:
        msg_err = abrir_bd()

        if msg_err != '' and msg_err is not None:
            raise MySQLdb.Error(msg_err)
        else:
            # INSERT VALUES na tCategory
            s_sql = "INSERT INTO tCategory(name_category, domain) VALUES('" + cat + "','" + domain + "');"

            bd.execute(s_sql)

            # Confirma a transação de inserção de registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                raise MySQLdb.Error(msg_err)
            else:
                return True, msg_err

    except MySQLdb.IntegrityError, e:
        if conn:
            rollback_bd()

        error_msg = " %d - %s" % (e.args[0], e.args[1])
        return False, error_msg

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def edit_cat(cat):
    """
    # Função que retorna o id do category para edição
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param cat: 'Restaurant'
    :return: name_category
    """
    s_sql = "SELECT id_category " \
            "FROM tCategory WHERE name_category = '" + cat + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                id_category = bd.fetchone()
                return id_category[0]
            else:
                return None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def update_cat(idcat, cat):
    """
    # Função que atualiza os dados do category na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de update no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param idcat: '12'
    :param cat: 'Restaurant'
    :return cat_edited: 'True'
    :return s_erromsg: error_msg
    """
    s_sql = "UPDATE tCategory SET " \
            "name_category = '" + cat + "' WHERE id_category = '" + str(idcat) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Confirma a transação de update do registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                return True, msg_err

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_cat_from_id(idcat):
    """
    # Função que retorna o category cadastrado
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param idcat: '1'
    :return: s_cat_new
    """
    s_sql = "SELECT name_category FROM tCategory WHERE id_category = '" + idcat + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                s_category = bd.fetchone()
                return s_category[0], msg_err
            else:
                return None, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def delete_cat(cdel):
    """
    # Função que exclui os dados do category no sistema
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param cdel: 'Restaurant'
    :return: True, msg_err
    """
    s_sql = "DELETE FROM tCategory WHERE name_category = '" + cdel + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            # exclui os dados do category
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                # Confirma a transação de exclusão do category no banco de dados
                msg_err = commit_bd()
                if msg_err != '' and msg_err is not None:
                    raise MySQLdb.Error(msg_err)
                else:
                    return True, None
            else:
                return False, ' None category was deleted!'

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_all_cstr(domain):
    """
    # Função que retorna os Customers cadastrados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain: 'asparona'
    :return: {fields, rs_dt_table}
    """
    s_sql = "SELECT name_Customer FROM tCustomer WHERE domain = '" + domain + "';"

    fields = ('Customer',)

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return fields, None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                rs_dt_table = bd.fetchall()
                return fields, rs_dt_table, msg_err
            else:
                rs_dt_table = None
                return fields, rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return fields, None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def add_newcstr(cstr, domain):
    """
    # Função que retorna se os dados do novo customer foi gravado na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param cstr: 'Tivit'
    :param domain: 'asparona'
    :return cstr_added: 'True/False'
    :return erro_msg: 'Customer já existe na base de dados'
    """
    try:
        msg_err = abrir_bd()

        if msg_err != '' and msg_err is not None:
            raise MySQLdb.Error(msg_err)
        else:
            # INSERT VALUES na tCustomer
            s_sql = "INSERT INTO tCustomer(name_customer, domain) VALUES('" + cstr + "','" + domain + "');"

            bd.execute(s_sql)

            # Confirma a transação de inserção de registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                raise MySQLdb.Error(msg_err)
            else:
                return True, msg_err

    except MySQLdb.IntegrityError, e:
        if conn:
            rollback_bd()

        error_msg = " %d - %s" % (e.args[0], e.args[1])
        return False, error_msg

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def edit_cstr(cstr):
    """
    # Função que retorna o id do customer para edição
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param cstr: 'Tivit'
    :return: name_customer
    """
    s_sql = "SELECT id_customer " \
            "FROM tCustomer WHERE name_customer = '" + cstr + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                id_customer = bd.fetchone()
                return id_customer[0]
            else:
                return None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def update_cstr(idcstr, cstr):
    """
    # Função que atualiza os dados do customer na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de update no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param idcstr: '12'
    :param cstr: 'Tivit'
    :return cstr_edited: 'True'
    :return s_erromsg: error_msg
    """
    s_sql = "UPDATE tCustomer SET " \
            "name_customer = '" + cstr + "' WHERE id_customer = '" + str(idcstr) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Confirma a transação de update do registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                return True, msg_err

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_cstr_from_id(idcstr):
    """
    # Função que retorna o customer cadastrado
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param idcstr: '1'
    :return: s_customer
    """
    s_sql = "SELECT name_customer FROM tCustomer WHERE id_customer = '" + str(idcstr) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                s_customer = bd.fetchone()
                return s_customer[0], msg_err
            else:
                return None, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def delete_cstr(cdel):
    """
    # Função que exclui os dados do customer no sistema
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param cdel: '1'
    :return: True, msg_err
    """
    s_sql = "DELETE FROM tCustomer WHERE name_customer = '" + cdel + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            # exclui os dados do customer
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                # Confirma a transação de exclusão do customer no banco de dados
                msg_err = commit_bd()
                if msg_err != '' and msg_err is not None:
                    raise MySQLdb.Error(msg_err)
                else:
                    return True, None
            else:
                return False, ' None customer was deleted!'

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_all_proj(domain):
    """
    # Função que retorna os projects cadastrados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain: 'asparona'
    :return: {fields, rs_dt_table}
    """
    s_sql = "SELECT name_project FROM tProject WHERE domain = '" + domain + "';"

    fields = ('Project',)

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return fields, None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                rs_dt_table = bd.fetchall()
                return fields, rs_dt_table, msg_err
            else:
                rs_dt_table = None
                return fields, rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return fields, None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def add_newproj(proj, domain):
    """
    # Função que retorna se os dados do novo project foi gravado na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param proj: 'Tivit BIRH'
    :param domain: 'asparona'
    :return proj_added: 'True/False'
    :return erro_msg: 'Project já existe na base de dados'
    """
    try:
        msg_err = abrir_bd()

        if msg_err != '' and msg_err is not None:
            raise MySQLdb.Error(msg_err)
        else:
            # INSERT VALUES na tProject
            s_sql = "INSERT INTO tProject(name_project, domain) VALUES('" + proj + "','" + domain + "');"

            bd.execute(s_sql)

            # Confirma a transação de inserção de registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                raise MySQLdb.Error(msg_err)
            else:
                return True, msg_err

    except MySQLdb.IntegrityError, e:
        if conn:
            rollback_bd()

        error_msg = " %d - %s" % (e.args[0], e.args[1])
        return False, error_msg

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def edit_proj(proj):
    """
    # Função que retorna o id do project para edição
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param proj: 'Tivit'
    :return: name_project
    """
    s_sql = "SELECT id_project " \
            "FROM tProject WHERE name_project = '" + proj + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                id_project = bd.fetchone()
                return id_project[0]
            else:
                return None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def update_proj(idproj, proj):
    """
    # Função que atualiza os dados do project na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de update no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param idproj: '12'
    :param proj: 'Tivit BIRH'
    :return proj_edited: 'True'
    :return s_erromsg: error_msg
    """
    s_sql = "UPDATE tProject SET " \
            "name_project = '" + proj + "' WHERE id_project = '" + str(idproj) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Confirma a transação de update do registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                return True, msg_err

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_proj_from_id(idproj):
    """
    # Função que retorna o project cadastrado
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param idproj: '1'
    :return: s_project
    """
    s_sql = "SELECT name_project FROM tProject WHERE id_project = '" + str(idproj) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                s_project = bd.fetchone()
                return s_project[0], msg_err
            else:
                return None, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def delete_proj(pdel):
    """
    # Função que exclui os dados do project no sistema
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param pdel: '1'
    :return: True, msg_err
    """
    s_sql = "DELETE FROM tProject WHERE name_project = '" + pdel + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            # exclui os dados do project
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                # Confirma a transação de exclusão do project no banco de dados
                msg_err = commit_bd()
                if msg_err != '' and msg_err is not None:
                    raise MySQLdb.Error(msg_err)
                else:
                    return True, None
            else:
                return False, ' None project was deleted!'

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_all_curr(domain):
    """
    # Função que retorna os currency cadastrados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um currsor para se comunicar através da conexão com os dados
    # 3- usando o currsor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param domain: 'asparona'
    :return: {fields, rs_dt_table}
    """
    s_sql = "SELECT code, description, sign FROM tCurrency WHERE domain = '" + domain + "';"

    fields = ('Code', 'Description', 'Sign')

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return fields, None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                rs_dt_table = bd.fetchall()
                return fields, rs_dt_table, msg_err
            else:
                rs_dt_table = None
                return fields, rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return fields, None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def edit_curr(curr):
    """
    # Função que retorna os dados do currency para edição
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param curr: 'BRL'
    :return: id_currency
    :return: description
    :return: sign
    """
    s_sql = "SELECT id_currency, description, sign " \
            "FROM tCurrency WHERE code = '" + curr + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                id_currency, description, sign = bd.fetchone()
                return id_currency, description, sign
            else:
                return None, None, None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def update_curr(curr, desc, sign, i_curr, domain):
    """
    # Função que atualiza os dados do currency na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de update no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param curr: 'BRL'
    :param desc: 'Brazilian Real'
    :param sign: 'R$'
    :param i_curr: '1'
    :param domain: 'asparona'
    :return curr_edited: 'True'
    :return s_erromsg: error_msg
    """
    s_sql = "UPDATE tCurrency SET " \
            "code = '" + curr + "'," \
            "description = '" + desc + "'," \
            "sign = '" + sign + "' " \
            "WHERE id_currency = '" + str(i_curr) + "' " \
            "AND domain = '" + domain + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Confirma a transação de update do registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                return True, msg_err

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def get_curr_from_id(idcurr):
    """
    # Função que retorna o currency cadastrado
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param idcurr: '1'
    :return: s_curr
    :return: s_desc
    :return: s_sign
    :return: s_erromsg_g
    """
    s_sql = "SELECT code, description, sign FROM tCurrency WHERE id_currency = '" + str(idcurr) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return None, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                s_curr, s_desc, s_sign = bd.fetchone()
                return s_curr, s_desc, s_sign, msg_err
            else:
                return None, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return None, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def add_newcurr(curr, desc, sign, domain):
    """
    # Função que retorna se os dados do novo currency foi gravado na base de dados
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param curr: 'BRL'
    :param desc: 'Brazilian Real'
    :param sign: 'R$'
    :param domain: 'asparona'
    :return curr_added: 'True/False'
    :return erro_msg: 'Currency já existe na base de dados'
    """
    try:
        msg_err = abrir_bd()

        if msg_err != '' and msg_err is not None:
            raise MySQLdb.Error(msg_err)
        else:
            # INSERT VALUES na tCurrency
            s_sql = "INSERT INTO tCurrency (code, description, sign, domain) " \
                    "VALUES('" + curr + "','" + desc + "','" + sign + "','" + domain + "');"

            bd.execute(s_sql)

            # Confirma a transação de inserção de registro no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                raise MySQLdb.Error(msg_err)
            else:
                return True, msg_err

    except MySQLdb.IntegrityError, e:
        if conn:
            rollback_bd()

        error_msg = " %d - %s" % (e.args[0], e.args[1])
        return False, error_msg

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()


def delete_curr(cdel):
    """
    # Função que exclui os dados do currency no sistema
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param cdel: '1'
    :return: True, msg_err
    """
    s_sql = "DELETE FROM tCurrency WHERE code = '" + cdel + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            # exclui os dados do currency
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                # Confirma a transação de exclusão do currency no banco de dados
                msg_err = commit_bd()
                if msg_err != '' and msg_err is not None:
                    raise MySQLdb.Error(msg_err)
                else:
                    return True, None
            else:
                return False, ' None currency was deleted!'

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn is not None:
            fechar_bd()