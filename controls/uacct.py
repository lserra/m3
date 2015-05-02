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

form_data = cgi.FieldStorage()  # obter os dados de login do account


s_acct = form_data.getvalue('account')  # pega o valor do campo account
i_acct = form_data.getvalue('id_acct')  # pega o valor do campo id_acct
s_domain = form_data.getvalue('domain')  # pega o valor do campo domain
s_user = form_data.getvalue('nameuser')  # pega o valor do campo nameuser
s_email = form_data.getvalue('emailassoc')  # pega o valor do campo emailassoc


import time  # funções de manipulação de data e hora do sistema
import mysf  # funções de renderização e output
import golias  # funções de segurança e regras do negócio


s_date = time.localtime()  # Captura os dados de data/hora do sistema
s_date = time.strftime("%A %d, %B %Y", s_date)  # Formatação da data: Monday 01, September 2014


# retorna os dados do account
golias.get_assoc_from_id(s_email)
s_idassoc, s_iddomain, s_nameuser, s_emailassoc, s_pwdassoc = golias.return_data_assoc()


# pega o nome do account e divide em nome e sobrenome
name = str.split(s_nameuser, ' ')
first_name = name[0]
last_name = name[1]


# retorna o nome do domínio
# s_domain = golias.return_domain_name(s_iddomain)


s_field = 1
n_field = []
s_f_msg = None
# valida se o campo account foi informado pelo account
if s_acct is None:
    s_field = 0
    n_field.append('A')
    s_f_msg = ' Data field required!'


# se todos os campos foram preenchidos, então realiza a alteração dos dados do account no sistema
if s_field != 0:
    # atualiza os dados do account editado no sistema
    (acct_edited, s_erromsg_u) = golias.update_acct(i_acct, str.title(s_acct))
    if acct_edited is True:
        (s_acct_new, s_erromsg_g) = golias.get_acct_from_id(i_acct)
        # renderiza a página 'uacct.html' para continuar com a edição do account no sistema
        print mysf.include_start_response()
        print (mysf.include_header())
        print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
        print (mysf.include_logout())
        print (mysf.include_div_s())
        print (mysf.include_messages('2', ' Data saved with success!'))
        print (mysf.include_pageheader('Accounts ', ' Edit account'))
        print (mysf.include_form_ea(s_acct_new, i_acct, s_domain, s_nameuser, str.lower(s_emailassoc)))
        print (mysf.include_div_e())
        print (mysf.include_footer())
    else:
        # renderiza a página 'uacct.html' com a mensagem do erro para verificação e tratamento
        print mysf.include_start_response()
        print (mysf.include_header())
        print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
        print (mysf.include_logout())
        print (mysf.include_div_s())
        print (mysf.include_messages('1', s_erromsg_u))
        print (mysf.include_pageheader('Accounts ', ' Edit account'))
        print (mysf.include_form_ea(s_acct, i_acct, s_domain, s_nameuser, str.lower(s_emailassoc)))
        print (mysf.include_div_e())
        print (mysf.include_footer())
else:
    # renderiza a página 'uacct.html' com a mensagem do erro para verificação e tratamento
    print mysf.include_start_response()
    print (mysf.include_header())
    print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
    print (mysf.include_logout())
    print (mysf.include_div_s())
    print (mysf.include_messages('3', s_f_msg))
    print (mysf.include_pageheader('account ', ' Edit task user'))
    print (mysf.include_form_ea_err(s_acct, i_acct, s_domain, s_nameuser, str.lower(s_emailassoc), n_field))
    print (mysf.include_div_e())
    print (mysf.include_footer())