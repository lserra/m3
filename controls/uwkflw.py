#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

"""
Created on 03/03/2015
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
# TODO: revisar e ajustar este trecho do código
s_domain_eduser = form_data.getvalue('domain_eu')  # pega o valor do campo domain
s_fname_eduser = form_data.getvalue('fname')  # pega o valor do campo fname
s_lname_eduser = form_data.getvalue('lname')  # pega o valor do campo lname
s_email_eduser = form_data.getvalue('email')  # pega o valor do campo email
s_profile_eduser = form_data.getvalue('profile')  # pega o valor do campo profile
s_task_eduser = form_data.getvalue('task')  # pega o valor do campo task

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
# TODO: revisar e ajustar este trecho do código
# valida se o campo dominio foi informado pelo usuário
if s_domain_eduser is None:
    s_field = 0
    n_field.append('D')
    s_f_msg = ' Data field required!'
    s_domain_eduser = s_domain
else:
    s_domain_eduser = str.lower(s_domain_eduser)

# valida se o campo first name foi informado pelo usuário
if s_fname_eduser is None:
    s_field = 0
    n_field.append('F')
    s_f_msg = ' Data field required!'
    s_fname_eduser = 'required'
else:
    s_fname_eduser = str.capitalize(s_fname_eduser)

# valida se o campo last name foi informado pelo usuário
if s_lname_eduser is None:
    s_field = 0
    n_field.append('L')
    s_f_msg = ' Data field required!'
    s_lname_eduser = 'required'
else:
    s_lname_eduser = str.capitalize(s_lname_eduser)

# valida se o campo email foi informado pelo usuário
if s_email_eduser is None:
    s_field = 0
    n_field.append('E')
    s_f_msg = ' Data field required!'
    s_email_eduser = 'required'
else:
    # verifica se o endereço de e-mail informado pelo usuario é válido
    (is_email) = golias.validate_email(s_email_eduser)
    if is_email is False:
        s_field = 0
        n_field.append('E')
        s_f_msg = ' Invalid e-mail. Please, try again!'
        s_email_eduser = 'name@domain.com'

# valida se o campo profile foi informado pelo usuário
if s_profile_eduser is None:
    s_field = 0
    n_field.append('P')
    s_f_msg = ' Data field required!'

# valida se o campo task foi informado pelo usuário
if s_task_eduser is None:
    s_field = 0
    n_field.append('T')
    s_f_msg = ' Data field required!'

# TODO: revisar e ajustar este trecho do código
# se todos os campos foram preenchidos, então realiza a alteração dos dados do workflow no sistema
if s_field != 0:
    s_name_eduser = str.strip(s_fname_eduser) + ' ' + str.strip(s_lname_eduser)

    # retorna os dados do workflow editado
    golias.get_assoc_from_id(s_email_eduser)
    s_idassoc_user_ed, s_iddomain_user_ed, s_name_user_ed, s_email_user_ed, s_pwd_user_ed = golias.return_data_assoc()

    # atualiza os dados do workflow editado no sistema
    (user_edited, s_erromsg) = golias.update_profile_assoc(s_iddomain_user_ed, s_idassoc_user_ed, s_name_eduser,
                                                           s_email_eduser, s_profile_eduser, s_task_eduser)
    if user_edited is True:
        # renderiza a página 'ewkflw.html' para continuar com a edição do workflow no sistema
        print mysf.include_start_response()
        print (mysf.include_header())
        print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
        print (mysf.include_logout())
        print (mysf.include_div_s())
        print (mysf.include_messages('2', ' Data saved with success!'))
        print (mysf.include_pageheader('Users ', ' Edit user'))
        print (mysf.include_form_eu(s_domain, s_nameuser, str.lower(s_emailassoc), s_domain_eduser, s_fname_eduser,
                                    s_lname_eduser, s_email_eduser, s_profile_eduser, s_task_eduser))
        print (mysf.include_div_e())
        print (mysf.include_footer())
    else:
        # renderiza a página 'ewkflw.html' com a mensagem do erro para verificação e tratamento
        print mysf.include_start_response()
        print (mysf.include_header())
        print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
        print (mysf.include_logout())
        print (mysf.include_div_s())
        print (mysf.include_messages('1', s_erromsg))
        print (mysf.include_pageheader('Users ', ' Edit user'))
        print (mysf.include_form_eu(s_domain, s_nameuser, str.lower(s_emailassoc), s_domain_eduser, s_fname_eduser,
                                    s_lname_eduser, s_email_eduser, s_profile_eduser, s_task_eduser))
        print (mysf.include_div_e())
        print (mysf.include_footer())
else:
    # renderiza a página 'ewkflw.html' com a mensagem do erro para verificação e tratamento
    print mysf.include_start_response()
    print (mysf.include_header())
    print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
    print (mysf.include_logout())
    print (mysf.include_div_s())
    print (mysf.include_messages('3', s_f_msg))
    print (mysf.include_pageheader('Users ', ' Edit user'))
    print (mysf.include_form_eu_err(s_domain_eduser, s_fname_eduser, s_lname_eduser, s_email_eduser,
                                    s_profile_eduser, s_task_eduser, s_domain, s_nameuser,
                                    str.lower(s_emailassoc), n_field))
    print (mysf.include_div_e())
    print (mysf.include_footer())