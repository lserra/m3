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


def abrir_bd():
    """
    # Esta função utiliza o módulo Mysqldb que contem a API de comunicação com o Mysql.
    # É preciso informar o usuário e senha que foi configurado no Mysql nesse momento.
    """
    global conn, bd

    try:
        conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="cycleclub")
        bd = conn.cursor()
    except MySQLdb.Error, e:
        error_msg = "Falha na conexão com o banco de dados. Erro %d: %s" % (e.args[0], e.args[1])
        return error_msg


def fechar_bd():
    """
    # Esta função utiliza o módulo Mysqldb que contem a API de comunicação com o Mysql.
    """
    conn.close()


def commit_bd():
    """
    # Esta função utiliza o módulo Mysqldb que contem a API de comunicação com o Mysql.
s   """
    try:
        conn.commit()
    except MySQLdb.Error, e:
        error_msg = "Falha na conexão com o banco de dados. Erro %d: %s" % (e.args[0], e.args[1])
        return error_msg


def rollback_bd():
    """
    # Esta função utiliza o módulo Mysqldb que contem a API de comunicação com o Mysql.
s   """
    try:
        conn.rollback()
    except MySQLdb.Error, e:
        error_msg = "Falha na conexão com o banco de dados. Erro %d: %s" % (e.args[0], e.args[1])
        return error_msg


# Função que valida se o e-mail informado pelo usuário é válido
def validate_email(address):
    # verifica se o usuário digitou algum e-mail
    if address == '' or address is None:
        address = "-@-"

    # to not allow single letter parts increase len_limit to 2 or more
    # len_limit, max_domain = 1, 4
    # acceptable in left side in username
    # accept_username = '_-'
    # only ascii values not all alpha
    # sep = [code for code in address if ((not code.isalpha() and code not in accept_username)
    #                                     or ord(code) > 128)]
    # if (  # sep joined must be ..@.... form
    #       ''.join(sep).strip('.') != '@' or sep[-1].strip() == '@'):  # must have point after @
    #     return False
    # else:
    #     end = address
    #     for s in sep:
    #         part, s, end = end.partition(s)
    #         if len(part) < len_limit:
    #             return False
    #
    # return max_domain >= len(end) > 1  # retorna true ou false

    """ from http://www.regular-expressions.info/email.html """
    pattern = r"\b[a-zA-Z0-9._%+-]*[a-zA-Z0-9_%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b"
    if re.match(pattern, address):
        return True
    else:
        return False


# Funcão que verifica se o usuário já é um associado
def get_assoc_from_id(email):
    """
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - pega o resultset como uma tupla
    # 4- fechar a conexão com o banco de dados
    :param email: 'laercio.serra@gmail.com'
    :return:
    """
    global idassoc, emailassoc, pwdassoc

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            s_sql = "select idassoc, emailassoc, pwdassoc from TB_ASSOC where emailassoc='" + str(email) + "';"
            bd.execute(s_sql)
            # Pega o número de linhas no resultset
            numrows = int(bd.rowcount)

            if numrows > 0:
                (idassoc, emailassoc, pwdassoc) = bd.fetchone()
                return True, msg_err
            else:
                return False, msg_err

    except MySQLdb.Error, e:
        error_msg = "Falha na conexão com o banco de dados. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        fechar_bd()


# Funcão que inclui o associado em nosso banco de dados
def put_assoc_from_id(email, pwd):
    """
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de insert no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param email: 'laercio.serra@gmail.com'
    :param pwd: '1234'
    :return:
    """
    s_email = email
    s_pwd = pwd
    s_status = 'S'
    s_regra = 'N'

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            s_sql = "INSERT INTO TB_ASSOC (emailassoc, pwdassoc, status, regra) "
            s_sql += "VALUES ('" + str(s_email) + "', '" + str(s_pwd) + "', '" + str(s_status) + "', '" + \
                     str(s_regra) + "');"
            bd.execute(s_sql)
            # Confirma a transação de inserção de registros no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                return True, msg_err

    except MySQLdb.Error, e:
        error_msg = "Falha na conexão com o banco de dados. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        fechar_bd()


def update_status_assoc(s_id, s_regra="S"):
    """
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de update no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param s_id: '17'
    :param s_regra: 'Concordo'
    :return:
    """
    id_assoc = s_id
    regra = s_regra

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            s_sql = "UPDATE TB_ASSOC SET regra='" + regra + "' "
            s_sql += "WHERE idassoc='" + str(id_assoc) + "';"
            bd.execute(s_sql)
            # Confirma a transação de inserção de registros no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                return True, msg_err

    except MySQLdb.Error, e:
        error_msg = "Falha na conexão com o banco de dados. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        fechar_bd()


# Função que valida o acesso ao sistema (autenticação)
def auth_assoc(email, pwd):
    """
    # valida o e-mail e a senha do associado
    :param email: 'laercio.serra@gmail.com'
    :param pwd: '1234'
    :return: true/false
    """
    decrypt = assoc_pwd_decrypto(pwdassoc)
    decrypt = unicode(decrypt, 'utf-8')

    if email == emailassoc and pwd == decrypt:
        return True
    else:
        return False


