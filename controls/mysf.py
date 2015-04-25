#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

"""
Created on 22/05/2014
@author: Laércio Serra (laercio.serra@gmail.com)
"""

# importa a classe "template" do módulo "string" da biblioteca padrão
# isto permite modelos simples de substituição de string

from string import Template


def include_button_create_new_acct(s_domain, s_nameuser, s_emailassoc):
    """
    # função que cria um formulário com controles ocultos para uma simples passagem de parâmetros
    # quando o botão de comando "Create New Account" for acionado
    :param s_domain: 'asparona'
    :param s_nameuser: 'Laercio Serra'
    :param s_emailassoc: 'laercio.serra@asparona.com'
    :return:
    """
    with open('../views/buttonnewacct.html') as sformb:
        sform_text = sformb.read()

    buttonform = Template(sform_text)

    return buttonform.substitute(domain=s_domain, nameuser=s_nameuser, emailassoc=s_emailassoc)


def include_button_create_new_user(s_domain, s_nameuser, s_emailassoc):
    """
    # função que cria um formulário com controles ocultos para uma simples passagem de parâmetros
    # quando o botão de comando "Create New User" for acionado
    :param s_domain: 'asparona'
    :param s_nameuser: 'Laercio Serra'
    :param s_emailassoc: 'laercio.serra@asparona.com'
    :return:
    """
    with open('../views/buttonnewuser.html') as sformb:
        sform_text = sformb.read()

    buttonform = Template(sform_text)

    return buttonform.substitute(domain=s_domain, nameuser=s_nameuser, emailassoc=s_emailassoc)


def include_button_create_new_wkflw(s_domain, s_nameuser, s_emailassoc):
    """
    # função que cria um formulário com controles ocultos para uma simples passagem de parâmetros
    # quando o botão de comando "Create New Workflow" for acionado
    :param s_domain: 'asparona'
    :param s_nameuser: 'Laercio Serra'
    :param s_emailassoc: 'laercio.serra@asparona.com'
    :return:
    """
    with open('../views/buttonnewwkflw.html') as sformb:
        sform_text = sformb.read()

    buttonform = Template(sform_text)

    return buttonform.substitute(domain=s_domain, nameuser=s_nameuser, emailassoc=s_emailassoc)


def include_data_table(fields):
    """
    # função que apresenta uma tabela somente com o cabeçalho e a mensagem 'No records found'
    # a página em si é armazenada em um arquivo separado em "views/table_nd.html" e
    # os elementos <$headers, $data_tb> são substituídos quando necessários
    :param fields: {field1, field2, field3, field4, field5}
    :return: headers, data_tb
    """
    s_th = ''
    s_itens = len(fields)

    for th in fields:
        s_hd = '<th>' + th + '</th>\n'
        s_th += s_hd

    s_dtb = '   <tr class="warning">\n' + \
            '       <td colspan="' + str(s_itens) + '">\n' + \
            '           <p class="text-center">\n' + \
            '           <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"> ' \
            'No records found . . .</span>\n' + \
            '           </p>\n' + \
            '       </td>\n' + \
            '   </tr>\n'

    with open('../views/table_nd.html') as tablef:
        table_text = tablef.read()

    table = Template(table_text)

    return table.substitute(headers=s_th, data_tb=s_dtb)


def include_data_table_disable(fields, rs_dt_table):
    """
    # função que apresenta os dados em uma tabela estática sem os botões de comandos (edit/delete)
    # a página em si é armazenada em um arquivo separado em "views/table.html" e
    # os elementos <$headers, $data_tb> são substituídos quando necessários
    :param fields: {field1, field2, field3, field4, field5}
    :param rs_dt_table:
    :return: headers, data_tb
    """
    s_th = ''

    for th in fields:
        s_hd = '<th>' + th + '</th>\n'
        s_th += s_hd

    s_dtb = ''

    for record in rs_dt_table:
        s_td = '<tr>\n'
        for col in record:
            s_td += '   <td>' + str(col) + '</td>\n'
            # s_td += '   <td class="text-center"> <!--Fixed Cells -->\n'
            # s_td += '       <a href="#" class="btn btn-default btn-xs disabled">\n'
            # s_td += '           <span class="glyphicon glyphicon-edit"></span> Edit\n'
            # s_td += '       </a>\n'
            # s_td += '       <a href="#" class="btn btn-default btn-xs disabled" data-toggle="modal"
            # data-target="#delete">\n'
            # s_td += '           <span class="glyphicon glyphicon-trash"></span> Delete\n'
            # s_td += '       </a>\n'
            # s_td += '   </td>\n'
        s_td += '</tr>\n'
        s_dtb += s_td

    with open('../views/table.html') as tablef:
        table_text = tablef.read()

    table = Template(table_text)

    return table.substitute(headers=s_th, data_tb=s_dtb)


def include_data_table_enable(domain, fields, rs_dt_table):
    """
    # função que apresenta os dados em uma tabela estática com os botões de comandos (edit/delete) habilitados
    # a página em si é armazenada em um arquivo separado em "views/table.html" e
    # os elementos <$headers, $data_tb> são substituídos quando necessários
    :param domain: 'asparona'
    :param fields: {field1, field2, field3, field4, field5}
    :param rs_dt_table: rows
    :return: headers, data_tb
    """
    s_th = ''

    for th in fields:
        s_hd = '<th>' + th + '</th>\n'
        s_th += s_hd

    s_th += '<!--Fixed Colunm -->\n'
    s_th += '<th class="text-center">Action</th>\n'

    s_dtb = ''

    for record in rs_dt_table:
        s_td = '<tr>\n'
        for col in record:
            s_td += '   <td>' + str(col) + '</td>\n'
        s_td += '   <td class="text-center"> <!--Fixed Cells -->\n'
        s_td += '       <a href="../controls/epay.py?d=' + domain + '&n=' + str(record[0]) + \
                '" class="btn btn-default btn-xs">\n'
        s_td += '           <span class="glyphicon glyphicon-edit"></span> Edit\n'
        s_td += '       </a>\n'
        s_td += '       <a href="../controls/dpay.py?d=' + domain + '&n=' + str(record[0]) + \
                '" class="btn btn-default btn-xs" data-toggle="modal" data-target="#delete">\n'
        s_td += '           <span class="glyphicon glyphicon-trash"></span> Delete\n'
        s_td += '       </a>\n'
        s_td += '   </td>\n'
        s_td += '</tr>\n'
        s_dtb += s_td

    with open('../views/table.html') as tablef:
        table_text = tablef.read()

    table = Template(table_text)

    return table.substitute(headers=s_th, data_tb=s_dtb)


def include_delete_acct():
    """
    # função que cria a janela modal para confirmação da exclusão de um registro.
    # a página em si é armazenada em um arquivo separado em "views/delete.html"
    :return:
    """
    with open('../views/delete_acct.html') as delf:
        del_text = delf.read()

    delete = Template(del_text)

    return delete.substitute()


def include_delete_user():
    """
    # função que cria a janela modal para confirmação da exclusão de um registro.
    # a página em si é armazenada em um arquivo separado em "views/delete.html"
    :return:
    """
    with open('../views/delete_user.html') as delf:
        del_text = delf.read()

    delete = Template(del_text)

    return delete.substitute()


def include_delete_matrix():
    """
    # função que cria a janela modal para confirmação da exclusão de um registro.
    # a página em si é armazenada em um arquivo separado em "views/delete.html"
    :return:
    """
    with open('../views/delete_matrix.html') as delf:
        del_text = delf.read()

    delete = Template(del_text)

    return delete.substitute()


def include_div_e():
    """
    # função que marca as tags </div>
    # esta função usa a sua única string como seu argumento para fechar as tags <div> da página HTML,
    # a página em si é armazenada em um arquivo separado em "views/div_e.html"
    :return:
    """
    with open('../views/div_e.html') as divf:
        div_text = divf.read()

    dive = Template(div_text)

    return dive.substitute()


def include_div_s():
    """
    # função que marca as tags <div>
    # esta função usa a sua única string como seu argumento para abrir as tags <div> da página HTML,
    # a página em si é armazenada em um arquivo separado em "views/div_s.html"
    :return:
    """
    with open('../views/div_s.html') as divf:
        div_text = divf.read()

    divs = Template(div_text)

    return divs.substitute()


def include_dt_tb_enable_users(domain, nameuser, emailassoc, fields, rs_dt_table):
    """
    # função que apresenta os dados em uma tabela estática com os botões de comandos (edit/delete) habilitados
    # a página em si é armazenada em um arquivo separado em "views/table.html" e
    # os elementos <$headers, $data_tb> são substituídos quando necessários
    :param domain: 'asparona'
    :param fields: {field1, field2, field3, field4, field5}
    :param rs_dt_table: rows
    :return: headers, data_tb
    """
    s_th = ''

    for th in fields:
        s_hd = '<th>' + th + '</th>\n'
        s_th += s_hd

    s_th += '<!--Fixed Colunm -->\n'
    s_th += '<th class="text-center">Action</th>\n'

    s_dtb = ''

    for record in rs_dt_table:
        s_td = '<tr>\n'
        for col in record:
            s_td += '   <td>' + str(col) + '</td>\n'
        s_td += '   <td class="text-center"> <!--Fixed Cells -->\n'
        s_td += '       <a href="../controls/eusers.py?d=' + domain + '&u=' + nameuser + '&e=' + emailassoc + \
                '&ue=' + record[1] + '" class="btn btn-default btn-xs">\n'
        s_td += '           <span class="glyphicon glyphicon-edit"></span> Edit\n'
        s_td += '       </a>\n'
        # s_td += '       <a href="../controls/dusers.py?d=' + domain + '&u=' + nameuser + '&e=' + emailassoc + \
        #         '&ud=' + record[1] + '" class="btn btn-default btn-xs" data-toggle="modal" data-target="#delete">\n'
        s_td += '       <a href="javascript:funcDelUser(\'' + domain + '\', \'' + nameuser + '\', \'' + emailassoc + \
                '\', \'' + record[1] + '\')" class="btn btn-default btn-xs">\n'
        s_td += '           <span class="glyphicon glyphicon-trash"></span> Delete\n'
        s_td += '       </a>\n'
        s_td += '   </td>\n'
        s_td += '</tr>\n'
        s_dtb += s_td

    with open('../views/table.html') as tablef:
        table_text = tablef.read()

    table = Template(table_text)

    return table.substitute(headers=s_th, data_tb=s_dtb)


def include_dt_tb_enable_acct(domain, nameuser, emailassoc, fields, rs_dt_table):
    """
    # função que apresenta os dados em uma tabela estática com os botões de comandos (edit/delete) habilitados
    # a página em si é armazenada em um arquivo separado em "views/table.html" e
    # os elementos <$headers, $data_tb> são substituídos quando necessários
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@gmail.com'
    :param fields: {field1, field2, field3, field4, field5}
    :param rs_dt_table: {(v1, v2, v3), (v4, v5, v6), (v7, v8, v9)}
    :return: headers, data_tb
    """
    s_th = ''

    for th in fields:
        s_hd = '<th>' + th + '</th>\n'
        s_th += s_hd

    s_th += '<!--Fixed Colunm -->\n'
    s_th += '<th class="text-center">Action</th>\n'

    s_dtb = ''

    for record in rs_dt_table:
        s_td = '<tr>\n'
        for col in record:
            s_td += '   <td>' + str(col) + '</td>\n'
        s_td += '   <td class="text-center"> <!--Fixed Cells -->\n'
        s_td += '       <a href="../controls/eacct.py?d=' + domain + '&u=' + nameuser + '&e=' + emailassoc + \
                '&ae=' + record[0] + '" class="btn btn-default btn-xs">\n'
        s_td += '           <span class="glyphicon glyphicon-edit"></span> Edit\n'
        s_td += '       </a>\n'
        # s_td += '       <a href="../controls/dacct.py?d=' + domain + '&u=' + nameuser + '&e=' + emailassoc + \
        #         '&ad=' + record[0] + '" class="btn btn-default btn-xs" data-toggle="modal" data-target="#delete">\n'
        s_td += '       <a href="javascript:funcDelAcct(\'' + domain + '\', \'' + nameuser + '\', \'' + emailassoc + \
                '\', \'' + record[0] + '\')" class="btn btn-default btn-xs">\n'
        s_td += '           <span class="glyphicon glyphicon-trash"></span> Delete\n'
        s_td += '       </a>\n'
        s_td += '   </td>\n'
        s_td += '</tr>\n'
        s_dtb += s_td

    with open('../views/table.html') as tablef:
        table_text = tablef.read()

    table = Template(table_text)

    return table.substitute(headers=s_th, data_tb=s_dtb)


