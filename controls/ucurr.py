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


s_curr = form_data.getvalue('code')  # pega o valor do campo code
s_desc = form_data.getvalue('description')  # pega o valor do campo description
s_sign = form_data.getvalue('sign')  # pega o valor do campo sign
i_curr = form_data.getvalue('id_currency')  # pega o valor do campo id_currency
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


# pega o nome do associado e divide em nome e sobrenome
name = str.split(s_nameuser, ' ')
first_name = name[0]
last_name = name[1]


# retorna o nome do domínio
# s_domain = golias.return_domain_name(s_iddomain)


s_field = 1
n_field = []
s_f_msg = None
# valida se o campo currency foi informado pelo associado
if s_curr is None:
    s_field = 0
    n_field.append('C')
    s_f_msg = ' Data field required!'

# valida se o campo description foi informado pelo associado
if s_desc is None:
    s_field = 0
    n_field.append('D')
    s_f_msg = ' Data field required!'

# valida se o campo sign foi informado pelo associado
if s_sign is None:
    s_field = 0
    n_field.append('S')
    s_f_msg = ' Data field required!'


# se todos os campos foram preenchidos, então realiza a alteração dos dados do currency no sistema
if s_field != 0:
    # atualiza os dados do currency editado no sistema
    (curr_edited, s_erromsg_u) = golias.update_curr(str.upper(s_curr), str.title(s_desc), str.upper(s_sign),
                                                    i_curr, s_domain)
    if curr_edited is True:
        (s_curr_new, s_desc_new, s_sign_new, s_erromsg_g) = golias.get_curr_from_id(i_curr)
        # renderiza a página 'ucurr.html' para continuar com a edição do currency no sistema
        print mysf.include_start_response()
        print (mysf.include_header())
        print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
        print (mysf.include_logout())
        print (mysf.include_div_s())
        print (mysf.include_messages('2', ' Data saved with success!'))
        print (mysf.include_pageheader('Currency ', ' Edit currency'))
        print (mysf.include_form_ecurr(s_curr_new, s_desc_new, s_sign_new, i_curr, s_domain,
                                       s_nameuser, str.lower(s_emailassoc)))
        print (mysf.include_div_e())
        print (mysf.include_footer())
    else:
        # renderiza a página 'ucurr.html' com a mensagem do erro para verificação e tratamento
        print mysf.include_start_response()
        print (mysf.include_header())
        print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
        print (mysf.include_logout())
        print (mysf.include_div_s())
        print (mysf.include_messages('1', s_erromsg_u))
        print (mysf.include_pageheader('Currency ', ' Edit currency'))
        print (mysf.include_form_ecurr(s_curr, s_desc, s_sign, i_curr, s_domain,
                                       s_nameuser, str.lower(s_emailassoc)))
        print (mysf.include_div_e())
        print (mysf.include_footer())
else:
    # renderiza a página 'ucurr.html' com a mensagem do erro para verificação e tratamento
    print mysf.include_start_response()
    print (mysf.include_header())
    print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
    print (mysf.include_logout())
    print (mysf.include_div_s())
    print (mysf.include_messages('3', s_f_msg))
    print (mysf.include_pageheader('currency ', ' Edit currency'))
    print (mysf.include_form_ecurr_err(s_curr, s_desc, s_sign, i_curr, s_domain,
                                       s_nameuser, str.lower(s_emailassoc), n_field))
    print (mysf.include_div_e())
    print (mysf.include_footer())