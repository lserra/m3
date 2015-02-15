#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

"""
Created on 22/05/2014
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

s_domain = form_data.getvalue('domain')  # pega o valor do campo email
s_email = form_data.getvalue('email')  # pega o valor do campo email
s_senha = form_data.getvalue('password')  # pega o valor do campo senha


import time  # funções de manipulação de data e hora do sistema
import mysf  # funções de renderização e output
import golias  # funções de segurança e regras do negócio


s_date = time.localtime()  # Captura os dados de data/hora do sistema
s_date = time.strftime("%A %d, %B %Y", s_date)  # Formatação da data: Monday 01, September 2014


print (mysf.include_start_response())


(is_email) = golias.validate_email(s_email)  # verifica se o endereço de e-mail informado pelo usuario é válido
if is_email:
    (is_assoc, s_errormsg) = golias.get_assoc_from_id(s_email)  # verifica se o usuário já é um associado
    if is_assoc:  # TODO: validar o dominio e verificar se o usuário está associado a este domínio
        (is_authenticated) = golias.auth_assoc(s_email, s_senha)  # autentica o associado para acessar o sistema
        if is_authenticated:  # TODO: criar uma função que verifica o número de tentativas e bloqueia o acesso após +3 tentativas
            s_idassoc, s_iddomain, s_nameuser, s_emailassoc, s_pwdassoc = golias.return_data_assoc()
            (s_fields, s_dt_tb, s_errormsg) = golias.list_expenses_payments_accepted(s_idassoc)
            # TODO: criar rotina de tratamento, caso o retorno seja 'None'
            print (mysf.include_header())
            print (mysf.include_user(s_domain, s_nameuser, str.lower(s_emailassoc), s_date))
            print (mysf.include_logout())
            print (mysf.include_div_s())
            print (mysf.include_messages('2', ' Welcome to My Expenses Report!'))
            print (mysf.include_pageheader('Expenses ', ' Last payments'))
            print (mysf.include_search_form())
            print (mysf.include_data_table_disable(s_fields, s_dt_tb))
            print (mysf.include_pagination())
            print (mysf.include_delete())
            print (mysf.include_div_e())
            print (mysf.include_footer())  # TODO: fixar o rodapé
        else:
            print (mysf.include_login())
            print (mysf.include_messages('1', ' Invalid e-mail or password. The password must have more than 8 '
                                              'characters. Please, try again!'))
            print (mysf.include_form_login())
            print (mysf.include_footer_login())
    else:
        print (mysf.include_login())

        if s_errormsg != '' and s_errormsg is not None:
            print (mysf.include_messages('1', s_errormsg))
        else:
            print (mysf.include_messages('4', ' You are not a user valid. Please, create a register!'))

        print (mysf.include_form_login())
        print (mysf.include_footer_login())
else:
    print (mysf.include_login())
    print (mysf.include_messages('3', ' Invalid e-mail. Please, try again!'))
    print (mysf.include_form_login())
    print (mysf.include_footer_login())