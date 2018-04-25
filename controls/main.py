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

s_domain = form_data.getvalue('d')  # pega o valor do campo domain
s_user = form_data.getvalue('u')  # pega o valor do campo nameuser
s_email = form_data.getvalue('e')  # pega o valor do campo emailassoc


import time  # funções de manipulação de data e hora do sistema
import mysf  # funções de renderização e output
import golias  # funções de segurança e regras do negócio


s_date = time.localtime()  # Captura os dados de data/hora do sistema
s_date = time.strftime("%A %d, %B %Y", s_date)  # Formatação da data: Monday 01, September 2014


def render_mthree_html(domain, nameuser, emailassoc, date, fields, dt_tb):
    """
    # Renderiza a página principal 'mthree.html'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@gmail.com'
    :param date: '12/01/2015'
    :param fields: {'a', 'b', 'c'}
    :param dt_tb: {(value1, value2, value3), (value4, value5, value6), (value7, value8, value9)}
    """
    print (mysf.include_start_response())
    print (mysf.include_header())
    print (mysf.include_user(domain, nameuser, emailassoc, date))
    print (mysf.include_logout())
    print (mysf.include_div_s())
    print (mysf.include_pageheader('Expenses ', ' Last payments'))
    print (mysf.include_search_form())
    if dt_tb is None:
        print (mysf.include_data_table(fields))
    else:
        print (mysf.include_data_table_enable(domain, fields, dt_tb))
    print (mysf.include_pagination())
    print (mysf.include_div_e())
    print (mysf.include_footer())


# retorna os dados do associado
golias.get_assoc_from_id(s_email)
s_idassoc, s_iddomain, s_nameuser, s_emailassoc, s_pwdassoc = golias.return_data_assoc()
# retorna a lista dos últimos expenses report pagos
s_fields, s_dt_tb, s_errormsg_le = golias.list_expenses_payments_accepted(s_idassoc)
# renderiza a páginal principal "main.html"
render_mthree_html(s_domain, s_nameuser, str.lower(s_emailassoc), s_date, s_fields, s_dt_tb)