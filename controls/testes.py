#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

"""
Created on 18/01/2015
@author: Laércio Serra (laercio.serra@gmail.com)
"""
# Este módulo faz parte da biblioteca padrão do Python e faz um ratreamento CGI
# que, quando ativado, organiza as mensagens de erros detalhadas que aparecem
# no navegador
import cgitb  # chama o módulo de rastreamento de erros do CGI


cgitb.enable()  # ativa o módulo para que os erros possam aparecer no browser


import mysf  # funções de renderização e output


# renderiza a página 'usystem.html' depois de ter os dados do sistema atualizados
print mysf.include_start_response()
print (mysf.include_header())
print (mysf.include_logout())
print (mysf.include_div_s())
print (mysf.include_pageheader('Expenses ', ' Update settings system'))
print (mysf.include_div_e())
print (mysf.include_footer())