def include_dt_tb_enable_matrix(domain, nameuser, emailassoc, fields, rs_dt_table):
    """
    # função que apresenta os dados em uma tabela estática com os botões de comandos (edit/delete) habilitados
    # a página em si é armazenada em um arquivo separado em "views/table.html" e
    # os elementos <$headers, $data_tb> são substituídos quando necessários
    :param domain: 'asparona'
    :param fields: {field1, field2, field3, field4, field5}
    :param rs_dt_table: rows
    :return: headers, data_tb
    """
    s_th = ''

    for th in fields:
        s_hd = '<th>' + th + '</th>\n'
        s_th += s_hd

    s_th += '<!--Fixed Colunm -->\n'
    s_th += '<th class="text-center">Action</th>\n'

    s_dtb = ''

    for record in rs_dt_table:
        s_td = '<tr>\n'
        for col in record:
            s_td += '   <td>' + str(col) + '</td>\n'
        s_td += '   <td class="text-center"> <!--Fixed Cells -->\n'
        s_td += '       <a href="../controls/ewkflw.py?d=' + domain + '&u=' + nameuser + '&e=' + emailassoc + \
                '&we=' + str(record[0]) + '" class="btn btn-default btn-xs">\n'
        s_td += '           <span class="glyphicon glyphicon-edit"></span> Edit\n'
        s_td += '       </a>\n'
        # s_td += '       <a href="../controls/dwkflw.py?d=' + domain + '&u=' + nameuser + '&e=' + emailassoc + \
        #         '&ud=' + record[1] + '" class="btn btn-default btn-xs" data-toggle="modal" data-target="#delete">\n'
        s_td += '       <a href="javascript:funcDelWkflw(\'' + domain + '\', \'' + nameuser + '\', \'' + emailassoc + \
                '\', \'' + str(record[0]) + '\')" class="btn btn-default btn-xs">\n'
        s_td += '           <span class="glyphicon glyphicon-trash"></span> Delete\n'
        s_td += '       </a>\n'
        s_td += '   </td>\n'
        s_td += '</tr>\n'
        s_dtb += s_td

    with open('../views/table.html') as tablef:
        table_text = tablef.read()

    table = Template(table_text)

    return table.substitute(headers=s_th, data_tb=s_dtb)


def include_footer():
    """
    # função que cria o rodapé
    # esta função usa a sua única string como seu argumento para criar o rodapé da página HTML,
    # a página em si é armazenada em um arquivo separado em "views/footer.html"
    :return:
    """
    with open('../views/footer.html') as footf:
        foot_text = footf.read()

    footer = Template(foot_text)

    return footer.substitute()


def include_footer_login():
    """
    # função que cria o rodapé da página de login do usuário para acesso ao sistema
    # esta função usa a sua única string como seu argumento para criar o rodapé da página HTML,
    # a página em si é armazenada em um arquivo separado em "views/footer_l.html"
    :return:
    """
    with open('../views/footer_l.html') as footf:
        foot_text = footf.read()

    footer_l = Template(foot_text)

    return footer_l.substitute()


def include_footer_reg():
    """
    # função que cria o rodapé da página de registro (cadastro) do associado
    # esta função usa a sua única string como seu argumento para criar o cabeçalho da página HTML,
    # a página em si é armazenada em um arquivo separado em "views/footer_r.html"
    :return:
    """
    with open('../views/footer_r.html') as footf:
        foot_text = footf.read()

    footer_r = Template(foot_text)

    return footer_r.substitute()


def include_form_cu(domain, nameuser, emailassoc):
    """
    # função que cria o formulário: create new user
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_cu
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :return:
    """
    form_cu = '            <form class="form-horizontal" role="form" method="post" action="../controls/iusers.py">\n'
    form_cu += '            <div class="form-group">\n'
    form_cu += '                 <label class="col-sm-4 control-label" for="domain_nu">Domain Name</label>\n'
    form_cu += '                 <div class="col-sm-6">\n'
    form_cu += '                     <input class="form-control" id="domain_nu" name="domain_nu" type="text" ' \
               'value="' + domain + '" readonly />\n'
    form_cu += '                 </div>\n'
    form_cu += '            </div>\n'
    form_cu += '            <div class="form-group">\n'
    form_cu += '                <label class="col-sm-4 control-label" for="fname">First Name User</label>\n'
    form_cu += '                <div class="col-sm-6">\n'
    form_cu += '                      <input class="form-control" id="fname" name= "fname" type="text" ' \
               'value="" required />\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    form_cu += '            <div class="form-group">\n'
    form_cu += '                <label class="col-sm-4 control-label" for="lname">Last Name User</label>\n'
    form_cu += '                <div class="col-sm-6">\n'
    form_cu += '                      <input class="form-control" id="lname" name= "lname" type="text" ' \
               'value="" required />\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    form_cu += '            <div class="form-group">\n'
    form_cu += '                <label class="col-sm-4 control-label" for="email">E-mail User</label>\n'
    form_cu += '                <div class="col-sm-6">\n'
    form_cu += '                      <input class="form-control" id="email" name= "email" type="text" ' \
               'value="" required />\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    form_cu += '            <div class="form-group">\n'
    form_cu += '                <label class="col-sm-4 control-label" for="pwd">Password User</label>\n'
    form_cu += '                <div class="col-sm-6">\n'
    form_cu += '                      <input class="form-control" id="pwd" name= "pwd" type="password" ' \
               'value="" required />\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    form_cu += '            <div class="form-group">\n'
    form_cu += '                <label class="col-sm-4 control-label" for="profile">Profile User</label>\n'
    form_cu += '                <div class="col-sm-6">\n'
    form_cu += '                      <select class="form-control" id="profile" name="profile">\n'
    form_cu += '                      	<option value="S">Supervisor </option>\n'
    form_cu += '                      	<option value="U">User </option>\n'
    form_cu += '                      </select>\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    form_cu += '            <div class="form-group">\n'
    form_cu += '                <label class="col-sm-4 control-label" for="task">Task User</label>\n'
    form_cu += '                <div class="col-sm-6">\n'
    form_cu += '                      <select class="form-control" id="task" name="task">\n'
    form_cu += '                      	<option value="A">Approve expense </option>\n'
    form_cu += '                      	<option value="C">Create expense </option>\n'
    form_cu += '                      	<option value="P">Pay expense </option>\n'
    form_cu += '                      </select>\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    form_cu += '            <div class="form-group">\n'
    form_cu += '                 <div class="col-sm-6">\n'
    form_cu += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_cu += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_cu += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_cu += '                 </div>\n'
    form_cu += '            </div>\n'
    form_cu += '            <div class="form-group">\n'
    form_cu += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_cu += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_cu += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_cu += '                    <a class="btn btn-default" href="../controls/users.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    form_cu += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_cu)


def include_form_cu_err(domain_newuser, fname_newuser, lname_newuser, email_newuser,
                        pwd_newuser, profile_newuser, task_newuser, domain, nameuser, emailassoc, field):
    """
    # função que cria o formulário: create new user para tratamento dos erros encontrados
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_cu
    :param domain_newuser:'asparona'
    :param fname_newuser: 'Laercio'
    :param lname_newuser: 'Serra'
    :param email_newuser: 'laercio.serra@asparona.com'
    :param pwd_newuser: 'qwertyu#$@'
    :param profile_newuser: 'U'
    :param task_newuser: 'U'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param field: ['D', 'P', 'T']
    :return:
    """
    form_cu = '            <form class="form-horizontal" role="form" method="post" action="../controls/iusers.py">\n'
    if field.count('D') != 0:
        form_cu += '            <div class="form-group has-error">\n'
    else:
        form_cu += '            <div class="form-group">\n'
    form_cu += '                 <label class="col-sm-4 control-label" for="domain_nu">Domain Name</label>\n'
    form_cu += '                 <div class="col-sm-6">\n'
    form_cu += '                     <input class="form-control" id="domain_nu" name="domain_nu" type="text" ' \
               'value="' + domain_newuser + '" readonly/>\n'
    form_cu += '                 </div>\n'
    form_cu += '            </div>\n'
    if field.count('F') != 0:
        form_cu += '            <div class="form-group has-error">\n'
    else:
        form_cu += '            <div class="form-group">\n'
    form_cu += '                <label class="col-sm-4 control-label" for="fname">First Name User</label>\n'
    form_cu += '                <div class="col-sm-6">\n'
    form_cu += '                      <input class="form-control" id="fname" name= "fname" type="text" value="' + \
               fname_newuser + '" required />\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    if field.count('L') != 0:
        form_cu += '            <div class="form-group has-error">\n'
    else:
        form_cu += '            <div class="form-group">\n'
    form_cu += '                <label class="col-sm-4 control-label" for="lname">Last Name User</label>\n'
    form_cu += '                <div class="col-sm-6">\n'
    form_cu += '                      <input class="form-control" id="lname" name= "lname" type="text" value="' + \
               lname_newuser + '" required />\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    if field.count('E') != 0:
        form_cu += '            <div class="form-group has-error">\n'
    else:
        form_cu += '            <div class="form-group">\n'
    form_cu += '                <label class="col-sm-4 control-label" for="email">E-mail User</label>\n'
    form_cu += '                <div class="col-sm-6">\n'
    form_cu += '                      <input class="form-control" id="email" name= "email" type="text" value="' + \
               email_newuser + '" required />\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    if field.count('W') != 0:
        form_cu += '            <div class="form-group has-error">\n'
    else:
        form_cu += '            <div class="form-group">\n'
    form_cu += '                <label class="col-sm-4 control-label" for="pwd">Password User</label>\n'
    form_cu += '                <div class="col-sm-6">\n'
    form_cu += '                      <input class="form-control" id="pwd" name= "pwd" type="password" value="' + \
               pwd_newuser + '" required />\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    if field.count('P') != 0:
        form_cu += '            <div class="form-group has-error">\n'
    else:
        form_cu += '            <div class="form-group">\n'
    form_cu += '                <label class="col-sm-4 control-label" for="profile">Profile User</label>\n'
    form_cu += '                <div class="col-sm-6">\n'
    form_cu += '                      <select class="form-control" id="profile" name="profile">\n'
    if profile_newuser == 'S':
        form_cu += '                      	<option selected value="S">Supervisor </option>\n'
        form_cu += '                      	<option value="U">User </option>\n'
    else:
        form_cu += '                      	<option value="S">Supervisor </option>\n'
        form_cu += '                      	<option selected value="U">User </option>\n'
    form_cu += '                      </select>\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    if field.count('T') != 0:
        form_cu += '            <div class="form-group has-error">\n'
    else:
        form_cu += '            <div class="form-group">\n'
    form_cu += '                <label class="col-sm-4 control-label" for="task">Task User</label>\n'
    form_cu += '                <div class="col-sm-6">\n'
    form_cu += '                      <select class="form-control" id="task" name="task">\n'
    if task_newuser == 'A':
        form_cu += '                      	<option selected value="A">Approve expense </option>\n'
        form_cu += '                      	<option value="C">Create expense </option>\n'
        form_cu += '                      	<option value="P">Pay expense </option>\n'
    elif task_newuser == 'C':
        form_cu += '                      	<option value="A">Approve expense </option>\n'
        form_cu += '                      	<option selected value="C">Create expense </option>\n'
        form_cu += '                      	<option value="P">Pay expense </option>\n'
    else:
        form_cu += '                      	<option value="A">Approve expense </option>\n'
        form_cu += '                      	<option value="C">Create expense </option>\n'
        form_cu += '                      	<option selected value="P">Pay expense </option>\n'
    form_cu += '                      </select>\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    form_cu += '            <div class="form-group">\n'
    form_cu += '                 <div class="col-sm-6">\n'
    form_cu += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_cu += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_cu += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_cu += '                 </div>\n'
    form_cu += '            </div>\n'
    form_cu += '            <div class="form-group">\n'
    form_cu += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_cu += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_cu += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_cu += '                    <a class="btn btn-default" href="../controls/users.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_cu += '                </div>\n'
    form_cu += '            </div>\n'
    form_cu += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_cu)


