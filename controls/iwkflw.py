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


s_publisher = form_data.getvalue('publisher')  # pega o valor do campo publisher
s_approver = form_data.getvalue('approver')  # pega o valor do campo approver
s_payer = form_data.getvalue('payer')  # pega o valor do campo payer
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

# valida se o campo publisher foi informado pelo usuário
if s_publisher is None:
    s_field = 0
    n_field.append('P')
    s_f_msg = ' Data field required!'


# valida se o campo approver foi informado pelo usuário
if s_approver is None:
    s_field = 0
    n_field.append('A')
    s_f_msg = ' Data field required!'


# valida se o campo payer foi informado pelo usuário
if s_payer is None:
    s_field = 0
    n_field.append('Y')
    s_f_msg = ' Data field required!'


# retorna todos os users com o perfil 'publisher' para popular a combo box da pág cwkflw.html
rs_publishers, p_msg_err = golias.get_all_publisher(s_domain)
# retorna todos os users com o perfil 'approver' para popular a combo box da pág cwkflw.html
rs_approvers, a_msg_err = golias.get_all_approver(s_domain)
# retorna todos os users com o perfil 'payer' para popular a combo box da pág cwkflw.html
rs_payers, y_msg_err = golias.get_all_payer(s_domain)


# se todos os campos foram preenchidos, então realiza a inclusão de um novo workflow no sistema
if s_field != 0:
    (wkflw_added, s_erromsg) = golias.add_newwkflw(s_domain, s_publisher, s_approver, s_payer)
    # se o workflow foi adicionado ao sistema, então renderiza a tela para cadastrar um novo workflow
    if wkflw_added is True:
        # renderiza a página 'cwkflw.html' para continuar com o cadastramento de um novo workflow no sistema
        print mysf.include_start_response()
        print (mysf.include_header())
        print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
        print (mysf.include_logout())
        print (mysf.include_div_s())
        print (mysf.include_pageheader('Workflow ', ' Create new workflow'))
        print (mysf.include_form_cw(s_domain, s_nameuser, str.lower(s_emailassoc),
                                    rs_publishers, rs_approvers, rs_payers))
        print (mysf.include_div_e())
        print (mysf.include_footer())
    else:
        # renderiza a página 'cwkflw.html' com a mensagem do erro para verificação e tratamento
        print mysf.include_start_response()
        print (mysf.include_header())
        print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
        print (mysf.include_logout())
        print (mysf.include_div_s())
        print (mysf.include_messages('1', s_erromsg))
        print (mysf.include_pageheader('Workflow ', ' Create new workflow'))
        print (mysf.include_form_cw(s_domain, s_nameuser, str.lower(s_emailassoc),
                                    rs_publishers, rs_approvers, rs_payers))
        print (mysf.include_div_e())
        print (mysf.include_footer())
else:
    # renderiza a página 'cwkflw.html' com a mensagem do erro para verificação e tratamento
    print mysf.include_start_response()
    print (mysf.include_header())
    print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
    print (mysf.include_logout())
    print (mysf.include_div_s())
    print (mysf.include_messages('3', s_f_msg))
    print (mysf.include_pageheader('Workflow ', ' Create new workflow'))
    print (mysf.include_form_cw_err(s_domain, s_nameuser, str.lower(s_emailassoc),
                                    rs_publishers, rs_approvers, rs_payers, n_field))
    print (mysf.include_div_e())
    print (mysf.include_footer())