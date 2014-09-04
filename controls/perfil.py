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
s_email = form_data.getvalue('emailassoc')  # pega o valor do campo email
s_resp = form_data.getvalue('resp')  # pega o valor do campo senha


import golias  # funções de segurança e regras do negócio
import mysf  # funções de renderização e output


if s_resp == 'Concordo':  # verifica se o associado concordou com as regras do cycleclub e depois registra isto no bd
    golias.get_assoc_from_id(s_email)  # verifica se o usuário já é um associado
    s_idassoc, s_emailassoc, s_pwdassoc = golias.return_data_assoc()  # retorna os dados do associado
    golias.update_status_assoc(s_idassoc)   # atualiza no bd a flag que determina se o associado concorda
                                                    # com as regras do cycleclub


# renderiza a página 'perfil.html' para completar os seus dados cadastrais
print mysf.include_start_response()
print mysf.include_header()
print mysf.include_user(str.lower(s_email))
print mysf.include_messages('2', ' Seja bem-vindo ao CYCLECLUB!')
print mysf.include_footer()