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


import golias  # funções de segurança e regras do negócio
import mysf  # funções de renderização e output


def output_page_a(code_err, err_msg):
    """
    # Função para deixar o código mais estruturado e limpo
    # esta função renderiza a saída da página "register.html"
    :param code_err:'3'
    :param err_msg:' Você informou um e-mail inválido! Por favor, tente novamente.'
    """
    print (mysf.include_start_response())
    print (mysf.include_header_reg())
    print (mysf.include_menu_s())
    print (mysf.include_messages(code_err, err_msg))
    print (mysf.include_form_reg())
    print (mysf.include_footer())


def output_page_b(code_err, err_msg):
    """
    # Função para deixar o código mais estruturado e limpo
    # esta função renderiza a saída da página "register.html"
    :param code_err:'3'
    :param err_msg:' Você informou um e-mail inválido! Por favor, tente novamente.'
    """
    print (mysf.include_start_response())
    print (mysf.include_header_reg())
    print (mysf.include_menu())
    print (mysf.include_messages(code_err, err_msg))
    print (mysf.include_footer())


def output_page_c(s_email):
    """
    # Função para deixar o código mais estruturado e limpo
    # esta função renderiza a saída da página "regras.html"
    :param s_email: "laercio.serra@gmail.com"
    """
    print (mysf.include_start_response())
    print (mysf.include_h_regras())
    print (mysf.include_menu_s())
    print (mysf.include_b_regras(s_email))
    print (mysf.include_footer())


# verifica se o usuário informou o e-mail e a senha
if (s_email != '' and s_email is not None) and (s_senha is not None and len(s_senha) >= 8):
    (is_email) = golias.validate_email(s_email)  # verifica se o endereço de e-mail informado pelo usuario é válido
    if is_email:
        (is_assoc, s_errormsg) = golias.get_assoc_from_id(s_email)  # verifica se o usuário já é um associado
        if is_assoc:
            if s_errormsg != '' and s_errormsg is not None:
                s_code_err = '1'
                output_page_a(s_code_err, s_errormsg)
            else:
                s_code_err = '4'
                s_err_msg = ' Você já é um associado do CYCLECLUB!'
                output_page_b(s_code_err, s_err_msg)
        else:
            s_senha_crypt = golias.assoc_pwd_crypto(s_senha)  # codifica a senha do associado antes de gravar no bd
            (is_inserted, s_errormsg) = golias.put_assoc_from_id(s_email, s_senha_crypt)
            if is_inserted:
                # renderiza a página de regras do clube
                output_page_c(s_email)
            else:
                s_code_err = '1'
                output_page_a(s_code_err, s_errormsg)
    else:
        s_code_err = '3'
        s_err_msg = ' E-mail inválido! Por favor, tente novamente.'
        output_page_a(s_code_err, s_err_msg)
else:
    s_code_err = '3'
    s_err_msg = ' E-mail ou senha inválida! A senha deve ter no mínimo 8 caracteres. Por favor, tente novamente.'
    output_page_a(s_code_err, s_err_msg)