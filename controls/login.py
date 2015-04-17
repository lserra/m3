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

s_domain = form_data.getvalue('domain')  # pega o valor do campo email
s_email = form_data.getvalue('email')  # pega o valor do campo email
s_senha = form_data.getvalue('password')  # pega o valor do campo senha


import time  # funções de manipulação de data e hora do sistema
import mysf  # funções de renderização e output
import golias  # funções de segurança e regras do negócio


s_date = time.localtime()  # Captura os dados de data/hora do sistema
s_date = time.strftime("%A %d, %B %Y", s_date)  # Formatação da data: Monday 01, September 2014


def render_mthree_html(domain, nameuser, emailassoc, date, fields, dt_tb):
    """
    # Renderiza a página principal 'mthree.html'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@gmail.com'
    :param date: '12/01/2015'
    :param fields: {'a', 'b', 'c'}
    :param dt_tb: {(value1, value2, value3), (value4, value5, value6), (value7, value8, value9)}
    """
    print (mysf.include_start_response())
    print (mysf.include_header())
    print (mysf.include_user(domain, nameuser, emailassoc, date))
    print (mysf.include_logout())
    print (mysf.include_div_s())
    print (mysf.include_messages('2', ' Welcome to My Expenses Report!'))
    print (mysf.include_pageheader('Expenses ', ' Last payments'))
    print (mysf.include_search_form())
    if dt_tb is None:
        print (mysf.include_data_table(fields))
    else:
        print (mysf.include_data_table_enable(domain, fields, dt_tb))
    print (mysf.include_pagination())
    # print (mysf.include_delete())
    print (mysf.include_div_e())
    print (mysf.include_footer())


def render_login_html(code, err_msg):
    """
    # Renderiza a página login 'login.html'
    :param code: '1'
    :param err_msg: 'Database error connection'
    """
    print (mysf.include_start_response())
    print (mysf.include_login())
    print (mysf.include_messages(code, err_msg))
    print (mysf.include_form_login())
    print (mysf.include_footer_login())


s_field = 1
n_field = []
s_f_msg = None

# valida se o campo dominio foi informado pelo usuário
if s_domain is None:
    s_field = 0
    n_field.append('D')
    s_f_msg = ' Data field required!'
    s_domain = 'required'
# else:
#     s_domain = str.lower(s_domain)
#     (is_domain, s_id_domain) = golias.verify_domain(s_domain)
#     if is_domain is False:
#         s_field = 0
#         n_field.append('D')
#         s_f_msg = ' Data value invalid. Please, try again!'
#         s_domain = None

# valida se o campo email foi informado pelo usuário
if s_email is None:
    s_field = 0
    n_field.append('E')
    s_f_msg = ' Data field required!'
    s_email = 'required'
else:
    # verifica se o endereço de e-mail informado pelo usuario é válido
    (is_email) = golias.validate_email(s_email)
    if is_email is False:
        s_field = 0
        n_field.append('E')
        s_f_msg = ' Data value invalid. Please, try again!'
        s_email = 'name@domain.com'

# valida se o campo password foi informado pelo usuário
if s_senha is None:
    s_field = 0
    n_field.append('P')
    s_f_msg = ' Data field required!'
    s_senha = None
else:
    # verifica se a senha informada pelo usuario é válido
    (is_pwd) = golias.validate_pwd(s_senha)
    if is_pwd is False:
        s_field = 0
        n_field.append('P')
        s_f_msg = ' Data value invalid. Please, try again!'
        s_senha = None

# TODO: fazer testes contra ataques de SQL injection
# valida se todos os campos foram preenchidos
if s_field != 0:
    # verifica se o domínio informado é válido
    s_domain = str.lower(s_domain)
    (is_domain, s_id_domain) = golias.verify_domain(s_domain)
    # verifica se o email é de um associado válido
    (is_assoc, s_errormsg_ga) = golias.get_assoc_from_id(s_email)
    # verifica se o usuário está associado ao domínio informado e se são válidos
    (is_valid, s_errormsg_gd) = golias.get_domain_assoc(s_id_domain, s_email)
    # se é um domínio é válido
    if is_domain:
        # se é um associado válido
        if is_assoc:
            # se o domínio e o associado são válidos
            if is_valid:
                # autentica o associado para acessar o sistema
                (is_authenticated) = golias.auth_assoc(s_email, s_senha)
                # se foi autenticado
                if is_authenticated:
                    # TODO: criar uma função que verifica o número de tentativas e bloqueia o acesso após +3 tentativas
                    s_idassoc, s_iddomain, s_nameuser, s_emailassoc, s_pwdassoc = golias.return_data_assoc()
                    s_fields, s_dt_tb, s_errormsg_le = golias.list_expenses_payments_accepted(s_idassoc)
                    if s_errormsg_le is None:
                        render_mthree_html(s_domain, s_nameuser, str.lower(s_emailassoc), s_date, s_fields, s_dt_tb)
                    else:
                        s_type = '4'
                        render_login_html(s_type, s_errormsg_le)
                else:
                    s_type = '1'
                    s_err_msg = ' E-mail or password invalid. The password must have more than 8 characters. ' \
                                'Please, try again!'
                    render_login_html(s_type, s_err_msg)
            else:
                s_type = '4'
                s_err_msg = ' Domain and User invalid. Please, try again or create a register!'
                if s_errormsg_ga is None:
                    render_login_html(s_type, s_err_msg)
                else:
                    render_login_html(s_type, s_errormsg_gd)
        else:
            s_type = '4'
            s_err_msg = ' User invalid. Please, try again or create a register!'
            if s_errormsg_ga is None:
                render_login_html(s_type, s_err_msg)
            else:
                render_login_html(s_type, s_errormsg_ga)
    else:
        s_type = '4'
        s_err_msg = ' Domain invalid. Please, try again or create a register!'
        render_login_html(s_type, s_err_msg)
else:
    print (mysf.include_login())
    print (mysf.include_messages('3', s_f_msg))
    print (mysf.include_form_login_err(n_field))
    print (mysf.include_footer_login())