def include_form_cw(domain, nameuser, emailassoc, publishers, approvers, payers):
    """
    # função que cria o formulário: create new workflow
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_cw
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param publishers: {id_user:name_user}
    :param approvers: {id_user:name_user}
    :param payers: {id_user:name_user}
    :return:
    """
    form_cw = '            <form class="form-horizontal" role="form" method="post" action="../controls/iwkflw.py">\n'
    form_cw += '            <div class="form-group">\n'
    form_cw += '                 <label class="col-sm-4 control-label" for="publisher">Publisher</label>\n'
    form_cw += '                 <div class="col-sm-6">\n'
    form_cw += '                      <select class="form-control" id="publisher" name="publisher" required>\n'
    if publishers is None:
        form_cw += '                        <option value="">No record</option>\n'
    else:
        for p in publishers:
            form_cw += '                        <option value="' + str(p[0]) + '">' + p[1] + '</option>\n'
    form_cw += '                      </select>\n'
    form_cw += '                 </div>\n'
    form_cw += '            </div>\n'
    form_cw += '            <div class="form-group">\n'
    form_cw += '                <label class="col-sm-4 control-label" for="approver">Approver</label>\n'
    form_cw += '                <div class="col-sm-6">\n'
    form_cw += '                      <select class="form-control" id="approver" name="approver" required>\n'
    if approvers is None:
        form_cw += '                        <option value="">No record</option>\n'
    else:
        for a in approvers:
            form_cw += '                        <option value="' + str(a[0]) + '">' + a[1] + '</option>\n'
    form_cw += '                      </select>\n'
    form_cw += '                </div>\n'
    form_cw += '            </div>\n'
    form_cw += '            <div class="form-group">\n'
    form_cw += '                <label class="col-sm-4 control-label" for="payer">Payer</label>\n'
    form_cw += '                <div class="col-sm-6">\n'
    form_cw += '                      <select class="form-control" id="payer" name="payer" required>\n'
    if payers is None:
        form_cw += '                        <option value="">No record</option>\n'
    else:
        for y in payers:
            form_cw += '                        <option value="' + str(y[0]) + '">' + y[1] + '</option>\n'
    form_cw += '                      </select>\n'
    form_cw += '                </div>\n'
    form_cw += '            </div>\n'
    form_cw += '            <div class="form-group">\n'
    form_cw += '                 <div class="col-sm-6">\n'
    form_cw += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_cw += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_cw += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_cw += '                 </div>\n'
    form_cw += '            </div>\n'
    form_cw += '            <div class="form-group">\n'
    form_cw += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_cw += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_cw += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_cw += '                    <a class="btn btn-default" href="../controls/wkflw.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_cw += '                </div>\n'
    form_cw += '            </div>\n'
    form_cw += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_cw)


def include_form_cw_err(domain, nameuser, emailassoc, publishers, approvers, payers, field):
    """
    # função que cria o formulário: create new workflow para tratamento dos erros encontrados
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_cw
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param publishers: {id_user:name_user}
    :param approvers: {id_user:name_user}
    :param payers: {id_user:name_user}
    :param field: ['P', 'A', 'Y']
    :return:
    """
    form_cw = '            <form class="form-horizontal" role="form" method="post" action="../controls/iwkflw.py">\n'
    if field.count('P') != 0:
        form_cw += '            <div class="form-group has-error">\n'
    else:
        form_cw += '            <div class="form-group">\n'
    form_cw += '                 <label class="col-sm-4 control-label" for="publisher">Publisher</label>\n'
    form_cw += '                 <div class="col-sm-6">\n'
    form_cw += '                      <select class="form-control" id="publisher" name="publisher" required>\n'
    if publishers is None:
        form_cw += '                        <option value="">No record</option>\n'
    else:
        for p in publishers:
            form_cw += '                        <option value="' + str(p[0]) + '">' + p[1] + '</option>\n'
    form_cw += '                      </select>\n'
    form_cw += '                 </div>\n'
    form_cw += '            </div>\n'
    if field.count('A') != 0:
        form_cw += '            <div class="form-group has-error">\n'
    else:
        form_cw += '            <div class="form-group">\n'
    form_cw += '                <label class="col-sm-4 control-label" for="approver">Approver</label>\n'
    form_cw += '                <div class="col-sm-6">\n'
    form_cw += '                      <select class="form-control" id="approver" name="approver" required>\n'
    if approvers is None:
        form_cw += '                        <option value="">No record</option>\n'
    else:
        for a in approvers:
            form_cw += '                        <option value="' + str(a[0]) + '">' + a[1] + '</option>\n'
    form_cw += '                      </select>\n'
    form_cw += '                </div>\n'
    form_cw += '            </div>\n'
    if field.count('Y') != 0:
        form_cw += '            <div class="form-group has-error">\n'
    else:
        form_cw += '            <div class="form-group">\n'
    form_cw += '                <label class="col-sm-4 control-label" for="payer">Payer</label>\n'
    form_cw += '                <div class="col-sm-6">\n'
    form_cw += '                      <select class="form-control" id="payer" name="payer" required>\n'
    if payers is None:
        form_cw += '                        <option value="">No record</option>\n'
    else:
        for y in payers:
            form_cw += '                        <option value="' + str(y[0]) + '">' + y[1] + '</option>\n'
    form_cw += '                      </select>\n'
    form_cw += '                </div>\n'
    form_cw += '            </div>\n'
    form_cw += '            <div class="form-group">\n'
    form_cw += '                 <div class="col-sm-6">\n'
    form_cw += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_cw += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_cw += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_cw += '                 </div>\n'
    form_cw += '            </div>\n'
    form_cw += '            <div class="form-group">\n'
    form_cw += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_cw += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_cw += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_cw += '                    <a class="btn btn-default" href="../controls/wkflw.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_cw += '                </div>\n'
    form_cw += '            </div>\n'
    form_cw += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_cw)


def include_form_cp():
    """
    # função que cria o form para alteração de senha do associado
    # a página em si é armazenada em um arquivo separado em "views/f_chgpwd.html"
    :return:
    """
    with open('../views/f_chgpwd.html') as formf:
        form_text = formf.read()

    formcp = Template(form_text)

    return formcp.substitute()


def include_form_ct():
    """
    # função que cria o form de contato para envio de mensagem
    # a página em si é armazenada em um arquivo separado em "views/f_contact.html"
    :return:
    """
    with open('../views/f_contact.html') as formf:
        form_text = formf.read()

    formct = Template(form_text)

    return formct.substitute()


def include_form_eu(domain, nameuser, emailassoc, d_ue, fn_ue, ln_ue, e_ue, p_ue, t_ue):
    """
    # função que cria o formulário: edit user
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_eu
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :return:
    """
    form_eu = '            <form class="form-horizontal" role="form" method="post" action="../controls/uusers.py">\n'
    form_eu += '            <div class="form-group">\n'
    form_eu += '                 <label class="col-sm-4 control-label" for="domain_eu">Domain Name</label>\n'
    form_eu += '                 <div class="col-sm-6">\n'
    form_eu += '                     <input class="form-control" id="domain_eu" name="domain_eu" type="text" ' \
               'value="' + d_ue + '" readonly/>\n'
    form_eu += '                 </div>\n'
    form_eu += '            </div>\n'
    form_eu += '            <div class="form-group">\n'
    form_eu += '                <label class="col-sm-4 control-label" for="fname">First Name User</label>\n'
    form_eu += '                <div class="col-sm-6">\n'
    form_eu += '                      <input class="form-control" id="fname" name= "fname" type="text" ' \
               'value="' + fn_ue + '" required />\n'
    form_eu += '                </div>\n'
    form_eu += '            </div>\n'
    form_eu += '            <div class="form-group">\n'
    form_eu += '                <label class="col-sm-4 control-label" for="lname">Last Name User</label>\n'
    form_eu += '                <div class="col-sm-6">\n'
    form_eu += '                      <input class="form-control" id="lname" name= "lname" type="text" ' \
               'value="' + ln_ue + '" required />\n'
    form_eu += '                </div>\n'
    form_eu += '            </div>\n'
    form_eu += '            <div class="form-group">\n'
    form_eu += '                <label class="col-sm-4 control-label" for="email">E-mail User</label>\n'
    form_eu += '                <div class="col-sm-6">\n'
    form_eu += '                      <input class="form-control" id="email" name= "email" type="text" ' \
               'value="' + e_ue + '" required />\n'
    form_eu += '                </div>\n'
    form_eu += '            </div>\n'
    form_eu += '            <div class="form-group">\n'
    form_eu += '                <label class="col-sm-4 control-label" for="profile">Profile User</label>\n'
    form_eu += '                <div class="col-sm-6">\n'
    form_eu += '                      <select class="form-control" id="profile" name="profile">\n'
    if p_ue == 'S':
        form_eu += '                      	<option selected value="S">Supervisor </option>\n'
        form_eu += '                      	<option value="U">User </option>\n'
    else:
        form_eu += '                      	<option value="S">Supervisor </option>\n'
        form_eu += '                      	<option selected value="U">User </option>\n'
    form_eu += '                      </select>\n'
    form_eu += '                </div>\n'
    form_eu += '            </div>\n'
    form_eu += '            <div class="form-group">\n'
    form_eu += '                <label class="col-sm-4 control-label" for="task">Task User</label>\n'
    form_eu += '                <div class="col-sm-6">\n'
    form_eu += '                      <select class="form-control" id="task" name="task">\n'
    if t_ue == 'A':
        form_eu += '                      	<option selected value="A">Approve expense </option>\n'
        form_eu += '                      	<option value="C">Create expense </option>\n'
        form_eu += '                      	<option value="P">Pay expense </option>\n'
    elif t_ue == 'C':
        form_eu += '                      	<option value="A">Approve expense </option>\n'
        form_eu += '                      	<option selected value="C">Create expense </option>\n'
        form_eu += '                      	<option value="P">Pay expense </option>\n'
    else:
        form_eu += '                      	<option value="A">Approve expense </option>\n'
        form_eu += '                      	<option value="C">Create expense </option>\n'
        form_eu += '                      	<option selected value="P">Pay expense </option>\n'
    form_eu += '                      </select>\n'
    form_eu += '                </div>\n'
    form_eu += '            </div>\n'
    form_eu += '            <div class="form-group">\n'
    form_eu += '                 <div class="col-sm-6">\n'
    form_eu += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_eu += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_eu += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_eu += '                 </div>\n'
    form_eu += '            </div>\n'
    form_eu += '            <div class="form-group">\n'
    form_eu += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_eu += '                    <input type="submit" name="save" value="Update" class="btn btn-primary">\n'
    form_eu += '                    <a class="btn btn-default" href="../controls/users.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_eu += '                </div>\n'
    form_eu += '            </div>\n'
    form_eu += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_eu)