def return_data_assoc():
    """
    # Função que retorna os dados do associado
    :return: idassoc, emailassoc, pwdassoc
    """
    return idassoc, emailassoc, pwdassoc


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
    # descodifica a senha do associado
    :param s_pwd: %$(@!
    :return: '1234'
    """
    cipher_text = s_pwd.decode('base64', 'strict')

    return cipher_text


# Função que envia os dados de login do associado por email
def send_login_assoc(s_email, s_pwd):
    """
    # conecta-se a um servidor do gmail para enviar os dados de login
    # do associado por e-mail
    :param s_email:'laercio.serra@gmail.com'
    :param s_pwd:'1234'
    """
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = '587'
        msg_err = ''

        sender = 'laercio.serra@neotrend.com.br'  # trocar pelo endereço de email: admin@cycleclub.com

        subject = '[CYCLECLUB]-Login'

        header = 'To:' + s_email + '\n' + 'From: ' + sender + '\n' + 'Subject:' + subject + '\n'

        body = 'Caro Associado,\n\n'
        body += 'Estamos enviando para você os seus dados de acesso (login) ao CYCLECLUB.\r\n\r\n'
        body += 'login = ' + s_email + '\r\n'
        body += 'senha = ' + s_pwd + '\r\n\r\n'
        body += 'Att,\n\n'
        body += 'CYCLECLUB\r'
        body += '-----------------------------------------------------------------------\r'
        body += 'Se você não solicitou esta verificação, você deve ignorar este e-mail.'

        msg = header + '\n' + body

        session = smtplib.SMTP(smtp_server, smtp_port)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login('laercio.serra@neotrend.com.br', 'lS071134')  # trocar pelo endereço de email: admin@cycleclub.com
        session.sendmail(sender, s_email, msg)
        session.quit()

        return True, msg_err

    except smtplib.SMTPException:
        error_msg = "Falha ao enviar email."
        return False, error_msg


# Função que envia os dados de login do associado por email
def send_message(nome, email, motivo, descmotivo):
    """
    # conecta-se a um servidor do gmail para enviar a mensagem
    # deixada através da página 'contato.html'
    :param nome:'Laercio Serra'
    :param email:'laercio.serra@gmail.com'
    :param motivo:'Reclamação'
    :param descmotivo:'problema de autenticação'
    """
    s_nome = nome
    s_email = email
    s_motivo = motivo
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = '587'
        msg_err = ''

        sender = 'laercio.serra@neotrend.com.br'  # trocar pelo endereço de email: admin@cycleclub.com

        subject = '[CYCLECLUB]-' + s_motivo

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
        session.login('laercio.serra@neotrend.com.br', 'lS071134')  # trocar pelo endereço de email: admin@cycleclub.com
        session.sendmail(sender, 'laercio.serra@gmail.com', msg)
        session.quit()

        return True, msg_err

    except smtplib.SMTPException:
        error_msg = "Falha ao enviar email."
        return False, error_msg


# Função que valida a alteração de senha
def validate_newpwd(pwd1, pwd2):
    """
    # verifica se os valores informados possuem mais do que 8 caracteres,
    # em seguida verifica as novas senhas e compara estes valores
    # se os valores forem iguais a nova senha está correta
    # senão envia uma mensagem para o usuário
    :param pwd1:'teste1234'
    :param pwd2:'teste1234'
    """
    msg_err = None

    if (len(pwd1) >= 8) and (len(pwd2) >= 8):
        if pwd1 == pwd2:
            return True, msg_err
        else:
            msg_err = ' As senhas não conferem. Por favor, tente novamente.'
            return False, msg_err
    else:
        msg_err = ' A senha deve ter no mínimo 8 caracteres. Por favor, tente novamente.'
        return False, msg_err


# Função que altera a senha do associado no banco de dados
def update_login_assoc(s_email, s_pwd):
    """
    # 1- estabelece uma conexão com o banco de dados
    # 2- criar um cursor para se comunicar através da conexão com os dados
    # 3- usando o cursor, manipula os dados usando o sql
    # 3.1 - confirma a transação de update no banco de dados
    # 4- fechar a conexão com o banco de dados
    :param s_email:'laercio.serra@gmail.com'
    :param s_pwd:'teste1234'
    :return:
    """
    login = s_email
    new_pwd = s_pwd

    try:
        msg_err = abrir_bd()
        if msg_err != '' and msg_err is not None:
            return False, msg_err
        else:
            s_sql = "UPDATE TB_ASSOC SET pwdassoc='" + str(new_pwd) + "' "
            s_sql += "WHERE emailassoc='" + login + "';"
            bd.execute(s_sql)
            # Confirma a transação de inserção de registros no banco de dados
            msg_err = commit_bd()
            if msg_err != '' and msg_err is not None:
                return False, msg_err
            else:
                return True, msg_err

    except MySQLdb.Error, e:
        error_msg = "Falha na conexão com o banco de dados. Erro %d: %s" % (e.args[0], e.args[1])
        return False, error_msg

    finally:
        fechar_bd()
