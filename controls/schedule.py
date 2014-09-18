#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

"""
Created on 01/07/2014
@author: Laércio Serra (laercio.serra@gmail.com)
"""

# O módulo CGI pega todos os dados do formulário e coloca-os em um dicionário
# import cgi


# Este módulo faz parte da biblioteca padrão do Python e faz um ratreamento CGI
# que, quando ativado, organiza as mensagens de erros detalhadas que aparecem
# no navegador
# import cgitb  # chama o módulo de rastreamento de erros do CGI


# cgitb.enable()  # ativa o módulo para que os erros possam aparecer no browser
# form_data = cgi.FieldStorage()  # obter os dados de login do associado
# s_email = form_data.getvalue('emailassoc')  # pega o valor do campo email
# s_resp = form_data.getvalue('resp')  # pega o valor do campo senha


import mysf  # funções de renderização e output
import time
import calendar


# renderiza a página 'perfil.html' para completar os seus dados cadastrais
print mysf.include_start_response()
print mysf.include_header()
# print mysf.include_user(str.lower('laercio.serra@gmail.com'))
print mysf.include_messages('2', ' Seja bem-vindo ao CYCLECLUB!')

lista = ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']
ano, mes, hoje = time.localtime(time.time())[:3]

print '<CENTER>'
print '<H1>Calendário de Aventuras do mês %02d/%04d</H1>' % (mes, ano)
print '<TABLE>'
print '<TR>'

for dia_sem in lista:
    if dia_sem in ['sab', 'dom']:
        bgcolor = 'gray'
    else:
        bgcolor = 'white'

    print '<TH WIDTH="45" BGCOLOR="%s">' % bgcolor
    print '<H3>%s</H3></TH>' % dia_sem

print '</TR>'

for semana in calendar.monthcalendar(ano, mes):
    print '<TR>'

    num_dia_sem = 0

    for dia in semana:
        if dia == hoje:
            bgcolor = 'pink'
        elif num_dia_sem >= 5:
            bgcolor = 'lightgreen'
        else:
            bgcolor = 'lightblue'

        print '<TD ALIGN="RIGHT" BGCOLOR="%s">' % bgcolor

        if dia != 0:
            print '<H2>%2d</H2>' % dia

print '</TD>'

num_dia_sem += 1

print '</TR>'
print '</TABLE></CENTER>'

print mysf.include_footer()