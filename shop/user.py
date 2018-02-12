# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib import auth

from shop.functions import config_helper

import logging
logger = logging.getLogger('icetusshop.shop')

def login(request):
	ctx = {}
	ctx['page_name'] = 'Login'

	if request.method == 'GET':
		if 'next' in request.GET:
			ctx['next'] = request.GET['next']
		return TemplateResponse(request,request.site.get_template('login.html'),ctx)
	else:	
		ctx.update(csrf(request))
		if 'next' in request.POST:
			next = request.POST['next']
			ctx['next'] = next
			
		user = auth.authenticate(username = request.POST['email'].lower(), password = request.POST['password'])
		return redirect('/')
