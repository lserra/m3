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
n_field = None
s_f_msg = None

# valida se o campo dominio foi informado pelo usuário
if s_domain_newuser is None:
    s_field = 0
    n_field = 'D'
    s_f_msg = 'Data field required!'
# valida se o campo first name foi informado pelo usuário
if s_fname_newuser is None:
    s_field = 0
    n_field = 'F'
    s_f_msg = 'Data field required!'
# valida se o campo last name foi informado pelo usuário
if s_lname_newuser is None:
    s_field = 0
    n_field = 'L'
    s_f_msg = 'Data field required!'
# valida se o campo email foi informado pelo usuário
if s_email_newuser is None:
    s_field = 0
    n_field = 'E'
    s_f_msg = 'Data field required!'
# valida se o campo password foi informado pelo usuário
if s_pwd_newuser is None:
    s_field = 0
    n_field = 'W'
    s_f_msg = 'Data field required!'
# valida se o campo profile foi informado pelo usuário
if s_profile_newuser is None:
    s_field = 0
    n_field = 'P'
    s_f_msg = 'Data field required!'


# se todos os campos foram preenchidos, então realiza a inclusão de um novo usuário no sistema
if s_field != 0:
    s_newuser = str.strip(s_fname_newuser) + ' ' + str.strip(s_lname_newuser)

    (user_added, s_erromsg) = golias.add_newuser(s_domain_newuser, s_newuser, s_email_newuser, s_pwd_newuser,
                                                 s_profile_newuser)

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
                                    s_pwd_newuser, s_profile_newuser, s_domain, s_nameuser, str.lower(s_emailassoc),
                                    s_field))
    print (mysf.include_div_e())
    print (mysf.include_footer())