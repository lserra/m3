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
s_nameuser = form_data.getvalue('u')  # pega o valor do campo user
s_email = form_data.getvalue('e')  # pega o valor do campo email


import time  # funções de manipulação de data e hora do sistema
import mysf  # funções de renderização e output
# import golias  # funções de segurança e regras do negócio


s_date = time.localtime()  # Captura os dados de data/hora do sistema
s_date = time.strftime("%A %d, %B %Y", s_date)  # Formatação da data: Monday 01, September 2014

# TODO: colocar o formulário no padrão do "update profile"
# TODO: criar rotina para gravar os dados do sistema no banco de dados
print mysf.include_start_response()
print (mysf.include_header())
print (mysf.include_user(s_domain, s_nameuser, s_email, s_date))
print (mysf.include_logout())
print (mysf.include_div_s())
# print (mysf.include_messages('2', ' Welcome to My Expenses Report!'))
print (mysf.include_pageheader('Expenses ', ' Update settings system'))
print (mysf.include_form_ss())
print (mysf.include_div_e())
print (mysf.include_footer())
