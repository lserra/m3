#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

"""
Created on 14/06/2014
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
s_nome = form_data.getvalue('nome')  # pega o valor do campo nome
s_email = form_data.getvalue('email')  # pega o valor do campo email
s_motivo = form_data.getvalue('motivo')  # pega o valor do campo motivo
s_descmotivo = form_data.getvalue('descmotivo')  # pega o valor do campo pwd2

import mysf  # funções de renderização e output
import golias  # funções de segurança e regras do negócio


print mysf.include_start_response()
print mysf.include_header_reg()
print mysf.include_menu_s()


# verifica se todos os campos foram preenchidos
if s_nome is None:
    print mysf.include_messages('3', ' É obrigatório o preenchimento de todos os campos! Por favor, tente novamente.')
    print mysf.include_form_ct()
elif s_email is None:
    print mysf.include_messages('3', ' É obrigatório o preenchimento de todos os campos! Por favor, tente novamente.')
    print mysf.include_form_ct()
elif s_motivo is None:
    print mysf.include_messages('3', ' É obrigatório o preenchimento de todos os campos! Por favor, tente novamente.')
    print mysf.include_form_ct()
elif s_descmotivo is None:
    print mysf.include_messages('3', ' É obrigatório o preenchimento de todos os campos! Por favor, tente novamente.')
    print mysf.include_form_ct()
else:
    (is_email) = golias.validate_email(s_email)  # verifica se o endereço de e-mail informado pelo usuario é válido
    if is_email:
        # verifica se o e-mail foi enviado com sucesso
        (ok_sendemail, s_errormsg) = golias.send_message(s_nome, s_email, s_motivo, s_descmotivo)
        if ok_sendemail:
            print mysf.include_messages('2', ' Sua mensagem foi enviada! Agradecemos o seu contato. Entraremos em \
            contato com você, assim que possível.')
        else:
            print mysf.include_messages('1', s_errormsg)
    else:
        print mysf.include_messages('3', ' E-mail inválido! Por favor, tente novamente.')
        print mysf.include_form_ct()

print mysf.include_footer()