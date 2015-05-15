#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

"""
Created on 12/05/2015
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
s_user = form_data.getvalue('u')  # pega o valor do campo nameuser
s_email = form_data.getvalue('e')  # pega o valor do campo emailassoc

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

# pega o perfil do usuário
# s_profile = golias.get_profile_assoc(s_emailassoc)

# lista de expenses report criados no período e que não foram submetidos para aprovação
s_fields, s_dt_tb, s_errormsg_le = golias.list_expenses_created(s_idassoc)


# renderiza a página 'expr.html' para visualizar a lista de expenses criados
print (mysf.include_start_response())
print (mysf.include_header())
print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
print (mysf.include_logout())
print (mysf.include_div_s())
# print (mysf.include_wells())
print (mysf.include_workflow('1'))
print (mysf.include_pageheader('Expenses ', ' List all expenses created'))
print (mysf.include_button_create_new_expr(s_domain, s_nameuser, str.lower(s_emailassoc)))
if s_dt_tb is None:
    print (mysf.include_data_table(s_fields))
else:
    print (mysf.include_dt_tb_enable_expr(s_domain, s_nameuser, str.lower(s_emailassoc), s_fields, s_dt_tb))
print (mysf.include_pagination())
print (mysf.include_delete_expr())
print (mysf.include_div_e())
print (mysf.include_footer())