def include_form_eu_err(domain_eduser, fname_eduser, lname_eduser, email_eduser,
                        profile_eduser, task_eduser, domain, nameuser, emailassoc, field):
    """
    # função que cria o formulário: edit user para tratamento dos erros encontrados
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_eu
    :param domain_eduser:'asparona'
    :param fname_eduser: 'Laercio'
    :param lname_eduser: 'Serra'
    :param email_eduser: 'laercio.serra@asparona.com'
    :param profile_eduser: 'U'
    :param task_eduser: 'U'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param field: ['D', 'P', 'T']
    :return:
    """
    form_eu = '            <form class="form-horizontal" role="form" method="post" action="../controls/uusers.py">\n'
    if field.count('D') != 0:
        form_eu += '            <div class="form-group has-error">\n'
    else:
        form_eu += '            <div class="form-group">\n'
    form_eu += '                 <label class="col-sm-4 control-label" for="domain_nu">Domain Name</label>\n'
    form_eu += '                 <div class="col-sm-6">\n'
    form_eu += '                     <input class="form-control" id="domain_nu" name="domain_nu" type="text" ' \
               'value="' + domain_eduser + '" readonly/>\n'
    form_eu += '                 </div>\n'
    form_eu += '            </div>\n'
    if field.count('F') != 0:
        form_eu += '            <div class="form-group has-error">\n'
    else:
        form_eu += '            <div class="form-group">\n'
    form_eu += '                <label class="col-sm-4 control-label" for="fname">First Name User</label>\n'
    form_eu += '                <div class="col-sm-6">\n'
    form_eu += '                      <input class="form-control" id="fname" name= "fname" type="text" value="' + \
               fname_eduser + '" required />\n'
    form_eu += '                </div>\n'
    form_eu += '            </div>\n'
    if field.count('L') != 0:
        form_eu += '            <div class="form-group has-error">\n'
    else:
        form_eu += '            <div class="form-group">\n'
    form_eu += '                <label class="col-sm-4 control-label" for="lname">Last Name User</label>\n'
    form_eu += '                <div class="col-sm-6">\n'
    form_eu += '                      <input class="form-control" id="lname" name= "lname" type="text" value="' + \
               lname_eduser + '" required />\n'
    form_eu += '                </div>\n'
    form_eu += '            </div>\n'
    if field.count('E') != 0:
        form_eu += '            <div class="form-group has-error">\n'
    else:
        form_eu += '            <div class="form-group">\n'
    form_eu += '                <label class="col-sm-4 control-label" for="email">E-mail User</label>\n'
    form_eu += '                <div class="col-sm-6">\n'
    form_eu += '                      <input class="form-control" id="email" name= "email" type="text" value="' + \
               email_eduser + '" required />\n'
    form_eu += '                </div>\n'
    form_eu += '            </div>\n'
    if field.count('P') != 0:
        form_eu += '            <div class="form-group has-error">\n'
    else:
        form_eu += '            <div class="form-group">\n'
    form_eu += '                <label class="col-sm-4 control-label" for="profile">Profile User</label>\n'
    form_eu += '                <div class="col-sm-6">\n'
    form_eu += '                      <select class="form-control" id="profile" name="profile">\n'
    if profile_eduser == 'S':
        form_eu += '                        <option selected value="S">Supervisor </option>\n'
        form_eu += '                        <option value="U">User </option>\n'
    else:
        form_eu += '                        <option value="S">Supervisor </option>\n'
        form_eu += '                        <option selected value="U">User </option>\n'
    form_eu += '                      </select>\n'
    form_eu += '                </div>\n'
    form_eu += '            </div>\n'
    if field.count('T') != 0:
        form_eu += '            <div class="form-group has-error">\n'
    else:
        form_eu += '            <div class="form-group">\n'
    form_eu += '                <label class="col-sm-4 control-label" for="task">Task User</label>\n'
    form_eu += '                <div class="col-sm-6">\n'
    form_eu += '                      <select class="form-control" id="task" name="task">\n'
    if task_eduser == 'A':
        form_eu += '                        <option selected value="A">Approve expense </option>\n'
        form_eu += '                        <option value="C">Create expense </option>\n'
        form_eu += '                        <option value="P">Pay expense </option>\n'
    elif task_eduser == 'C':
        form_eu += '                        <option value="A">Approve expense </option>\n'
        form_eu += '                        <option selected value="C">Create expense </option>\n'
        form_eu += '                        <option value="P">Pay expense </option>\n'
    else:
        form_eu += '                        <option value="A">Approve expense </option>\n'
        form_eu += '                        <option value="C">Create expense </option>\n'
        form_eu += '                        <option selected value="P">Pay expense </option>\n'
    form_eu += '                      </select>\n'
    form_eu += '                </div>\n'
    form_eu += '            </div>\n'
    form_eu += '            <div class="form-group">\n'
    form_eu += '                 <div class="col-sm-6">\n'
    form_eu += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_eu += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_eu += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_eu += '                 </div>\n'
    form_eu += '            </div>\n'
    form_eu += '            <div class="form-group">\n'
    form_eu += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_eu += '                    <input type="submit" name="save" value="Update" class="btn btn-primary">\n'
    form_eu += '                    <a class="btn btn-default" href="../controls/users.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_eu += '                </div>\n'
    form_eu += '            </div>\n'
    form_eu += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_eu)


def include_form_ew(wkflw, domain, nameuser, emailassoc, id_publisher, publisher, id_approver, approver,
                    id_payer, payer, approvers, payers):
    """
    # função que cria o formulário: edit workflow
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_ew
    :param wkflw: '12'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param id_publisher: '1'
    :param publisher: 'Larissa Serra'
    :param id_approver: '33'
    :param approver: 'Dilma Roussef'
    :param id_payer: '14'
    :param payer: 'Luiz Inacio da Silva'
    :param approvers: {id_user:name_user}
    :param payers: {id_user:name_user}
    :return:
    """
    form_ew = '            <form class="form-horizontal" role="form" method="post" action="../controls/uwkflw.py">\n'
    form_ew += '            <div class="form-group">\n'
    form_ew += '                 <label class="col-sm-4 control-label" for="publisher">Publisher</label>\n'
    form_ew += '                 <div class="col-sm-6">\n'
    form_ew += '                      <select class="form-control" id="publisher" name="publisher" readonly>\n'
    form_ew += '                        <option selected value="' + str(id_publisher) + '">' + publisher + '</option>\n'
    form_ew += '                      </select>\n'
    form_ew += '                 </div>\n'
    form_ew += '            </div>\n'
    form_ew += '            <div class="form-group">\n'
    form_ew += '                <label class="col-sm-4 control-label" for="approver">Approver</label>\n'
    form_ew += '                <div class="col-sm-6">\n'
    form_ew += '                      <select class="form-control" id="approver" name="approver" required>\n'
    if approvers is None:
        form_ew += '                        <option value="' + str(id_approver) + '">' + approver + '</option>\n'
    else:
        for a in approvers:
            form_ew += '                        <option value="' + str(a[0]) + '">' + a[1] + '</option>\n'
        form_ew += '                        <option selected value="' + str(id_approver) + '">' + approver + \
                   '</option>\n'
    form_ew += '                      </select>\n'
    form_ew += '                </div>\n'
    form_ew += '            </div>\n'
    form_ew += '            <div class="form-group">\n'
    form_ew += '                <label class="col-sm-4 control-label" for="payer">Payer</label>\n'
    form_ew += '                <div class="col-sm-6">\n'
    form_ew += '                      <select class="form-control" id="payer" name="payer" required>\n'
    if payers is None:
        form_ew += '                        <option value="' + str(id_payer) + '">' + payer + '</option>\n'
    else:
        for y in payers:
            form_ew += '                        <option value="' + str(y[0]) + '">' + y[1] + '</option>\n'
        form_ew += '                        <option selected value="' + str(id_payer) + '">' + payer + '</option>\n'
    form_ew += '                      </select>\n'
    form_ew += '                </div>\n'
    form_ew += '            </div>\n'
    form_ew += '            <div class="form-group">\n'
    form_ew += '                 <div class="col-sm-6">\n'
    form_ew += '                     <input type="hidden" id="wkflw" name="wkflw" value="' + wkflw + '"/>\n'
    form_ew += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_ew += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_ew += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_ew += '                 </div>\n'
    form_ew += '            </div>\n'
    form_ew += '            <div class="form-group">\n'
    form_ew += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_ew += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_ew += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_ew += '                    <a class="btn btn-default" href="../controls/wkflw.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_ew += '                </div>\n'
    form_ew += '            </div>\n'
    form_ew += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_ew)


def include_form_ew_err(wkflw, domain, nameuser, emailassoc, id_publisher, publisher, id_approver, approver,
                        id_payer, payer, approvers, payers, field):
    """
    # função que cria o formulário: edit workflow para tratamento dos erros encontrados
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_ew
    :param wkflw: '12'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param id_publisher: '1'
    :param publisher: 'Larissa Serra'
    :param id_approver: '33'
    :param approver: 'Dilma Roussef'
    :param id_payer: '14'
    :param payer: 'Luiz Inacio da Silva'
    :param approvers: {id_user:name_user}
    :param payers: {id_user:name_user}
    :param field: ['P', 'A', 'Y']
    :return:
    """
    form_ew = '            <form class="form-horizontal" role="form" method="post" action="../controls/uwkflw.py">\n'
    form_ew += '            <div class="form-group">\n'
    form_ew += '                 <label class="col-sm-4 control-label" for="publisher">Publisher</label>\n'
    if field.count('P') != 0:
        form_ew += '            <div class="form-group has-error">\n'
    else:
        form_ew += '            <div class="form-group">\n'
    form_ew += '                      <select class="form-control" id="publisher" name="publisher" readonly>\n'
    form_ew += '                        <option selected value="' + str(id_publisher) + '">' + publisher + '</option>\n'
    form_ew += '                      </select>\n'
    form_ew += '                 </div>\n'
    form_ew += '            </div>\n'
    if field.count('A') != 0:
        form_ew += '            <div class="form-group has-error">\n'
    else:
        form_ew += '            <div class="form-group">\n'
    form_ew += '                <label class="col-sm-4 control-label" for="approver">Approver</label>\n'
    form_ew += '                <div class="col-sm-6">\n'
    form_ew += '                      <select class="form-control" id="approver" name="approver" required>\n'
    if approvers is None:
        form_ew += '                        <option value="' + str(id_approver) + '">' + approver + '</option>\n'
    else:
        for a in approvers:
            form_ew += '                        <option value="' + str(a[0]) + '">' + a[1] + '</option>\n'
        form_ew += '                        <option selected value="' + str(id_approver) + '">' + approver + \
                   '</option>\n'
    form_ew += '                      </select>\n'
    form_ew += '                </div>\n'
    form_ew += '            </div>\n'
    if field.count('Y') != 0:
        form_ew += '            <div class="form-group has-error">\n'
    else:
        form_ew += '            <div class="form-group">\n'
    form_ew += '                <label class="col-sm-4 control-label" for="payer">Payer</label>\n'
    form_ew += '                <div class="col-sm-6">\n'
    form_ew += '                      <select class="form-control" id="payer" name="payer" required>\n'
    if payers is None:
        form_ew += '                        <option value="' + str(id_payer) + '">' + payer + '</option>\n'
    else:
        for y in payers:
            form_ew += '                        <option value="' + str(y[0]) + '">' + y[1] + '</option>\n'
        form_ew += '                        <option selected value="' + str(id_payer) + '">' + payer + '</option>\n'
    form_ew += '                      </select>\n'
    form_ew += '                </div>\n'
    form_ew += '            </div>\n'
    form_ew += '            <div class="form-group">\n'
    form_ew += '                 <div class="col-sm-6">\n'
    form_ew += '                     <input type="hidden" id="wkflw" name="wkflw" value="' + wkflw + '"/>\n'
    form_ew += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_ew += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_ew += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_ew += '                 </div>\n'
    form_ew += '            </div>\n'
    form_ew += '            <div class="form-group">\n'
    form_ew += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_ew += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_ew += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_ew += '                    <a class="btn btn-default" href="../controls/wkflw.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_ew += '                </div>\n'
    form_ew += '            </div>\n'
    form_ew += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_ew)


def include_form_gl():
    """
    # função que cria o form para pesquisa do e-mail do associado
    # e recuperação dos dados de login para serem enviados por e-mail
    # a página em si é armazenada em um arquivo separado em "views/f_getlogin.html"
    :return:
    """
    with open('../views/f_getlogin.html') as formf:
        form_text = formf.read()

    formgl = Template(form_text)

    return formgl.substitute()


def include_form_login():
    """
    # função que cria o form de login do usuário para acesso ao sistema
    # a página em si é armazenada em um arquivo separado em "views/form_l.html"
    :return:
    """
    with open('../views/form_l.html') as formf:
        form_text = formf.read()

    form_l = Template(form_text)

    return form_l.substitute()


