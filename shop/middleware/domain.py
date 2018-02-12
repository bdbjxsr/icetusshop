# coding=utf-8
import logging
from django.shortcuts import redirect
from shop.functions import url_helper
logger = logging.getLogger('icetusshop.shop')

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class DomainMiddleware(MiddlewareMixin):
	def process_request(self, request):
		#logger.debug('Deal Domain Info Request Start ...')
		logger.info('The Domain is : %s' % url_helper.get_host(request))
		site = url_helper.get_site(request)
		if site:
			request.site = site
		else:
			# 站点未定义，则跳转到官网
			return redirect('http://www.icetus.com')
		
		#logger.debug('Deal Domain Info Request End   ...')
		


	def process_template_response(self, request, response):
		#logger.debug('Deal Domain Info Template Response Start ...')
		
		siteinfo = {}
		siteinfo['static_base'] = '/static/%s' % (request.site.get_template())
		siteinfo['name'] = request.site.name
		response.context_data['siteinfo'] = siteinfo
		
		#logger.debug('Deal Domain Info Template Response End   ...')
		return response
