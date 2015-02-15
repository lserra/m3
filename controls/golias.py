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


def add_newuser(domain, name, email, pwd, profile):
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
    :return user_added: 'True/False'
    :return erro_msg: 'Usuário já existe na base de dados'
    """
    try:
        # 1- criptografar a senha
        pwd_newuser = assoc_pwd_crypto(pwd)

        # 2- INSERT VALUES na tbUser
        (user_added, error_msg) = put_assoc_from_id(domain, name, email, pwd_newuser)

        # verifica se o bd não retornou algum erro, então INSERT VALUES na tbMatrix
        if user_added is True:
            # 3- INSERT VALUES na tbMatrix
            (matrix_added, error_msg) = put_assoc_matrix(name, profile)

            # verifica se o bd não retornou algum erro
            if matrix_added is True:
                user_added = matrix_added
                return user_added, error_msg
            else:
                user_added = matrix_added
                return user_added, error_msg
        else:
            return user_added, error_msg

    except MySQLdb.Error, e:
        if conn:
            rollback_bd()

        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn:
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


def fechar_bd():
    """
    # Esta função utiliza o módulo Mysqldb que contem a API de comunicação com o Mysql.
    """
    conn.close()


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
    s_sql = "SELECT u.name_user, u.email_user, m.profile_user " + \
            "FROM tDomain d, tUser u, tMatrix m WHERE d.id_domain = u.id_domain AND m.id_user = u.id_user AND " + \
            "d.domain='" + str(domain_name) + "';"

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                (fields) = ('Name', 'Email', 'Profile')
                (rs_dt_table) = bd.fetchall()
                return fields, rs_dt_table, msg_err
            else:
                (fields) = ('Name', 'Email', 'Profile')
                (rs_dt_table) = None
                return fields, rs_dt_table, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn:
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
        if conn:
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
        if conn:
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
        if conn:
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
                return None, None, msg_err

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn:
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
    :return:is_domain, s_iddomain
    """
    s_domain = str.lower(domain)
    s_email = str.lower(email)

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            (is_domain, id_domain) = verify_domain(s_domain)  # verifica a existência do domínio informado
            if is_domain:
                s_sql = "INSERT INTO tUser (id_domain, name_user, email_user, password, new_user) " \
                        "VALUES ('" + str(id_domain) + "', '" + str(name_user) + "', '" + str(s_email) + "', '" + \
                        str(pwd) + "', 'S');"

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
                        "VALUES ('" + str(id_assoc) + "', '" + profile + "', 'NULL');"

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
        if conn:
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
        if conn:
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
        if conn:
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
        if conn:
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
        if conn:
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
        if conn:
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
                return True, id_assoc
            else:
                return False, None

    except MySQLdb.Error, e:
        error_msg = "Database connection failure. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        if conn:
            fechar_bd()