def include_form_login_err(field):
    """
    # função que cria o form de login para acesso ao sistema com os erros
    # para serem verificados e tratados pelo usuário
    # a página em si é armazenada em um arquivo separado em "views/form_l_err.html" e o
    # elemento $form é substituído quando necessário por form_l_err
    :param field: ['D', 'P', 'T']
    :return:
    """
    form_l_err = '                        <h2>Please Sign In</h2>\n'
    form_l_err += '                        <hr class="colorgraph">\n'
    if field.count('D') != 0:
        form_l_err += '                        <div class="form-group has-error">\n'
    else:
        form_l_err += '                        <div class="form-group">\n'
    form_l_err += '                            <input type="text" name="domain" id="domain" ' \
                  'class="form-control input-lg" placeholder="Domain" required>\n'
    form_l_err += '                        </div>\n'
    if field.count('E') != 0:
        form_l_err += '                        <div class="form-group has-error">\n'
    else:
        form_l_err += '                        <div class="form-group">\n'
    form_l_err += '                            <input type="email" name="email" id="email" ' \
                  'class="form-control input-lg" placeholder="Email Address" required>\n'
    form_l_err += '                        </div>\n'
    if field.count('P') != 0:
        form_l_err += '                        <div class="form-group has-error">\n'
    else:
        form_l_err += '                        <div class="form-group">\n'
    form_l_err += '                            <input type="password" name="password" id="password" ' \
                  'class="form-control input-lg" placeholder="Password" required>\n'
    form_l_err += '                        </div>\n'
    form_l_err += '                        <span class="button-checkbox">\n'
    form_l_err += '                            <div class="checkbox">\n'
    form_l_err += '                                <label>\n'
    form_l_err += '                                  <input type="checkbox"> Remember me\n'
    form_l_err += '                                </label>\n'
    form_l_err += '                                <a href="" class="btn btn-link pull-right">Forgot Password?</a>\n'
    form_l_err += '                            </div>\n'
    form_l_err += '                        </span>\n'
    form_l_err += '                        <hr class="colorgraph">\n'
    form_l_err += '                        <div class="row">\n'
    form_l_err += '                            <div class="col-xs-6 col-sm-6 col-md-6">\n'
    form_l_err += '                                <input type="submit" class="btn btn-lg btn-success btn-block" ' \
                  'value="Sign In">\n'
    form_l_err += '                            </div>\n'
    form_l_err += '                            <div class="col-xs-6 col-sm-6 col-md-6">\n'
    form_l_err += '                                <a href="../views/register.html" ' \
                  'class="btn btn-lg btn-primary btn-block">Register</a>\n'
    form_l_err += '                            </div>\n'
    form_l_err += '                        </div>\n'

    with open('../views/form_l_err.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_l_err)


def include_form_ss(domain, nameuser, emailassoc, dtrep, alrep):
    """
    # função que cria o formulário: settings system
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_ss
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param dtrep: '2015-01-26'
    :param alrep: 'TRUE'
    :return:
    """
    form_ss = '            <form class="form-horizontal" role="form" method="post" action="../controls/usystem.py">\n'
    form_ss += '            <div class="form-group">\n'
    form_ss += '                 <label class="col-sm-4 control-label" for="dtrep">Closing date of the report</label>\n'
    form_ss += '                 <div class="col-sm-6">\n'
    form_ss += '                     <input class="form-control" id="dtrep" name="dtrep" type="text" ' \
               'value="' + str(dtrep) + '" required />\n'
    form_ss += '                 </div>\n'
    form_ss += '            </div>\n'
    form_ss += '            <div class="form-group">\n'
    form_ss += '                <label class="col-sm-4 control-label" for="alrep">' \
               'Alert users to the closing report</label>\n'
    # form_ss += '                <div class="col-sm-6">\n'
    # form_ss += '                      <input class="form-control" id="alrep" name= "alrep" ' \
    # 'type="text" value="' + alrep + '"/>\n'
    # form_ss += '                </div>\n'
    form_ss += '                <div class="col-sm-6">\n'
    form_ss += '                      <select class="form-control" id="alrep" name="alrep">\n'
    form_ss += '                      	<option selected value="' + alrep + '">' + alrep + '</option>\n'
    if alrep == 'FALSE':
        form_ss += '                      	<option value="TRUE">TRUE </option>\n'
    else:
        form_ss += '                      	<option value="FALSE">FALSE </option>\n'
    form_ss += '                      </select>\n'
    form_ss += '                </div>\n'
    form_ss += '            </div>\n'
    form_ss += '            <div class="form-group">\n'
    form_ss += '                 <div class="col-sm-6">\n'
    form_ss += '                     <input id="domain" name="domain" type="hidden" value="' + domain + '"/>\n'
    form_ss += '                     <input id="nameuser" name="nameuser" type="hidden" value="' + nameuser + '"/>\n'
    form_ss += '                     <input id="emailassoc" name="emailassoc" type="hidden" ' \
               'value="' + emailassoc + '"/>\n'
    form_ss += '                 </div>\n'
    form_ss += '            </div>\n'
    form_ss += '            <div class="form-group">\n'
    form_ss += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_ss += '                    <button type="submit" class="btn btn-primary">Update</button>\n'
    form_ss += '                </div>\n'
    form_ss += '            </div>\n'
    form_ss += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_ss)


def include_form_ss_erra(domain, nameuser, emailassoc, dtrep, alrep):
    """
    # função que cria o formulário: settings system com foco no campo alerta (validation state)
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_ss
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param dtrep: '2015-01-26'
    :param alrep: 'TRUE'
    :return:
    """
    form_ss = '            <form class="form-horizontal" role="form" method="post" action="../controls/usystem.py">\n'
    form_ss += '            <div class="form-group">\n'
    form_ss += '                 <label class="col-sm-4 control-label" for="dtrep">Closing date of the report</label>\n'
    form_ss += '                 <div class="col-sm-6">\n'
    form_ss += '                     <input class="form-control" id="dtrep" name="dtrep" type="text" ' \
               'value="' + str(dtrep) + '" required />\n'
    form_ss += '                 </div>\n'
    form_ss += '            </div>\n'
    form_ss += '            <div class="form-group has-error">\n'
    form_ss += '                <label class="col-sm-4 control-label" for="alrep">' \
               'Alert users to the closing report</label>\n'
    # form_ss += '                <div class="col-sm-6">\n'
    # form_ss += '                      <input class="form-control" id="alrep" name= "alrep" type="text" ' \
    #            'value="' + alrep + '"/>\n'
    # form_ss += '                </div>\n'
    form_ss += '                <div class="col-sm-6">\n'
    form_ss += '                      <select class="form-control" id="alrep" name="alrep">\n'
    form_ss += '                      	<option selected value="' + alrep + '">' + alrep + '</option>\n'
    if alrep == 'FALSE':
        form_ss += '                      	<option value="TRUE">TRUE </option>\n'
    else:
        form_ss += '                      	<option value="FALSE">FALSE </option>\n'
    form_ss += '                      </select>\n'
    form_ss += '                </div>\n'
    form_ss += '            </div>\n'
    form_ss += '            <div class="form-group">\n'
    form_ss += '                 <div class="col-sm-6">\n'
    form_ss += '                     <input id="domain" name="domain" type="hidden" value="' + domain + '"/>\n'
    form_ss += '                     <input id="nameuser" name="nameuser" type="hidden" value="' + nameuser + '"/>\n'
    form_ss += '                     <input id="emailassoc" name="emailassoc" type="hidden" ' \
               'value="' + emailassoc + '"/>\n'
    form_ss += '                 </div>\n'
    form_ss += '            </div>\n'
    form_ss += '            <div class="form-group">\n'
    form_ss += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_ss += '                    <button type="submit" class="btn btn-primary">Update</button>\n'
    form_ss += '                </div>\n'
    form_ss += '            </div>\n'
    form_ss += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_ss)


def include_form_ss_errd(domain, nameuser, emailassoc, dtrep, alrep):
    """
    # função que cria o formulário: settings system com foco no campo data (validation state)
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_ss
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param dtrep: '2015-01-26'
    :param alrep: 'TRUE'
    :return:
    """
    form_ss = '            <form class="form-horizontal" role="form" method="post" action="../controls/usystem.py">\n'
    form_ss += '            <div class="form-group has-error">\n'
    form_ss += '                 <label class="col-sm-4 control-label" for="dtrep">Closing date of the report</label>\n'
    form_ss += '                 <div class="col-sm-6">\n'
    form_ss += '                     <input class="form-control" id="dtrep" name="dtrep" type="text" ' \
               'value="' + str(dtrep) + '" required />\n'
    form_ss += '                 </div>\n'
    form_ss += '            </div>\n'
    form_ss += '            <div class="form-group">\n'
    form_ss += '                <label class="col-sm-4 control-label" for="alrep">' \
               'Alert users to the closing report</label>\n'
    # form_ss += '                <div class="col-sm-6">\n'
    # form_ss += '                      <input class="form-control" id="alrep" name= "alrep" type="text" ' \
    #            'value="' + alrep + '"/>\n'
    # form_ss += '                </div>\n'
    form_ss += '                <div class="col-sm-6">\n'
    form_ss += '                      <select class="form-control" id="alrep" name="alrep">\n'
    form_ss += '                      	<option selected value="' + alrep + '">' + alrep + '</option>\n'
    if alrep == 'FALSE':
        form_ss += '                      	<option value="TRUE">TRUE </option>\n'
    else:
        form_ss += '                      	<option value="FALSE">FALSE </option>\n'
    form_ss += '                      </select>\n'
    form_ss += '                </div>\n'
    form_ss += '            </div>\n'
    form_ss += '            <div class="form-group">\n'
    form_ss += '                 <div class="col-sm-6">\n'
    form_ss += '                     <input id="domain" name="domain" type="hidden" value="' + domain + '"/>\n'
    form_ss += '                     <input id="nameuser" name="nameuser" type="hidden" value="' + nameuser + '"/>\n'
    form_ss += '                     <input id="emailassoc" name="emailassoc" type="hidden" ' \
               'value="' + emailassoc + '"/>\n'
    form_ss += '                 </div>\n'
    form_ss += '            </div>\n'
    form_ss += '            <div class="form-group">\n'
    form_ss += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_ss += '                    <button type="submit" class="btn btn-primary">Update</button>\n'
    form_ss += '                </div>\n'
    form_ss += '            </div>\n'
    form_ss += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_ss)


def include_form_reg():
    """
    # função que cria o form de registro (cadastro) do associado
    # a página em si é armazenada em um arquivo separado em "views/form_r.html"
    :return:
    """
    with open('../views/form_r.html') as formf:
        form_text = formf.read()

    form_r = Template(form_text)

    return form_r.substitute()


def include_header():
    """
    # função que cria o cabeçalho da página principal (index.html)
    # esta função usa a sua única string como seu argumento para criar o cabeçalho da página HTML,
    # a página em si é armazenada em um arquivo separado em "views/header.html"
    :return:
    """
    s_js = "$(document).ready(function() {\n"
    s_js += "    $('#dt_table').dataTable( {\n"
    s_js += "            } );\n"
    s_js += "    } );\n"

    with open('../views/header.html') as headf:
        head_text = headf.read()

    header = Template(head_text)

    return header.substitute(js=s_js)


def include_header_reg():
    """
    # função que cria o cabeçalho da página de registro (cadastro) do associado
    # esta função usa a sua única string como seu argumento para criar o cabeçalho da página HTML,
    # a página em si é armazenada em um arquivo separado em "views/header_r.html"
    :return:
    """
    with open('../views/header_r.html') as headf:
        head_text = headf.read()

    header_r = Template(head_text)

    return header_r.substitute()


def include_login():
    """
    # função que cria o form de login do usuário no sistema
    # a página em si é armazenada em um arquivo separado em "views/header_l.html"
    :return:
    """
    with open('../views/header_l.html') as formf:
        form_text = formf.read()

    header_l = Template(form_text)

    return header_l.substitute()


def include_logout():
    """
    # função que efetua o logout do usuário no sistema e o redireciona para outra página
    # a página em si é armazenada em um arquivo separado em "views/logout.html"
    :return:
    """
    with open('../views/logout.html') as formf:
        form_text = formf.read()

    logout = Template(form_text)

    return logout.substitute()


def include_menu_s():
    """
    # função que cria a barra de menu/navegação (simples), sem o form de logim
    # esta função usa a sua única string como seu argumento para criar o rodapé da página HTML,
    # a página em si é armazenada em um arquivo separado em "views/menu.html"
    :return:
    """
    with open('../views/menu_s.html') as menuf:
        menu_text = menuf.read()

    menu = Template(menu_text)

    return menu.substitute()


