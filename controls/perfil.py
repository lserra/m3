#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

"""
Created on 05/06/2014
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

s_fname = form_data.getvalue('first_name')  # pega o valor do campo first_name
s_lname = form_data.getvalue('last_name')  # pega o valor do campo last_name
s_domain = form_data.getvalue('domain')  # pega o valor do campo domain
s_email = form_data.getvalue('email')  # pega o valor do campo email
s_pwd1 = form_data.getvalue('password')  # pega o valor do campo password
s_pwd2 = form_data.getvalue('password_confirmation')  # pega o valor do campo password_confirmation


import time  # funções de manipulação de data e hora do sistema
import mysf  # funções de renderização e output
import golias  # funções de segurança e regras do negócio


s_nameuser = str(s_fname) + ' ' + str(s_lname)

s_date = time.localtime()  # Captura os dados de data/hora do sistema
s_date = time.strftime("%A %d, %B %Y", s_date)  # Formatação da data: Monday 01, September 2014


# valida a nova senha  # TODO: criar a função de atualização da nova senha no banco de dados
(is_valid, s_errmsg) = golias.validate_newpwd(s_pwd1, s_pwd2)


if is_valid:
    s_type = '2'
    s_msg = ' Password changed successfully!'
else:
    s_type = '1'
    s_msg = s_errmsg


# renderiza a página principal 'mthree.html'
print mysf.include_start_response()
print (mysf.include_header())
print (mysf.include_user(s_domain, s_nameuser, s_email, s_date))
print (mysf.include_logout())
print (mysf.include_div_s())

if is_valid:
    print (mysf.include_messages(s_type, s_msg))
else:
    print (mysf.include_messages(s_type, s_msg))
    print (mysf.include_pageheader('Profile ', ' Update login/password'))
    print (mysf.include_profile(s_fname, s_lname, s_domain, s_email))

print (mysf.include_div_e())
print (mysf.include_footer())