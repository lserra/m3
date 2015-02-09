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

# TODO: criar rotina de validação do input dos dados


# TODO: revisar esta rotina de inclusão de um novo usuário e fazer os ajustes se for necessário
s_newuser = str.strip(s_fname_newuser) + ' ' + str.strip(s_lname_newuser)
(user_added, s_erromsg) = golias.add_newuser(s_domain_newuser, s_newuser, s_email_newuser, s_pwd_newuser,
                                             s_profile_newuser, s_task_newuser)

if user_added:
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
    # renderiza a página 'cusers.html' para continuar com o cadastramento de um novo usuário no sistema
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