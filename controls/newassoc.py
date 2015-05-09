#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

"""
Created on 22/05/2014
@author: Laércio Serra (laercio.serra@gmail.com)
"""

# O módulo CGI pega todos os dados do formulário e coloca-os em um dicionário
import cgi


# Este módulo faz parte da biblioteca padrão do Python e faz um ratreamento CGI
# que, quando ativado, organiza as mensagens de erros detalhadas que aparecem
# no navegador
import cgitb  # chama o módulo de rastreamento de erros do CGI


cgitb.enable()  # ativa o módulo para que os erros possam aparecer no browser
form_data = cgi.FieldStorage()  # obter os dados de login do associado
s_firstname = form_data.getvalue('first_name')  # pega o valor do campo first_name
s_last_name = form_data.getvalue('last_name')  # pega o valor do campo last_name
s_domain = form_data.getvalue('domain')  # pega o valor do campo domain
s_email = form_data.getvalue('email')   # pega o valor do campo email
s_senha = form_data.getvalue('password')   # pega o valor do campo senha
s_senha_c = form_data.getvalue('password_confirmation')   # pega o valor do campo confirmação de senha


s_nameuser = str.capitalize(s_firstname) + ' ' + str.capitalize(s_last_name)


import time  # funções de manipulação de data e hora do sistema
import golias  # funções de segurança e regras do negócio
import mysf  # funções de renderização e output


s_date = time.localtime()  # Captura os dados de data/hora do sistema
s_date = time.strftime("%A %d, %B %Y", s_date)  # Formatação da data: Monday 01, September 2014


def output_page_a(code_err, err_msg):
    """
    # Função para deixar o código mais estruturado e limpo
    # esta função renderiza a saída da página "register.html"
    :param code_err:'3'
    :param err_msg:' Você informou um e-mail inválido! Por favor, tente novamente.'
    """
    print (mysf.include_start_response())
    print (mysf.include_header_reg())
    print (mysf.include_messages(code_err, err_msg))
    print (mysf.include_form_reg())
    print (mysf.include_footer_reg())


# def output_page_b(code_err, err_msg):
#     """
#     # Função para deixar o código mais estruturado e limpo
#     # esta função renderiza a saída da página "register.html"
#     :param code_err:'3'
#     :param err_msg:' Você informou um e-mail inválido! Por favor, tente novamente.'
#     """
#     print (mysf.include_start_response())
#     print (mysf.include_header_reg())
#     print (mysf.include_messages(code_err, err_msg))
#     print (mysf.include_form_reg())
#     print (mysf.include_footer_reg())


def output_page_c():
    """
    # Função para deixar o código mais estruturado e limpo
    # esta função renderiza a saída da página "mthreef.html"
    """
    print (mysf.include_start_response())
    print (mysf.include_header())
    print (mysf.include_user(s_domain, s_nameuser, str.lower(s_email), s_date))
    print (mysf.include_logout())
    print (mysf.include_div_s())
    print (mysf.include_messages('2', ' Welcome to Expenses Report!'))
    print (mysf.include_pageheader('Expenses ', ' Last payments'))
    print (mysf.include_search_form())
    print (mysf.include_table())
    print (mysf.include_pagination())
    print (mysf.include_div_e())
    print (mysf.include_footer())


# verifica se o usuário informou uma senha com mais de 7 caracteres
if s_senha is not None and len(s_senha) >= 8:
    if s_senha == s_senha_c:  # verifica se as senhas são as mesmas
        (is_email) = golias.validate_email(s_email)  # verifica se o endereço de e-mail informado pelo usuario é válido
        if is_email:
            (is_assoc, s_errormsg) = golias.get_assoc_from_id(s_email)  # verifica se o usuário já é um associado
            if is_assoc:
                if s_errormsg != '' and s_errormsg is not None:
                    s_code_err = '1'
                    output_page_a(s_code_err, s_errormsg)
                else:
                    s_code_err = '4'
                    s_err_msg = " You don't need a register because you're already registered!"
                    output_page_a(s_code_err, s_err_msg)
            else:
                s_senha_crypt = golias.assoc_pwd_crypto(s_senha)  # codifica a senha do associado antes de gravar no bd
                (is_inserted, s_errormsg) = golias.put_assoc_from_id(s_domain, s_nameuser, s_email, s_senha_crypt)
                if is_inserted:
                    # renderiza a página principal do sistema
                    output_page_c()
                else:
                    s_code_err = '1'
                    output_page_a(s_code_err, s_errormsg)
        else:
            s_code_err = '3'
            s_err_msg = ' Invalid e-mail. Please, try again!'
            output_page_a(s_code_err, s_err_msg)
    else:
        s_code_err = '3'
        s_err_msg = ' Invalid password. The password must have more than 8 characters. Please, try again!'
        output_page_a(s_code_err, s_err_msg)
else:
    s_code_err = '3'
    s_err_msg = ' Invalid password. The password must have more than 8 characters. Please, try again!'
    output_page_a(s_code_err, s_err_msg)