# coding=utf-8
from shop.models import Domain

import logging
logger = logging.getLogger('icetusshop.shop')

def get_site(request):
	host = get_host(request)
	site = None
	try:
		domain = Domain.objects.get(domain=host)
		if domain:
			site = domain.site
	except Exception as err:
		logger.error('Site not defined. [%s] ' % err)
	return site

def get_host(request):
	return request.get_host()
	
def get_path(request,is_need_para = True):
	if is_need_para:
		return request.get_full_path()
	else:
		return request.get_path()