def include_messages(s_type, s_msg):
    """
    # função que envia uma mensagem do sistema para o usuário
    # a página em si é armazenada em um arquivo separado em "views/messages.html"
    # e os elementos <$classe>, <$tipo>, <$mensagem> são substituídos quando necessário
    :param s_type: [1]=ERRO/[2]=SUCESSO/[3]=INFORMAÇÃO/[4]=ADVERTÊNCIA
    :param s_msg: "Login efetuado com sucesso, seja bem-vindo!"
    :return:
    """
    s_classe = ''
    s_desc = ''

    with open('../views/messages.html') as msgf:
        msg_text = msgf.read()

    if s_type == '1':
        s_classe = "alert alert-danger alert-dismissible"
        s_desc = 'ERROR:'
    elif s_type == '2':
        s_classe = "alert alert-success alert-dismissible"
        s_desc = 'SUCCESS:'
    elif s_type == '3':
        s_classe = "alert alert-warning alert-dismissible"
        s_desc = 'WARNING:'
    elif s_type == '4':
        s_classe = "alert alert-info alert-dismissible"
        s_desc = 'INFO:'

    msg = Template(msg_text)

    return msg.substitute(classe=s_classe, tipo=s_desc, mensagem=s_msg)


def include_pageheader(s_title, s_subtitle):
    """
    # função que cria o cabeçaho do formulário da tela de cadastro ou de pesquisa
    # a página em si é armazenada em um arquivo separado em "views/pageheader.html"
    :param s_title:
    :param s_subtitle:
    :return: header
    """
    with open('../views/pageheader.html') as pagehf:
        pageh_text = pagehf.read()

    pageheader = Template(pageh_text)

    return pageheader.substitute(title=s_title, subtitle=s_subtitle)


def include_pagination():
    """
    # função que cria os botões de paginação do formulário de pesquisa das expenses listadas na tabela
    # a página em si é armazenada em um arquivo separado em "views/pagination.html"
    :return:
    """
    with open('../views/pagination.html') as pagef:
        page_text = pagef.read()

    pagination = Template(page_text)

    return pagination.substitute()


def include_profile(s_fname, s_lname, s_domain, s_email):
    """
    # função que cria o formulário para atualização do perfil do usuário
    # a página em si é armazenada em um arquivo separado em "views/profile.html"
    :return:
    """
    with open('../views/profile.html') as prof:
        prof_text = prof.read()

    profile = Template(prof_text)

    return profile.substitute(first_name=s_fname, last_name=s_lname, domain=s_domain, email=s_email)


def include_search_form():
    """
    # função que cria o formulário de pesquisa para filtrar as expenses listadas na tabela
    # a página em si é armazenada em um arquivo separado em "views/searchform.html"
    :return:
    """
    with open('../views/searchform.html') as sformf:
        sform_text = sformf.read()

    searchform = Template(sform_text)

    return searchform.substitute()


def include_start_response(resp="text/html"):
    """
    # função que aceita uma string (opcional) como seu único argumento e a usa
    # para criar uma linha CGI "content-type" com "text/html" como padrão
    :param resp: "text/html"
    :return:Content-type:"text/html"\n\n
    """
    return 'Content-type: ' + resp + '\n\n'


def include_table():
    """
    # função que apresenta os dados (expenses) em uma tabela estática
    # a página em si é armazenada em um arquivo separado em "views/table.html" e
    :return:
    """
    with open('../views/table.html') as tablef:
        table_text = tablef.read()

    table = Template(table_text)

    return table.substitute()


def include_user(s_domain, s_user, s_email, s_date):
    """
    # função que cria a barra de menu/navegação com o nome do usuário que está acessando o sistema
    # a página em si é armazenada em um arquivo separado em "views/navbar.html"
    # e o elemento <$user> é substituído quando necessário
    :param s_user: "laercio.serra@gmail.com"
    :return: "laercio.serra@gmail.com"
    """
    with open('../views/navbar.html') as menuf:
        menu_text = menuf.read()

    navbar = Template(menu_text)

    return navbar.substitute(domain=s_domain, user=s_user, email=s_email, date=s_date)


def include_form_ca(domain, nameuser, emailassoc):
    """
    # função que cria o formulário: create new account
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_ca
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :return:
    """
    form_ca = '            <form class="form-horizontal" role="form" method="post" action="../controls/iacct.py">\n'
    form_ca += '            <div class="form-group">\n'
    form_ca += '                 <label class="col-sm-4 control-label" for="account">Account</label>\n'
    form_ca += '                 <div class="col-sm-6">\n'
    form_ca += '                    <input class="form-control" id="account" name= "account" type="text" ' \
               'value="" required />\n'
    form_ca += '                 </div>\n'
    form_ca += '            </div>\n'
    form_ca += '            <div class="form-group">\n'
    form_ca += '                 <div class="col-sm-6">\n'
    form_ca += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_ca += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_ca += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_ca += '                 </div>\n'
    form_ca += '            </div>\n'
    form_ca += '            <div class="form-group">\n'
    form_ca += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_ca += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_ca += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_ca += '                    <a class="btn btn-default" href="../controls/acct.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_ca += '                </div>\n'
    form_ca += '            </div>\n'
    form_ca += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_ca)


def include_form_ca_err(domain, nameuser, emailassoc, acct, field):
    """
    # função que cria o formulário: create new account para tratamento dos erros encontrados
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_ca
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param acct: 'Cash'
    :param field: ['A',]
    :return:
    """
    form_ca = '            <form class="form-horizontal" role="form" method="post" action="../controls/iacct.py">\n'
    if field.count('A') != 0:
        form_ca += '            <div class="form-group has-error">\n'
    else:
        form_ca += '            <div class="form-group">\n'
    form_ca += '                 <label class="col-sm-4 control-label" for="account">Account</label>\n'
    form_ca += '                 <div class="col-sm-6">\n'
    form_ca += '                    <input class="form-control" id="account" name= "account" type="text" ' \
               'value="' + acct + '" required />\n'
    form_ca += '                 </div>\n'
    form_ca += '            </div>\n'
    form_ca += '            <div class="form-group">\n'
    form_ca += '                 <div class="col-sm-6">\n'
    form_ca += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_ca += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_ca += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_ca += '                 </div>\n'
    form_ca += '            </div>\n'
    form_ca += '            <div class="form-group">\n'
    form_ca += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_ca += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_ca += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_ca += '                    <a class="btn btn-default" href="../controls/acct.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_ca += '                </div>\n'
    form_ca += '            </div>\n'
    form_ca += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_ca)


def include_form_ea(acct, id_account, domain, nameuser, emailassoc):
    """
    # função que cria o formulário: edit account
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_ea
    :param acct: 'Cash'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param id_account: '1'
    :return:
    """
    form_ea = '            <form class="form-horizontal" role="form" method="post" action="../controls/uacct.py">\n'
    form_ea += '            <div class="form-group">\n'
    form_ea += '                 <label class="col-sm-4 control-label" for="account">Account</label>\n'
    form_ea += '                 <div class="col-sm-6">\n'
    form_ea += '                    <input class="form-control" id="account" name= "account" type="text" ' \
               'value="' + acct + '" required />\n'
    form_ea += '                 </div>\n'
    form_ea += '            </div>\n'
    form_ea += '            <div class="form-group">\n'
    form_ea += '                 <div class="col-sm-6">\n'
    form_ea += '                     <input type="hidden" id="id_acct" name="id_acct" value="' + str(id_account) \
               + '"/>\n'
    form_ea += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_ea += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_ea += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_ea += '                 </div>\n'
    form_ea += '            </div>\n'
    form_ea += '            <div class="form-group">\n'
    form_ea += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_ea += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_ea += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_ea += '                    <a class="btn btn-default" href="../controls/acct.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_ea += '                </div>\n'
    form_ea += '            </div>\n'
    form_ea += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_ea)


def include_form_ea_err(acct, id_account, domain, nameuser, emailassoc, field):
    """
    # função que cria o formulário: edit account
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_ea
    :param acct: 'Cash'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param id_account: '1'
    :return:
    """
    form_ea = '            <form class="form-horizontal" role="form" method="post" action="../controls/uacct.py">\n'
    form_ea += '            <div class="form-group">\n'
    form_ea += '                 <label class="col-sm-4 control-label" for="account">Account</label>\n'
    if field.count('A') != 0:
        form_ea += '            <div class="form-group has-error">\n'
    else:
        form_ea += '            <div class="form-group">\n'
    form_ea += '                    <input class="form-control" id="account" name= "account" type="text" ' \
               'value="' + acct + '" required />\n'
    form_ea += '                 </div>\n'
    form_ea += '            </div>\n'
    form_ea += '            <div class="form-group">\n'
    form_ea += '                 <div class="col-sm-6">\n'
    form_ea += '                     <input type="hidden" id="id_acct" name="id_acct" value="' + str(id_account) \
               + '"/>\n'
    form_ea += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_ea += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_ea += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_ea += '                 </div>\n'
    form_ea += '            </div>\n'
    form_ea += '            <div class="form-group">\n'
    form_ea += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_ea += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_ea += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_ea += '                    <a class="btn btn-default" href="../controls/acct.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_ea += '                </div>\n'
    form_ea += '            </div>\n'
    form_ea += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_ea)


def include_button_create_new_cat(s_domain, s_nameuser, s_emailassoc):
    """
    # função que cria um formulário com controles ocultos para uma simples passagem de parâmetros
    # quando o botão de comando "Create New Category" for acionado
    :param s_domain: 'asparona'
    :param s_nameuser: 'Laercio Serra'
    :param s_emailassoc: 'laercio.serra@asparona.com'
    :return:
    """
    with open('../views/buttonnewcat.html') as sformb:
        sform_text = sformb.read()

    buttonform = Template(sform_text)

    return buttonform.substitute(domain=s_domain, nameuser=s_nameuser, emailassoc=s_emailassoc)


def include_dt_tb_enable_cat(domain, nameuser, emailassoc, fields, rs_dt_table):
    """
    # função que apresenta os dados em uma tabela estática com os botões de comandos (edit/delete) habilitados
    # a página em si é armazenada em um arquivo separado em "views/table.html" e
    # os elementos <$headers, $data_tb> são substituídos quando necessários
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@gmail.com'
    :param fields: {field1, field2, field3, field4, field5}
    :param rs_dt_table: {(v1, v2, v3), (v4, v5, v6), (v7, v8, v9)}
    :return: headers, data_tb
    """
    s_th = ''

    for th in fields:
        s_hd = '<th>' + th + '</th>\n'
        s_th += s_hd

    s_th += '<!--Fixed Colunm -->\n'
    s_th += '<th class="text-center">Action</th>\n'

    s_dtb = ''

    for record in rs_dt_table:
        s_td = '<tr>\n'
        for col in record:
            s_td += '   <td>' + str(col) + '</td>\n'
        s_td += '   <td class="text-center"> <!--Fixed Cells -->\n'
        s_td += '       <a href="../controls/ecat.py?d=' + domain + '&u=' + nameuser + '&e=' + emailassoc + \
                '&ce=' + record[0] + '" class="btn btn-default btn-xs">\n'
        s_td += '           <span class="glyphicon glyphicon-edit"></span> Edit\n'
        s_td += '       </a>\n'
        # s_td += '       <a href="../controls/dcat.py?d=' + domain + '&u=' + nameuser + '&e=' + emailassoc + \
        #         '&ad=' + record[0] + '" class="btn btn-default btn-xs" data-toggle="modal" data-target="#delete">\n'
        s_td += '       <a href="javascript:funcDelCat(\'' + domain + '\', \'' + nameuser + '\', \'' + emailassoc + \
                '\', \'' + record[0] + '\')" class="btn btn-default btn-xs">\n'
        s_td += '           <span class="glyphicon glyphicon-trash"></span> Delete\n'
        s_td += '       </a>\n'
        s_td += '   </td>\n'
        s_td += '</tr>\n'
        s_dtb += s_td

    with open('../views/table.html') as tablef:
        table_text = tablef.read()

    table = Template(table_text)

    return table.substitute(headers=s_th, data_tb=s_dtb)


def include_delete_cat():
    """
    # função que cria a janela modal para confirmação da exclusão de um registro.
    # a página em si é armazenada em um arquivo separado em "views/delete.html"
    :return:
    """
    with open('../views/delete_cat.html') as delf:
        del_text = delf.read()

    delete = Template(del_text)

    return delete.substitute()


