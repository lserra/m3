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

s_domain = form_data.getvalue('d')  # pega o valor do campo domain
s_user = form_data.getvalue('u')  # pega o valor do campo user
s_email = form_data.getvalue('e')  # pega o valor do campo email
s_wedit = form_data.getvalue('we')  # pega o valor do campo email do user a ser editado


import time  # funções de manipulação de data e hora do sistema
import mysf  # funções de renderização e output
import golias  # funções de segurança e regras do negócio


s_date = time.localtime()  # Captura os dados de data/hora do sistema
s_date = time.strftime("%A %d, %B %Y", s_date)  # Formatação da data: Monday 01, September 2014


# retorna os dados do associado
golias.get_assoc_from_id(s_email)
s_idassoc, s_iddomain, s_nameuser, s_emailassoc, s_pwdassoc = golias.return_data_assoc()


# retorna o nome do domínio
# s_domain = golias.return_domain_name(s_iddomain)


# retorna os dados do workflow a ser editado
(i_publisher, s_publisher, i_approver, s_approver, i_payer, s_payer) = golias.edit_wkflw(s_domain, s_wedit)
# retorna todos os users com o perfil 'approver' para popular a combo box da pág ewklw.html
rs_approvers, a_msg_err = golias.get_all_approver_cb(s_domain, i_approver)
# retorna todos os users com o perfil 'payer' para popular a combo box da pág ewklw.html
rs_payers, y_msg_err = golias.get_all_payer_cb(s_domain, i_payer)


# pega o nome do usuário e divide em nome e sobrenome
name = str.split(s_nameuser, ' ')
first_name = name[0]
last_name = name[1]


# renderiza a página 'ewkflw.html' para editar os dados de um workflow do sistema
print mysf.include_start_response()
print (mysf.include_header())
print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
print (mysf.include_logout())
print (mysf.include_div_s())
print (mysf.include_pageheader('Workflow ', ' Edit task user'))
print (mysf.include_form_ew(s_wedit, s_domain, s_nameuser, str.lower(s_emailassoc), i_publisher, s_publisher,
                            i_approver, s_approver, i_payer, s_payer, rs_approvers, rs_payers))
print (mysf.include_div_e())
print (mysf.include_footer())