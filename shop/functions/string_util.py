# coding=utf-8

import logging
logger = logging.getLogger('icetusshop.shop')

# 去掉路径最后的‘/’
def path_end_with_slash(path,is_need):
	if is_need:
		if not path.endswith('/'):
			path = path + '/'
	else:
		if path.endswith('/'):
			path = path[:-1]
			
	return path
