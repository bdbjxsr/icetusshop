from django import template
register = template.Library()

import logging
logger = logging.getLogger('icetusshop.shop')

@register.simple_tag
def mystatic(parser):
	parser = parser.replace('{{template_base}}' , '/static/client/1/pages/demo')
	return parser