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

s_domain = form_data.getvalue('d')  # pega o valor do campo domain
s_user = form_data.getvalue('u')  # pega o valor do campo user
s_email = form_data.getvalue('e')  # pega o valor do campo email
s_wdel = form_data.getvalue('wd')  # pega o valor do campo id_workflow a ser apagado


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


# exclui o workflow do sistema
(wkflw_deleted, s_errormsg_d) = golias.delete_wkflw(s_domain, s_wdel)


# retorna os dados da matriz de task/users
(s_fields, s_dt_tb, s_errormsg_m) = golias.get_all_matrix(s_domain)


# renderiza a página 'wkflw.html' para visualizar os usuários do sistema
print mysf.include_start_response()
print (mysf.include_header())
print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
print (mysf.include_logout())
print (mysf.include_div_s())
if wkflw_deleted is True:
    print (mysf.include_messages('2', ' Workflow deleted with success!'))
else:
    if s_errormsg_d is not None:
        print (mysf.include_messages('1', s_errormsg_d))
    elif s_errormsg_m is not None:
        print (mysf.include_messages('1', s_errormsg_m))
    # else:
    #     s_errormsg = s_errormsg_d + '\n' + s_errormsg_m
    #     print (mysf.include_messages('1', s_errormsg))
print (mysf.include_pageheader('Workflow ', ' List all matrix task user'))
print (mysf.include_button_create_new_wkflw(s_domain, s_nameuser, str.lower(s_emailassoc)))
if s_dt_tb is None:
    print (mysf.include_data_table(s_fields))
else:
    print (mysf.include_dt_tb_enable_matrix(s_domain, s_nameuser, str.lower(s_emailassoc), s_fields, s_dt_tb))
print (mysf.include_pagination())
print (mysf.include_delete_matrix())
print (mysf.include_div_e())
print (mysf.include_footer())