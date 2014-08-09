#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Created on 28/07/2013

@author: Samsung
"""
# import urllib
# import urllib2

# query_args = { 'q':'query string', 'foo':'bar' } # you have to pass in a dictionary
#
# encoded_args = urllib.urlencode(query_args)
#
# print 'Encoded:', encoded_args

# s_url = 'http://python.org/?' + encoded_args
# s_url = 'http://localhost/cycleclub/views/regras.html'
# print s_url

# def include_redir_page(s_url):
#     print urllib2.urlopen(s_url).read()
#
# include_redir_page(s_url)
#
# formulario = cgi.FieldStorage()

# Verifica se o campo foi preenchido
# if formulario.has_key("nome"):
#   print "O campo foi preenchido"
# else:
#   print "O campo não foi preenchido"

# print urllib2.urlopen(s_url)

# req = urllib2.Request(s_url)

# try:
#     print urllib2.urlopen(req).read()
#
# except urllib2.URLError, e:
#     print e.code
#     print e.read()

# import re

# address = 'calchp12c@gmail.com'
# address = 'laercio.serra@gmail.com'
# address = 'lsinform@netfly.com.br'
# address = "-@-"

# def email_validate_re(address):
#     """ from http://www.regular-expressions.info/email.html """
#     pattern = r"\b[a-zA-Z0-9._%+-]*[a-zA-Z0-9_%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b"
#     if re.match(pattern, address):
#         print 'OK'
#     else:
#         print 'NOK'
#
# email_validate_re(address)