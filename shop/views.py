# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse

from shop.functions import config_helper

import logging
logger = logging.getLogger('icetusshop.shop')

def view_index(request):
	ctx = {}

	return TemplateResponse(request, request.site.get_template(pagename = 'index.html'), ctx)