#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

"""
Created on 14/06/2014
@author: Laércio Serra (laercio.serra@gmail.com)
"""
# Declaração das variáveis globais que serão usadas pelo aplicativo enquanto a sua sessão estiver ativa

class sistema:
        s_domain = None
        s_user = None
        s_email = None
        s_senha = None


        def __init__(self, s_domain, s_user, s_email, s_senha):
            self.domain = s_domain
            self.user = s_user,
            self.email = s_email
            self.senha = s_senha


        def get_domain(self):
            return self.domain


        def get_user(self):
            return self.user


        def get_email(self):
            return self.email


        def get_senha(self):
            return self.senha