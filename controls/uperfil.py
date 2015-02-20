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
s_email = form_data.getvalue('u')  # pega o valor do campo email


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
s_domain = golias.return_domain_name(s_iddomain)


# renderiza a página 'profile.html' para atualizar os seus dados cadastrais
print mysf.include_start_response()
print (mysf.include_header())
print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
print (mysf.include_logout())
print (mysf.include_div_s())
print (mysf.include_pageheader('Profile ', ' Update password'))
print (mysf.include_profile(first_name, last_name, s_domain, str.lower(s_emailassoc)))
print (mysf.include_div_e())
print (mysf.include_footer())