def include_form_cc(domain, nameuser, emailassoc):
    """
    # função que cria o formulário: create new category
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_cc
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :return:
    """
    form_cc = '        <form class="form-horizontal" role="form" method="post" action="../controls/icat.py">\n'
    form_cc += '            <div class="form-group">\n'
    form_cc += '                 <label class="col-sm-4 control-label" for="category">Category</label>\n'
    form_cc += '                 <div class="col-sm-6">\n'
    form_cc += '                    <input class="form-control" id="category" name= "category" type="text" ' \
               'value="" required />\n'
    form_cc += '                 </div>\n'
    form_cc += '            </div>\n'
    form_cc += '            <div class="form-group">\n'
    form_cc += '                 <div class="col-sm-6">\n'
    form_cc += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_cc += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_cc += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_cc += '                 </div>\n'
    form_cc += '            </div>\n'
    form_cc += '            <div class="form-group">\n'
    form_cc += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_cc += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_cc += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_cc += '                    <a class="btn btn-default" href="../controls/cat.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_cc += '                </div>\n'
    form_cc += '            </div>\n'
    form_cc += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_cc)


def include_form_cc_err(domain, nameuser, emailassoc, cat, field):
    """
    # função que cria o formulário: create new category para tratamento dos erros encontrados
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_cc
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param cat: 'Restaurant'
    :param field: ['C',]
    :return:
    """
    form_cc = '            <form class="form-horizontal" role="form" method="post" action="../controls/icat.py">\n'
    if field.count('C') != 0:
        form_cc += '            <div class="form-group has-error">\n'
    else:
        form_cc += '            <div class="form-group">\n'
    form_cc += '                 <label class="col-sm-4 control-label" for="category">Category</label>\n'
    form_cc += '                 <div class="col-sm-6">\n'
    form_cc += '                    <input class="form-control" id="category" name= "category" type="text" ' \
               'value="' + cat + '" required />\n'
    form_cc += '                 </div>\n'
    form_cc += '            </div>\n'
    form_cc += '            <div class="form-group">\n'
    form_cc += '                 <div class="col-sm-6">\n'
    form_cc += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_cc += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_cc += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_cc += '                 </div>\n'
    form_cc += '            </div>\n'
    form_cc += '            <div class="form-group">\n'
    form_cc += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_cc += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_cc += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_cc += '                    <a class="btn btn-default" href="../controls/cat.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_cc += '                </div>\n'
    form_cc += '            </div>\n'
    form_cc += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_cc)


def include_form_ec(cat, id_category, domain, nameuser, emailassoc):
    """
    # função que cria o formulário: edit category
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_ec
    :param cat: 'Restaurant'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param id_category: '1'
    :return:
    """
    form_ec = '            <form class="form-horizontal" role="form" method="post" action="../controls/ucat.py">\n'
    form_ec += '            <div class="form-group">\n'
    form_ec += '                 <label class="col-sm-4 control-label" for="category">Category</label>\n'
    form_ec += '                 <div class="col-sm-6">\n'
    form_ec += '                    <input class="form-control" id="category" name= "category" type="text" ' \
               'value="' + cat + '" required />\n'
    form_ec += '                 </div>\n'
    form_ec += '            </div>\n'
    form_ec += '            <div class="form-group">\n'
    form_ec += '                 <div class="col-sm-6">\n'
    form_ec += '                     <input type="hidden" id="id_cat" name="id_cat" value="' + str(id_category) \
               + '"/>\n'
    form_ec += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_ec += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_ec += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_ec += '                 </div>\n'
    form_ec += '            </div>\n'
    form_ec += '            <div class="form-group">\n'
    form_ec += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_ec += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_ec += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_ec += '                    <a class="btn btn-default" href="../controls/cat.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_ec += '                </div>\n'
    form_ec += '            </div>\n'
    form_ec += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_ec)


def include_form_ec_err(cat, id_category, domain, nameuser, emailassoc, field):
    """
    # função que cria o formulário: edit category
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_ec
    :param cat: 'Restaurant'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param id_category: '1'
    :return:
    """
    form_ec = '            <form class="form-horizontal" role="form" method="post" action="../controls/ucat.py">\n'
    form_ec += '            <div class="form-group">\n'
    form_ec += '                 <label class="col-sm-4 control-label" for="category">Category</label>\n'
    if field.count('C') != 0:
        form_ec += '            <div class="form-group has-error">\n'
    else:
        form_ec += '            <div class="form-group">\n'
    form_ec += '                    <input class="form-control" id="category" name= "category" type="text" ' \
               'value="' + cat + '" required />\n'
    form_ec += '                 </div>\n'
    form_ec += '            </div>\n'
    form_ec += '            <div class="form-group">\n'
    form_ec += '                 <div class="col-sm-6">\n'
    form_ec += '                     <input type="hidden" id="id_cat" name="id_cat" value="' + str(id_category) \
               + '"/>\n'
    form_ec += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_ec += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_ec += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
               emailassoc + '"/>\n'
    form_ec += '                 </div>\n'
    form_ec += '            </div>\n'
    form_ec += '            <div class="form-group">\n'
    form_ec += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_ec += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_ec += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_ec += '                    <a class="btn btn-default" href="../controls/cat.py?d=' + domain + \
               '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_ec += '                </div>\n'
    form_ec += '            </div>\n'
    form_ec += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_ec)


def include_button_create_new_cstr(s_domain, s_nameuser, s_emailassoc):
    """
    # função que cria um formulário com controles ocultos para uma simples passagem de parâmetros
    # quando o botão de comando "Create New Customer" for acionado
    :param s_domain: 'asparona'
    :param s_nameuser: 'Laercio Serra'
    :param s_emailassoc: 'laercio.serra@asparona.com'
    :return:
    """
    with open('../views/buttonnewcstr.html') as sformb:
        sform_text = sformb.read()

    buttonform = Template(sform_text)

    return buttonform.substitute(domain=s_domain, nameuser=s_nameuser, emailassoc=s_emailassoc)


def include_dt_tb_enable_cstr(domain, nameuser, emailassoc, fields, rs_dt_table):
    """
    # função que apresenta os dados em uma tabela estática com os botões de comandos (edit/delete) habilitados
    # a página em si é armazenada em um arquivo separado em "views/table.html" e
    # os elementos <$headers, $data_tb> são substituídos quando necessários
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@gmail.com'
    :param fields: {field1, field2, field3, field4, field5}
    :param rs_dt_table: {(v1, v2, v3), (v4, v5, v6), (v7, v8, v9)}
    :return: headers, data_tb
    """
    s_th = ''

    for th in fields:
        s_hd = '<th>' + th + '</th>\n'
        s_th += s_hd

    s_th += '<!--Fixed Colunm -->\n'
    s_th += '<th class="text-center">Action</th>\n'

    s_dtb = ''

    for record in rs_dt_table:
        s_td = '<tr>\n'
        for col in record:
            s_td += '   <td>' + str(col) + '</td>\n'
        s_td += '   <td class="text-center"> <!--Fixed Cells -->\n'
        s_td += '       <a href="../controls/ecstr.py?d=' + domain + '&u=' + nameuser + '&e=' + emailassoc + \
                '&ce=' + record[0] + '" class="btn btn-default btn-xs">\n'
        s_td += '           <span class="glyphicon glyphicon-edit"></span> Edit\n'
        s_td += '       </a>\n'
        # s_td += '       <a href="../controls/dcstr.py?d=' + domain + '&u=' + nameuser + '&e=' + emailassoc + \
        #         '&ad=' + record[0] + '" class="btn btn-default btn-xs" data-toggle="modal" data-target="#delete">\n'
        s_td += '       <a href="javascript:funcDelCstr(\'' + domain + '\', \'' + nameuser + '\', \'' + emailassoc + \
                '\', \'' + record[0] + '\')" class="btn btn-default btn-xs">\n'
        s_td += '           <span class="glyphicon glyphicon-trash"></span> Delete\n'
        s_td += '       </a>\n'
        s_td += '   </td>\n'
        s_td += '</tr>\n'
        s_dtb += s_td

    with open('../views/table.html') as tablef:
        table_text = tablef.read()

    table = Template(table_text)

    return table.substitute(headers=s_th, data_tb=s_dtb)


def include_delete_cstr():
    """
    # função que cria a janela modal para confirmação da exclusão de um registro.
    # a página em si é armazenada em um arquivo separado em "views/delete.html"
    :return:
    """
    with open('../views/delete_cstr.html') as delf:
        del_text = delf.read()

    delete = Template(del_text)

    return delete.substitute()


def include_form_cstr(domain, nameuser, emailassoc):
    """
    # função que cria o formulário: create new customer
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_cstr
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :return:
    """
    form_cstr = '        <form class="form-horizontal" role="form" method="post" action="../controls/icstr.py">\n'
    form_cstr += '            <div class="form-group">\n'
    form_cstr += '                 <label class="col-sm-4 control-label" for="customer">Customer</label>\n'
    form_cstr += '                 <div class="col-sm-6">\n'
    form_cstr += '                    <input class="form-control" id="customer" name= "customer" type="text" ' \
                 'value="" required />\n'
    form_cstr += '                 </div>\n'
    form_cstr += '            </div>\n'
    form_cstr += '            <div class="form-group">\n'
    form_cstr += '                 <div class="col-sm-6">\n'
    form_cstr += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_cstr += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_cstr += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
                 emailassoc + '"/>\n'
    form_cstr += '                 </div>\n'
    form_cstr += '            </div>\n'
    form_cstr += '            <div class="form-group">\n'
    form_cstr += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_cstr += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_cstr += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_cstr += '                    <a class="btn btn-default" href="../controls/cstr.py?d=' + domain + \
                 '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_cstr += '                </div>\n'
    form_cstr += '            </div>\n'
    form_cstr += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_cstr)


def include_form_cstr_err(domain, nameuser, emailassoc, cstr, field):
    """
    # função que cria o formulário: create new customer para tratamento dos erros encontrados
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_cstr
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param cstr: 'Tivit'
    :param field: ['C',]
    :return:
    """
    form_cstr = '            <form class="form-horizontal" role="form" method="post" action="../controls/icstr.py">\n'
    if field.count('C') != 0:
        form_cstr += '            <div class="form-group has-error">\n'
    else:
        form_cstr += '            <div class="form-group">\n'
    form_cstr += '                 <label class="col-sm-4 control-label" for="customer">Customer</label>\n'
    form_cstr += '                 <div class="col-sm-6">\n'
    form_cstr += '                    <input class="form-control" id="customer" name= "customer" type="text" ' \
                 'value="' + cstr + '" required />\n'
    form_cstr += '                 </div>\n'
    form_cstr += '            </div>\n'
    form_cstr += '            <div class="form-group">\n'
    form_cstr += '                 <div class="col-sm-6">\n'
    form_cstr += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_cstr += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_cstr += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
                 emailassoc + '"/>\n'
    form_cstr += '                 </div>\n'
    form_cstr += '            </div>\n'
    form_cstr += '            <div class="form-group">\n'
    form_cstr += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_cstr += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_cstr += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_cstr += '                    <a class="btn btn-default" href="../controls/cat.py?d=' + domain + \
                 '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_cstr += '                </div>\n'
    form_cstr += '            </div>\n'
    form_cstr += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_cstr)


def include_form_ecstr(cstr, id_customer, domain, nameuser, emailassoc):
    """
    # função que cria o formulário: edit customer
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_ecstr
    :param cstr: 'Tivit'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param id_customer: '1'
    :return:
    """
    form_ecstr = '            <form class="form-horizontal" role="form" method="post" action="../controls/ucstr.py">\n'
    form_ecstr += '            <div class="form-group">\n'
    form_ecstr += '                 <label class="col-sm-4 control-label" for="customer">Customer</label>\n'
    form_ecstr += '                 <div class="col-sm-6">\n'
    form_ecstr += '                    <input class="form-control" id="customer" name= "customer" type="text" ' \
                  'value="' + cstr + '" required />\n'
    form_ecstr += '                 </div>\n'
    form_ecstr += '            </div>\n'
    form_ecstr += '            <div class="form-group">\n'
    form_ecstr += '                 <div class="col-sm-6">\n'
    form_ecstr += '                     <input type="hidden" id="id_cstr" name="id_cstr" value="' + str(id_customer) \
                  + '"/>\n'
    form_ecstr += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_ecstr += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_ecstr += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
                  emailassoc + '"/>\n'
    form_ecstr += '                 </div>\n'
    form_ecstr += '            </div>\n'
    form_ecstr += '            <div class="form-group">\n'
    form_ecstr += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_ecstr += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_ecstr += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_ecstr += '                    <a class="btn btn-default" href="../controls/cstr.py?d=' + domain + \
                  '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_ecstr += '                </div>\n'
    form_ecstr += '            </div>\n'
    form_ecstr += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_ecstr)


