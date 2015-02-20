#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

"""
Created on 14/06/2014
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

s_domain_newuser = form_data.getvalue('domain_nu')  # pega o valor do campo domain
s_fname_newuser = form_data.getvalue('fname')  # pega o valor do campo fname
s_lname_newuser = form_data.getvalue('lname')  # pega o valor do campo lname
s_email_newuser = form_data.getvalue('email')  # pega o valor do campo email
s_pwd_newuser = form_data.getvalue('pwd')  # pega o valor do campo pwd
s_profile_newuser = form_data.getvalue('profile')  # pega o valor do campo profile
s_task_newuser = form_data.getvalue('task')  # pega o valor do campo task

s_domain = form_data.getvalue('domain')  # pega o valor do campo domain
s_user = form_data.getvalue('nameuser')  # pega o valor do campo nameuser
s_email = form_data.getvalue('emailassoc')  # pega o valor do campo emailassoc

import time  # funções de manipulação de data e hora do sistema
import mysf  # funções de renderização e output
import golias  # funções de segurança e regras do negócio


s_date = time.localtime()  # Captura os dados de data/hora do sistema
s_date = time.strftime("%A %d, %B %Y", s_date)  # Formatação da data: Monday 01, September 2014


# retorna os dados do associado
golias.get_assoc_from_id(s_email)
s_idassoc, s_iddomain, s_nameuser, s_emailassoc, s_pwdassoc = golias.return_data_assoc()


# pega o nome do usuário e divide em nome e sobrenome
name = str.split(s_nameuser, ' ')
first_name = name[0]
last_name = name[1]


# retorna o nome do domínio
# s_domain = golias.return_domain_name(s_iddomain)

s_field = 1
n_field = []
s_f_msg = None

# valida se o campo dominio foi informado pelo usuário
if s_domain_newuser is None:
    s_field = 0
    n_field.append('D')
    s_f_msg = ' Data field required!'
    s_domain_newuser = s_domain
else:
    s_domain_newuser = str.lower(s_domain_newuser)

# valida se o campo first name foi informado pelo usuário
if s_fname_newuser is None:
    s_field = 0
    n_field.append('F')
    s_f_msg = ' Data field required!'
    s_fname_newuser = 'required'
else:
    s_fname_newuser = str.capitalize(s_fname_newuser)

# valida se o campo last name foi informado pelo usuário
if s_lname_newuser is None:
    s_field = 0
    n_field.append('L')
    s_f_msg = ' Data field required!'
    s_lname_newuser = 'required'
else:
    s_lname_newuser = str.capitalize(s_lname_newuser)

# valida se o campo email foi informado pelo usuário
if s_email_newuser is None:
    s_field = 0
    n_field.append('E')
    s_f_msg = ' Data field required!'
    s_email_newuser = 'required'
else:
    # verifica se o endereço de e-mail informado pelo usuario é válido
    (is_email) = golias.validate_email(s_email_newuser)
    if is_email is False:
        s_field = 0
        n_field.append('E')
        s_f_msg = ' Invalid e-mail. Please, try again!'
        s_email_newuser = 'name@domain.com'

# valida se o campo password foi informado pelo usuário
if s_pwd_newuser is None:
    s_field = 0
    n_field.append('W')
    s_f_msg = ' Data field required!'
    s_pwd_newuser = '12345678'
else:
    (is_pwd) = golias.validate_pwd(s_pwd_newuser)
    if is_pwd is False:
        s_field = 0
        n_field.append('W')
        s_f_msg = ' The password must have more than 8 characters. Please, try again!'
        s_pwd_newuser = '12345678'

# valida se o campo profile foi informado pelo usuário
if s_profile_newuser is None:
    s_field = 0
    n_field.append('P')
    s_f_msg = ' Data field required!'

# valida se o campo task foi informado pelo usuário
if s_task_newuser is None:
    s_field = 0
    n_field.append('T')
    s_f_msg = ' Data field required!'


# se todos os campos foram preenchidos, então realiza a inclusão de um novo usuário no sistema
if s_field != 0:
    s_newuser = str.strip(s_fname_newuser) + ' ' + str.strip(s_lname_newuser)

    if s_profile_newuser == 'S':
        exist_sup = golias.get_assoc_supervisor(s_domain_newuser)
        if exist_sup is True:
            user_added = False
            s_erromsg = ' The \'Supervisor User\' was found. Please, try again or contact your System Administrator!'
        else:
            (user_added, s_erromsg) = golias.add_newuser(s_domain_newuser, s_newuser, s_email_newuser, s_pwd_newuser,
                                                         s_profile_newuser, s_task_newuser)
    else:
        (user_added, s_erromsg) = golias.add_newuser(s_domain_newuser, s_newuser, s_email_newuser, s_pwd_newuser,
                                                     s_profile_newuser, s_task_newuser)

    # se o usuário foi adicionado ao sistema, então renderiza a tela para cadastrar um novo usuário
    if user_added is True:
        # renderiza a página 'cusers.html' para continuar com o cadastramento de um novo usuário no sistema
        print mysf.include_start_response()
        print (mysf.include_header())
        print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
        print (mysf.include_logout())
        print (mysf.include_div_s())
        print (mysf.include_messages('2', ' New user created!'))
        print (mysf.include_pageheader('Users ', ' Create new user'))
        print (mysf.include_form_cu(s_domain, s_nameuser, str.lower(s_emailassoc)))
        print (mysf.include_div_e())
        print (mysf.include_footer())
    else:
        # renderiza a página 'cusers.html' com a mensagem do erro para verificação e tratamento
        print mysf.include_start_response()
        print (mysf.include_header())
        print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
        print (mysf.include_logout())
        print (mysf.include_div_s())
        print (mysf.include_messages('1', s_erromsg))
        print (mysf.include_pageheader('Users ', ' Create new user'))
        print (mysf.include_form_cu(s_domain, s_nameuser, str.lower(s_emailassoc)))
        print (mysf.include_div_e())
        print (mysf.include_footer())
else:
    # renderiza a página 'cusers.html' com a mensagem do erro para verificação e tratamento
    print mysf.include_start_response()
    print (mysf.include_header())
    print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
    print (mysf.include_logout())
    print (mysf.include_div_s())
    print (mysf.include_messages('3', s_f_msg))
    print (mysf.include_pageheader('Users ', ' Create new user'))
    print (mysf.include_form_cu_err(s_domain_newuser, s_fname_newuser, s_lname_newuser, s_email_newuser,
                                    s_pwd_newuser, s_profile_newuser, s_task_newuser, s_domain, s_nameuser,
                                    str.lower(s_emailassoc), n_field))
    print (mysf.include_div_e())
    print (mysf.include_footer())