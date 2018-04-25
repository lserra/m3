#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

"""
Created on 18/01/2015
@author: Laércio Serra (laercio.serra@gmail.com)
"""
# O módulo CGI pega todos os dados do formulário e coloca-os em um dicionário
import cgi


# Este módulo faz parte da biblioteca padrão do Python e faz um rastreamento CGI
# que, quando ativado, organiza as mensagens de erros detalhadas que aparecem
# no navegador
import cgitb  # chama o módulo de rastreamento de erros do CGI


cgitb.enable()  # ativa o módulo para que os erros possam aparecer no browser

form_data = cgi.FieldStorage()  # obter os dados de configuração do sistema

s_alrep = form_data.getvalue('alrep')  # pega o valor do campo alert report
s_dtrep = form_data.getvalue('dtrep')  # pega o valor do campo date report
s_f_email = form_data.getvalue('f_email')  # pega o valor do campo from email
s_curr = form_data.getvalue('curr')  # pega o valor do campo currency
s_dsy = form_data.getvalue('dsy')  # pega o valor do campo decimal symbol
s_tsy = form_data.getvalue('tsy')  # pega o valor do campo thousand symbol
s_domain = form_data.getvalue('domain')  # pega o valor do campo domain
s_user = form_data.getvalue('nameuser')  # pega o valor do campo name user
s_email = form_data.getvalue('emailassoc')  # pega o valor do campo email associado

import time  # funções de manipulação de data e hora do sistema
import mysf  # funções de renderização e output
import golias  # funções de segurança e regras do negócio


s_date = time.localtime()  # Captura os dados de data/hora do sistema
s_date = time.strftime("%A %d, %B %Y", s_date)  # Formatação da data: Monday 01, September 2014


# retorna os dados do associado
golias.get_assoc_from_id(s_email)
(s_idassoc, s_iddomain, s_nameuser, s_emailassoc, s_pwdassoc) = golias.return_data_assoc()


# pega o nome do usuário e divide em nome e sobrenome
name = str.split(s_nameuser, ' ')
first_name = name[0]
last_name = name[1]


# retorna o nome do domínio
# s_domain = golias.return_domain_name(s_iddomain)


# valida se a data informada pelo associado está no formato YYYY-MM-DD
if s_dtrep is None:
    s_dtrep = '0000-00-00'
    statusd = 0
    d_errormsg = None
elif golias.validate_date(s_dtrep):
    statusd = 0
    d_errormsg = None
else:
    statusd = 1
    d_errormsg = 'Incorrect data format, should be "YYYY-MM-DD"'


# valida se o dado informado pelo associado está no formato 'TRUE/FALSE'
if s_alrep is None:
    s_alrep = 'FALSE'
    statusa = 0
    a_errormsg = None
elif str.upper(s_alrep) == 'TRUE' or str.upper(s_alrep) == 'FALSE':
    statusa = 0
    a_errormsg = None
else:
    statusa = 1
    a_errormsg = 'Incorrect data value, should be "TRUE or FALSE"'


# valida se o e-mail fornecido pelo associado é válido
if golias.validate_email(s_f_email):
    statuse = 0
    e_errormsg = None
else:
    statuse = 1
    e_errormsg = 'Incorrect data value, should be "user@domain.com"'


if statusd == 0 and statusa == 0 and statuse == 0:
    # rotina para gravar os dados do sistema no banco de dados
    (status, s_errormsg) = golias.update_setsys(s_iddomain, str.upper(s_alrep), s_dtrep, s_f_email, s_curr,
                                                s_dsy, s_tsy)
    # rotina que lê os dados atualizados do sistema no banco de dados e apresenta no form
    (s_iddomain, s_dtrep, s_alrep, s_f_email, s_curr, s_dsy, s_tsy) = golias.get_setsys(s_iddomain)
else:
    status = 'False'


# retorna todas as currency para popular a combo box
(s_fields, s_dt_tb_curr, s_errormsg_gac) = golias.get_all_curr(s_domain)

s_all_curr = []

if s_dt_tb_curr is not None:
    for curr in s_dt_tb_curr:
        s_all_curr.append(curr[0])

    s_all_curr.remove(s_curr)


# renderiza a página 'usystem.html' depois de ter os dados do sistema atualizado
print (mysf.include_start_response())
print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
print (mysf.include_logout())
print (mysf.include_div_s())
print (mysf.include_header())

if status is True:
    print (mysf.include_messages('2', ' Settings system updated'))
else:
    if statusd == 1:
        print (mysf.include_messages('1', d_errormsg))
    elif statusa == 1:
        print (mysf.include_messages('1', a_errormsg))
    elif statuse == 1:
        print (mysf.include_messages('1', e_errormsg))

print (mysf.include_pageheader('Expenses ', ' Update settings system'))

if status is True:
    print (mysf.include_form_ss(s_domain, s_nameuser, s_emailassoc, s_dtrep, s_alrep, s_f_email,
                                s_curr, s_dsy, s_tsy, s_all_curr))
else:
    if statusd == 1:
        print (mysf.include_form_ss_errd(s_domain, s_nameuser, s_emailassoc, s_dtrep, s_alrep, s_f_email,
                                         s_curr, s_dsy, s_tsy, s_all_curr))
    elif statusa == 1:
        print (mysf.include_form_ss_erra(s_domain, s_nameuser, s_emailassoc, s_dtrep, s_alrep, s_f_email,
                                         s_curr, s_dsy, s_tsy, s_all_curr))
    elif statuse == 1:
        print (mysf.include_form_ss_erre(s_domain, s_nameuser, s_emailassoc, s_dtrep, s_alrep, s_f_email,
                                         s_curr, s_dsy, s_tsy, s_all_curr))

print (mysf.include_div_e())
print (mysf.include_footer())