def include_form_ecstr_err(cstr, id_customer, domain, nameuser, emailassoc, field):
    """
    # função que cria o formulário: edit customer
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_ecstr
    :param cstr: 'Tivit'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param id_customer: '1'
    :return:
    """
    form_ecstr = '            <form class="form-horizontal" role="form" method="post" action="../controls/ucstr.py">\n'
    form_ecstr += '            <div class="form-group">\n'
    form_ecstr += '                 <label class="col-sm-4 control-label" for="customer">Customer</label>\n'
    if field.count('C') != 0:
        form_ecstr += '            <div class="form-group has-error">\n'
    else:
        form_ecstr += '            <div class="form-group">\n'
    form_ecstr += '                    <input class="form-control" id="customer" name= "customer" type="text" ' \
                  'value="' + cstr + '" required />\n'
    form_ecstr += '                 </div>\n'
    form_ecstr += '            </div>\n'
    form_ecstr += '            <div class="form-group">\n'
    form_ecstr += '                 <div class="col-sm-6">\n'
    form_ecstr += '                     <input type="hidden" id="id_cstr" name="id_cstr" value="' + str(id_customer) \
                  + '"/>\n'
    form_ecstr += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_ecstr += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_ecstr += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
                  emailassoc + '"/>\n'
    form_ecstr += '                 </div>\n'
    form_ecstr += '            </div>\n'
    form_ecstr += '            <div class="form-group">\n'
    form_ecstr += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_ecstr += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_ecstr += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_ecstr += '                    <a class="btn btn-default" href="../controls/cat.py?d=' + domain + \
                  '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_ecstr += '                </div>\n'
    form_ecstr += '            </div>\n'
    form_ecstr += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_ecstr)


def include_button_create_new_proj(s_domain, s_nameuser, s_emailassoc):
    """
    # função que cria um formulário com controles ocultos para uma simples passagem de parâmetros
    # quando o botão de comando "Create New Project" for acionado
    :param s_domain: 'asparona'
    :param s_nameuser: 'Laercio Serra'
    :param s_emailassoc: 'laercio.serra@asparona.com'
    :return:
    """
    with open('../views/buttonnewproj.html') as sformb:
        sform_text = sformb.read()

    buttonform = Template(sform_text)

    return buttonform.substitute(domain=s_domain, nameuser=s_nameuser, emailassoc=s_emailassoc)


def include_dt_tb_enable_proj(domain, nameuser, emailassoc, fields, rs_dt_table):
    """
    # função que apresenta os dados em uma tabela estática com os botões de comandos (edit/delete) habilitados
    # a página em si é armazenada em um arquivo separado em "views/table.html" e
    # os elementos <$headers, $data_tb> são substituídos quando necessários
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@gmail.com'
    :param fields: {field1, field2, field3, field4, field5}
    :param rs_dt_table: {(v1, v2, v3), (v4, v5, v6), (v7, v8, v9)}
    :return: headers, data_tb
    """
    s_th = ''

    for th in fields:
        s_hd = '<th>' + th + '</th>\n'
        s_th += s_hd

    s_th += '<!--Fixed Colunm -->\n'
    s_th += '<th class="text-center">Action</th>\n'

    s_dtb = ''

    for record in rs_dt_table:
        s_td = '<tr>\n'
        for col in record:
            s_td += '   <td>' + str(col) + '</td>\n'
        s_td += '   <td class="text-center"> <!--Fixed Cells -->\n'
        s_td += '       <a href="../controls/eproj.py?d=' + domain + '&u=' + nameuser + '&e=' + emailassoc + \
                '&pe=' + record[0] + '" class="btn btn-default btn-xs">\n'
        s_td += '           <span class="glyphicon glyphicon-edit"></span> Edit\n'
        s_td += '       </a>\n'
        # s_td += '       <a href="../controls/dproj.py?d=' + domain + '&u=' + nameuser + '&e=' + emailassoc + \
        #         '&ad=' + record[0] + '" class="btn btn-default btn-xs" data-toggle="modal" data-target="#delete">\n'
        s_td += '       <a href="javascript:funcDelProj(\'' + domain + '\', \'' + nameuser + '\', \'' + emailassoc + \
                '\', \'' + record[0] + '\')" class="btn btn-default btn-xs">\n'
        s_td += '           <span class="glyphicon glyphicon-trash"></span> Delete\n'
        s_td += '       </a>\n'
        s_td += '   </td>\n'
        s_td += '</tr>\n'
        s_dtb += s_td

    with open('../views/table.html') as tablef:
        table_text = tablef.read()

    table = Template(table_text)

    return table.substitute(headers=s_th, data_tb=s_dtb)


def include_delete_proj():
    """
    # função que cria a janela modal para confirmação da exclusão de um registro.
    # a página em si é armazenada em um arquivo separado em "views/delete.html"
    :return:
    """
    with open('../views/delete_proj.html') as delf:
        del_text = delf.read()

    delete = Template(del_text)

    return delete.substitute()


def include_form_cproj(domain, nameuser, emailassoc):
    """
    # função que cria o formulário: create new project
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_cproj
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :return:
    """
    form_cproj = '        <form class="form-horizontal" role="form" method="post" action="../controls/iproj.py">\n'
    form_cproj += '            <div class="form-group">\n'
    form_cproj += '                 <label class="col-sm-4 control-label" for="project">Project</label>\n'
    form_cproj += '                 <div class="col-sm-6">\n'
    form_cproj += '                    <input class="form-control" id="project" name= "project" type="text" ' \
                  'value="" required />\n'
    form_cproj += '                 </div>\n'
    form_cproj += '            </div>\n'
    form_cproj += '            <div class="form-group">\n'
    form_cproj += '                 <div class="col-sm-6">\n'
    form_cproj += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_cproj += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_cproj += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
                  emailassoc + '"/>\n'
    form_cproj += '                 </div>\n'
    form_cproj += '            </div>\n'
    form_cproj += '            <div class="form-group">\n'
    form_cproj += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_cproj += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_cproj += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_cproj += '                    <a class="btn btn-default" href="../controls/proj.py?d=' + domain + \
                  '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_cproj += '                </div>\n'
    form_cproj += '            </div>\n'
    form_cproj += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_cproj)


def include_form_cproj_err(domain, nameuser, emailassoc, proj, field):
    """
    # função que cria o formulário: create new project para tratamento dos erros encontrados
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_proj
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param proj: 'Tivit BIRH'
    :param field: ['P',]
    :return:
    """
    form_proj = '            <form class="form-horizontal" role="form" method="post" action="../controls/iproj.py">\n'
    if field.count('P') != 0:
        form_proj += '            <div class="form-group has-error">\n'
    else:
        form_proj += '            <div class="form-group">\n'
    form_proj += '                 <label class="col-sm-4 control-label" for="project">Project</label>\n'
    form_proj += '                 <div class="col-sm-6">\n'
    form_proj += '                    <input class="form-control" id="project" name= "project" type="text" ' \
                 'value="' + proj + '" required />\n'
    form_proj += '                 </div>\n'
    form_proj += '            </div>\n'
    form_proj += '            <div class="form-group">\n'
    form_proj += '                 <div class="col-sm-6">\n'
    form_proj += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_proj += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_proj += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
                 emailassoc + '"/>\n'
    form_proj += '                 </div>\n'
    form_proj += '            </div>\n'
    form_proj += '            <div class="form-group">\n'
    form_proj += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_proj += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_proj += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_proj += '                    <a class="btn btn-default" href="../controls/proj.py?d=' + domain + \
                 '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_proj += '                </div>\n'
    form_proj += '            </div>\n'
    form_proj += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_proj)


def include_form_eproj(proj, id_project, domain, nameuser, emailassoc):
    """
    # função que cria o formulário: edit project
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_eproj
    :param proj: 'Tivit BIRH'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param id_project: '1'
    :return:
    """
    form_eproj = '            <form class="form-horizontal" role="form" method="post" action="../controls/uproj.py">\n'
    form_eproj += '            <div class="form-group">\n'
    form_eproj += '                 <label class="col-sm-4 control-label" for="project">Project</label>\n'
    form_eproj += '                 <div class="col-sm-6">\n'
    form_eproj += '                    <input class="form-control" id="project" name= "project" type="text" ' \
                  'value="' + proj + '" required />\n'
    form_eproj += '                 </div>\n'
    form_eproj += '            </div>\n'
    form_eproj += '            <div class="form-group">\n'
    form_eproj += '                 <div class="col-sm-6">\n'
    form_eproj += '                     <input type="hidden" id="id_proj" name="id_proj" value="' + str(id_project) \
                  + '"/>\n'
    form_eproj += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_eproj += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_eproj += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
                  emailassoc + '"/>\n'
    form_eproj += '                 </div>\n'
    form_eproj += '            </div>\n'
    form_eproj += '            <div class="form-group">\n'
    form_eproj += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_eproj += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_eproj += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_eproj += '                    <a class="btn btn-default" href="../controls/proj.py?d=' + domain + \
                  '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_eproj += '                </div>\n'
    form_eproj += '            </div>\n'
    form_eproj += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_eproj)


def include_form_eproj_err(proj, id_project, domain, nameuser, emailassoc, field):
    """
    # função que cria o formulário: edit project
    # a página em si é armazenada em um arquivo separado em "views/form.html" e o
    # elemento $form é substituído quando necessário por form_eproj
    :param proj: 'Tivit'
    :param domain: 'asparona'
    :param nameuser: 'Laercio Serra'
    :param emailassoc: 'laercio.serra@asparona.com'
    :param id_project: '1'
    :return:
    """
    form_eproj = '            <form class="form-horizontal" role="form" method="post" action="../controls/uproj.py">\n'
    form_eproj += '            <div class="form-group">\n'
    form_eproj += '                 <label class="col-sm-4 control-label" for="project">Project</label>\n'
    if field.count('P') != 0:
        form_eproj += '            <div class="form-group has-error">\n'
    else:
        form_eproj += '            <div class="form-group">\n'
    form_eproj += '                    <input class="form-control" id="project" name= "project" type="text" ' \
                  'value="' + proj + '" required />\n'
    form_eproj += '                 </div>\n'
    form_eproj += '            </div>\n'
    form_eproj += '            <div class="form-group">\n'
    form_eproj += '                 <div class="col-sm-6">\n'
    form_eproj += '                     <input type="hidden" id="id_proj" name="id_proj" value="' + str(id_project) \
                  + '"/>\n'
    form_eproj += '                     <input type="hidden" id="domain" name="domain" value="' + domain + '"/>\n'
    form_eproj += '                     <input type="hidden" id="nameuser" name="nameuser" value="' + nameuser + '"/>\n'
    form_eproj += '                     <input type="hidden" id="emailassoc" name="emailassoc" value="' + \
                  emailassoc + '"/>\n'
    form_eproj += '                 </div>\n'
    form_eproj += '            </div>\n'
    form_eproj += '            <div class="form-group">\n'
    form_eproj += '                <div class="col-sm-offset-4 col-sm-6">\n'
    form_eproj += '                    <input type="submit" name="save" value="Save" class="btn btn-primary">\n'
    form_eproj += '                    <input type="reset" name="reset" value="Reset" class="btn btn-default">\n'
    form_eproj += '                    <a class="btn btn-default" href="../controls/proj.py?d=' + domain + \
                  '&u=' + nameuser + '&e=' + emailassoc + '" role="button">Cancel</a>\n'
    form_eproj += '                </div>\n'
    form_eproj += '            </div>\n'
    form_eproj += '        </form>\n'

    with open('../views/form.html') as formf:
        form_text = formf.read()

    form = Template(form_text)

    return form.substitute(form=form_eproj)