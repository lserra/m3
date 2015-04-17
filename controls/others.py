# def include_h_regras():
# """
# # função que cria o cabeçalho da página de regras do cycleclub
#     # esta função usa a sua única string como seu argumento para criar o cabeçalho da página HTML,
#     # a página em si é armazenada em um arquivo separado em "views/header_r.html"
#     :return:
#     """
#     with open('../views/h_regras.html') as headf:
#         head_text = headf.read()
#
#     header = Template(head_text)
#
#     return header.substitute()


# def include_start_formc(s_url, form_type="POST"):
#     """
#     # função que retorna a marcação html de início do formulário do tipo CRUD,
#     # permitindo depois personalizar/acrescentar os demais componentes do formulário conforme a navegação do usuário
#     # a página em si é armazenada em um arquivo separado em "views/form.html"
#     # e o elemento <$inicio_form> é substituído quando necessário
#     # a função também permite que especifique a URL para enviar os dados do formulário,
#     # bem como o método a utilizar (GET/POST)
#     :param s_url: 'caminho/script.py'
#     :param form_type: 'POST'
#     :return:
#     """
#     s_formc = '<!-- início do form de crud -->\n'
#     s_formc += '<div id="crud">\n'
#     s_formc += '<form class="form-horizontal" action="' + s_url + '" method="' + form_type + '">'
#
#     return s_formc


# def include_formv(lstitens, rsdatatable):
#     """
#     # função que retorna a marcação html de início do formulário do tipo VIEW,
#     # permitindo depois personalizar/acrescentar os demais componentes do formulário conforme a navegação do usuário
#     # a página em si é armazenada em um arquivo separado em "views/form.html"
#     # e o elemento <$inicio_form> é substituído quando necessário
#     # a função também permite que especifique a URL para enviar os dados do formulário,
#     # bem como o método a utilizar (GET/POST)
#     :param lstitens:
#     :param rsdatatable:
#     """
#     include_cols_cong(lstitens)
#     include_data_table(rsdatatable)


# def include_radio_button(lstbutton):
#     """
#     # componente de um formulário => radio button
#     # obs1.: válido somente para as páginas crud
#     :param lstbutton:{[button]}
#     :return:
#     """
#     s_radios = '<!-- grupo de botões de seleção alinhados na vertical -->\n'
#     s_radios += '<div class="control-group" style="margin-left:300px">\n'
#     s_radios += '<label class="control-label">Selecione uma opção</label>\n'
#
#     for button in lstbutton:
#
#         s_radios += '<div class="controls">\n'
#         s_radios += '<label class="radio">\n'
#         s_radios += '<input type="radio" name="optButtons" id="' + str(button) + '" value="' + \
#                     str(button) + '">' + str(button) + '\n'
#         s_radios += '</label>\n'
#         s_radios += '</div>\n'
#
#     s_radios += '</div>'
#
#     return s_radios


# def include_checkbox(lstlstitens):
#     """
#     # componente de um formulário => checkbox
#     # obs1.: válido somente para as páginas crud
#     :param lstlstitens:{[item]}
#     :return:
#     """
#     s_check = '<!-- grupo de caixas de seleção alinhados na horizontal -->\n'
#     s_check += '<div class="control-group" style="margin-left:300px">\n'
#     s_check += '<label class="control-label">Selecione as opções</label>\n'
#
#     for item in lstlstitens:
#         s_check += '<div class="controls">\n'
#         s_check += '<label class="checkbox inline">\n'
#         s_check += '<input type="checkbox" id="' + item + '" value="' + item + '">' + item + '\n'
#         s_check += '</label>\n'
#         s_check += '</div>\n'
#
#     s_check += '</div>'
#
#     return s_check


# def include_options_select_c(lstoptions):
#     """
#     # componente de um formulário => selectbox
#     # obs1.: válido somente para as páginas crud
#     :param lstoptions:{[option]}
#     :return:
#     """
#     s_select = '!-- caixa de seleção editável para escolha de uma opção -->\n'
#     s_select += '<div class="control-group" style="margin-left:300px">\n'
#     s_select += '<label class="control-label">Selecione uma opção</label>\n'
#     s_select += '<div class="controls">\n'
#     s_select += '<select>\n'
#
#     for option in lstoptions:
#         s_select += '<option>' + option + '</option>\n'
#
#     s_select += '</select>\n'
#     s_select += '</div>\n'
#     s_select += '</div>'
#
#     return s_select


