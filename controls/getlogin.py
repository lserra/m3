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


import mysf  # funções de renderização e output
import golias  # funções de segurança e regras do negócio


print mysf.include_start_response()
print mysf.include_header_reg()
print mysf.include_menu_s()


(is_email) = golias.validate_email(s_email)  # verifica se o endereço de e-mail informado pelo usuario é válido
if is_email:
    (is_assoc, s_errormsg) = golias.get_assoc_from_id(s_email)  # verifica se o usuário já é um associado
    if is_assoc:
        s_idassoc, s_emailassoc, s_pwdassoc = golias.return_data_assoc()
        s_pwdassoc = golias.assoc_pwd_decrypto(s_pwdassoc)
        # verifica se o e-mail foi enviado para o associado com sucesso
        (ok_sendemail, s_errormsg) = golias.send_login_assoc(s_emailassoc, s_pwdassoc)
        if ok_sendemail:
            print mysf.include_messages('2', ' Dados de login enviados para o seu e-mail!')
        else:
            print mysf.include_messages('1', s_errormsg)
            print mysf.include_form_gl()
    else:
        if s_errormsg != '' and s_errormsg is not None:
            print mysf.include_messages('1', s_errormsg)
            print mysf.include_form_gl()
        else:
            print mysf.include_messages('4', ' Você ainda não é um associado do CYCLECLUB. Faça já o seu cadastro!')
            print mysf.include_form_gl()
else:
    print mysf.include_messages('3', ' E-mail inválido! Por favor, tente novamente.')
    print mysf.include_form_gl()


print mysf.include_footer()