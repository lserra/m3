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
s_email = form_data.getvalue('email')  # pega o valor do campo email
s_senha = form_data.getvalue('pwd')  # pega o valor do campo senha

import mysf  # funções de renderização e output
import golias  # funções de segurança e regras do negócio


print (mysf.include_start_response())
print (mysf.include_header())

(is_email) = golias.validate_email(s_email)  # verifica se o endereço de e-mail informado pelo usuario é válido
if is_email:
    (is_assoc, s_errormsg) = golias.get_assoc_from_id(s_email)  # verifica se o usuário já é um associado
    if is_assoc:
        (is_authenticated) = golias.auth_assoc(s_email, s_senha)  # autentica o associado para acessar o sistema
        if is_authenticated:
            s_idassoc, s_emailassoc, s_pwdassoc = golias.return_data_assoc()
            print (mysf.include_user(str.lower(s_emailassoc)))
            print (mysf.include_messages('2', ' Seja bem-vindo ao CYCLECLUB!'))
        else:
            print (mysf.include_menu())
            print (mysf.include_messages('1', ' E-mail ou senha inválida! A senha deve ter no mínimo 8 caracteres.\
            Por favor, tente novamente.'))
    else:
        print (mysf.include_menu())
        if s_errormsg != '' and s_errormsg is not None:
            print (mysf.include_messages('1', s_errormsg))
        else:
            print (mysf.include_messages('4', ' Você ainda não é um associado do CYCLECLUB. Faça já o seu cadastro!'))
else:
    print (mysf.include_menu())
    print (mysf.include_messages('3', ' E-mail inválido! Por favor, tente novamente.'))

print (mysf.include_footer())