# def include_input_text(s_id, s_label, s_tip):
#     """
#     # componente de um formulário => textbox editável
#     # obs1.: válido somente para as páginas crud
#     :param s_id: 'name'
#     :param s_label: 'Nome'
#     :param s_tip: 'Informe o seu nome completo'
#     :return:
#     """
#     s_textbox = '<!-- caixa de entrada editável para texto -->\n'
#     s_textbox += '<div class="control-group" style="margin-left:300px">\n'
#     s_textbox += '<label class="control-label">' + s_label + '</label>\n'
#     s_textbox += '<div class="controls">\n'
#     s_textbox += '<input type="text" id="' + s_id + '" placeholder="' + s_tip + '" class="span5">\n'
#     s_textbox += '</div>\n'
#     s_textbox += '</div>'
#
#     return s_textbox


# def include_textarea(s_label):
#     """
#     # componente de um formulário => textarea editável
#     # obs1.: válido somente para as páginas crud
#     :param s_label: 'Comentários'
#     :return:
#     """
#     s_textarea = '<!-- caixa de entrada editável para texto do tipo memo -->\n'
#     s_textarea += '<div class="control-group" style="margin-left:300px">\n'
#     s_textarea += '<label class="control-label">' + s_label + '</label>\n'
#     s_textarea += '<div class="controls">\n'
#     s_textarea += '<textarea rows="5" class="span5"></textarea>\n'
#     s_textarea += '</div>\n'
#     s_textarea += '</div>'
#
#     return s_textarea


# def include_input_num(s_label):
#     """
#     # componente de um formulário => textbox editável (somente números)
#     # obs1.: válido somente para as páginas crud
#     :param s_label: 'Idade'
#     :return:
#     """
#     s_textnum = '<!-- caixa de entrada editável para valores numéricos -->\n'
#     s_textnum += '<div class="control-group" style="margin-left:300px">\n'
#     s_textnum += '<label class="control-label">' + s_label + '</label>\n'
#     s_textnum += '<div class="controls">\n'
#     s_textnum += '<div class="input-append">\n'
#     s_textnum += '<input class="span2" id="appendedInput" type="text">\n'
#     s_textnum += '<span class="add-on">.00</span>\n'
#     s_textnum += '</div>\n'
#     s_textnum += '</div>\n'
#     s_textnum += '</div>'
#
#     return s_textnum


# def include_input_moeda(s_label):
#     """
#     # componente de um formulário => textbox editável (somente moeda)
#     # obs1.: válido somente para as páginas crud
#     :param s_label: 'Receita'
#     :return:
#     """
#     s_textmoeda = '<!-- caixa de entrada editável para valores monetários -->\n'
#     s_textmoeda += '<div class="control-group" style="margin-left:300px">\n'
#     s_textmoeda += '<label class="control-label">' + s_label + '</label>\n'
#     s_textmoeda += '<div class="controls">\n'
#     s_textmoeda += '<div class="input-prepend input-append">\n'
#     s_textmoeda += '<span class="add-on">$</span>\n'
#     s_textmoeda += '<input class="span2" id="appendedPrependedInput" type="text">\n'
#     s_textmoeda += '<span class="add-on">,00</span>\n'
#     s_textmoeda += '</div>\n'
#     s_textmoeda += '</div>\n'
#     s_textmoeda += '</div>'
#
#     return s_textmoeda


# def include_input_text_noedit(s_label, s_value):
#     """
#     # componente de um formulário => textbox não editável sem ícone
#     # obs1.: válido somente para as páginas crud
#     :param s_label: 'Importante'
#     :param s_value: 'Texto importante'
#     :return:
#     """
#     s_noedit = '<!-- caixa de entrada não editável sem ícone -->\n'
#     s_noedit += '<div class="control-group" style="margin-left:300px">\n'
#     s_noedit += '<label class="control-label">' + s_label + '</label>\n'
#     s_noedit += '<div class="controls">\n'
#     s_noedit += '<span class="input-xlarge uneditable-input">' + s_value + '</span>\n'
#     s_noedit += '</div>\n'
#     s_noedit += '</div>'
#
#     return s_noedit


# def include_input_text_help(s_label, s_help):
#     """
#     # componente de um formulário => textbox sem ícone com texto de ajuda
#     # obs1.: válido somente para as páginas crud
#     :param s_label: 'Login'
#     :param s_help: 'Informe o seu e-mail para efetuar o login'
#     :return:
#     """
#     s_edithelp = '<!-- caixa de entrada editável sem ícone com texto de ajuda -->\n'
#     s_edithelp += '<div class="control-group" style="margin-left:300px">\n'
#     s_edithelp += '<label class="control-label">' + s_label + '</label>\n'
#     s_edithelp += '<div class="controls">\n'
#     s_edithelp += '<input type="text"><span class="help-block">' + s_help + '</span>\n'
#     s_edithelp += '</div>\n'
#     s_edithelp += '</div>'
#
#     return s_edithelp


# def include_input_text_icon(s_label):
#     """
#     # componente de um formulário => textbox editável com ícone
#     # obs1.: válido somente para as páginas crud
#     :param s_label: 'Login'
#     :return:
#     """
#     s_texticon = '<!-- caixa de entrada editável com ícone -->\n'
#     s_texticon += '<div class="control-group" style="margin-left:300px">\n'
#     s_texticon += '<label class="control-label">' + s_label + '</label>\n'
#     s_texticon += '<div class="controls">\n'
#     s_texticon += '<div class="input-prepend">\n'
#     s_texticon += '<span class="add-on"><i class="icon-envelope"></i></span>\n'
#     s_texticon += '<input class="span2" id="inputIcon" type="text">\n'
#     s_texticon += '</div>\n'
#     s_texticon += '</div>\n'
#     s_texticon += '</div>'
#
#     return s_texticon


# def include_options_select_s(lstlstitens):
#     """
#     # transforma a lista em opções de um controle 'select'
#     # a página em si é armazenada em um arquivo separado em "views/forms.html" e o
#     # elemento <$options> é substituído quando necessário
#     # obs1.: válido somente para as páginas view
#     :param lstlstitens:{[item]}
#     :return:
#     """
#     s_opt = ''
#
#     for I in lstlstitens:
#         s_opt += '<option>' + str.upper(I) + '<option>\n'
#
#     with open('../views/forms.html') as formsf:
#         forms_text = formsf.read
#
#     forms = Template(forms_text)
#
#     return forms.substitute(options=s_opt)


# def include_ds_typeahead(lstlstitens):
#     """
#     # transforma a lista em valores para um array que será o data source de uma função javascript (typeahead)
#     :param lstlstitens:{[item]}
#     :return:
#     """
#     s_values = ''
#
#     for I in lstlstitens:
#         s_values += '"' + I + '",'
#
#     with open('../views/forms.html') as formsf:
#         forms_text = formsf.read
#
#     forms = Template(forms_text)
#
#     return forms.substitute(ds_values=s_values)


# def include_cols_cong(lstitens):
#     """
#     # desenha uma tabela em que o cabeçalho fica congelado
#     # a página em si é armazenada em um arquivo separado em "views/formv.html" e os
#     # elementos <$col1>, <$col2>, <$col3> são substituídos quando necessário
#     # obs1.: válido somente para as páginas view
#     :param lstitens:{[item]}
#     :return:
#     """
#     s_col1 = lstitens[0]
#     s_col2 = lstitens[1]
#     s_col3 = lstitens[2]
#
#     with open('../views/formv.html') as formvf:
#         formv_text = formvf.read
#
#     formv = Template(formv_text)
#
#     return formv.substitute(col1=s_col1, col2=s_col2, col3=s_col3)


# import urllib2


# def include_redir_page(s_url):
#     """
#     # função que faz um redirecionamento de página a partir de um parâmetro
#     # o parâmetro é a url da página a ser redirecionada
#     :param s_url: 'http://localhost/cycleclub/views/regras.html'
#     """
#     req = urllib2.Request(s_url)
#
#     try:
#         print urllib2.urlopen(req).read()
#
#     except urllib2.HTTPError, e:
#         print "ERRO " + str(e.code) + ": " + e.read()


# def include_menu():
#     """
#     # função que cria a barra de menu/navegação
#     # esta função usa a sua única string como seu argumento para criar o rodapé da página HTML,
#     # a página em si é armazenada em um arquivo separado em "views/menu.html"
#     :return:
#     """
#     with open('../views/menu.html') as menuf:
#         menu_text = menuf.read()
#
#     menu = Template(menu_text)
#
#     return menu.substitute()


# def include_b_regras(s_email):
#     """
#     # função que renderiza as regras do cycleclub com o email do associado que está acessando o sistema
#     # a página em si é armazenada em um arquivo separado em "views/b_regras.html"
#     # e o elemento <$emailassoc> é substituído quando necessário
#     :param s_email: "laercio.serra@gmail.com"
#     :return: "laercio.serra@gmail.com"
#     """
#     with open('../views/b_regras.html') as bodyf:
#         body_text = bodyf.read()
#
#     body = Template(body_text)
#
#     return body.substitute(emailassoc=s_email)