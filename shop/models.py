from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.encoding import python_2_unicode_compatible

import logging
logger = logging.getLogger('icetusshop.shop')

class MyUserManager(BaseUserManager):
	def _create_user(self, username, email, password, **extra_fields):
		"""
		Creates and saves a User with the given username, email and password.
		"""

		# if not username:
		#	 raise ValueError('The given username must be set')
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		return self._create_user(username, email, password, **extra_fields)

	def create_superuser(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True')

		return self._create_user(username, email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=254, unique=True, null=True, db_index=True)
	email = models.EmailField('email address', unique=True, db_index=True, max_length=254)
	first_name = models.CharField(max_length=254, null=True)
	middle_name = models.CharField(max_length=254, null=True)
	last_name = models.CharField(max_length=254, null=True)
	mobile_phone = models.CharField(max_length=50, null=True)
	gender = models.CharField(max_length=3, null=True)
	birthday = models.DateField(null=True)
	is_staff = models.BooleanField('staff status', default=False)
	is_active = models.BooleanField('active', default=True)
	reg_ip = models.CharField(max_length=32, null=True, blank=True, verbose_name='注册IP地址')
	last_ip = models.CharField(max_length=32, null=True, blank=True, verbose_name='最后登陆IP地址')

	create_time = models.DateTimeField(auto_now_add=True, null=True)
	update_time = models.DateTimeField(auto_now=True, null=True)

	USERNAME_FIELD = 'email'

	objects = MyUserManager()

	class Meta:
		db_table = 'myuser'

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return str(self.first_name) + ' ' + str(self.last_name)

	def get_human_gender(self):
		if self.gender == '1':
			return 'male'
		elif self.gender == '0':
			return 'female'
		else:
			return 'unknow'

			
			
@python_2_unicode_compatible
class Site(models.Model):			
	name = models.CharField(max_length=254, unique=True, null=True, db_index=True , verbose_name='站点名称')
	manager = models.ForeignKey(MyUser, default=None, related_name='sites', verbose_name='关联的用户')
	operators = models.ManyToManyField(MyUser, null=True, blank=True, related_name='opratoe_sites',verbose_name='操作员')
	create_time = models.DateTimeField(auto_now_add=True, null=True)
	update_time = models.DateTimeField(auto_now=True, null=True)
	
	def __str__(self):
		return self.name

	#return 'client/1/pages/demo/index.html'
	def get_template(self,pagename='',type='client',is_end_with_slash=False):
		logger.info('Start to find template : [site:%s] [pagename:%s] [type:%s]' % (self,pagename,type))

		template = ''
		if type.lower() == 'client':
			template = 'client/defalut/pages/%s' % pagename
		elif type.lower() == 'admin':
			template = 'admin/defalut/%s' % pagename
		elif type.lower() == 'email':
			template = 'client/defalut/emails/%s' % pagename
		else:
			raise Http404
		
		from shop.functions import string_util
			
		try:
			template_name = SiteConfig.objects.filter(site=self).filter(name='template_name')
			if template_name.count() > 0:
				template_name = template_name[0].val
			
			if type.lower() == 'client':
				template = 'client/%s/pages/%s/%s' % (self.id,template_name,pagename)
			elif type.lower() == 'admin':
				template =  'admin/%s/%s' % (template_name,pagename)
			elif type.lower() == 'email':
				template = 'client/%s/emails/%s/%s' % (self.id,template_name,pagename)
			else:
				raise Http404
							
		except Exception as err:
			logger.error('Site [%s] template [%s] not defined. Error Message: %s ' % (self,type,err))

		template = string_util.path_end_with_slash(template,is_end_with_slash)
		return template
		
		
	class Meta:
		verbose_name = '站点信息'
		verbose_name_plural = '站点信息'
	

@python_2_unicode_compatible	
class Domain(models.Model):
	domain = models.CharField(max_length=254, unique=True, null=True, db_index=True , verbose_name='域名')
	site = models.ForeignKey(Site, default=None, related_name='domains', verbose_name='关联的站点')
	
	create_time = models.DateTimeField(auto_now_add=True, null=True)
	update_time = models.DateTimeField(auto_now=True, null=True)
	
	def __str__(self):
		return self.domain

	class Meta:
		verbose_name = '域名信息'
		verbose_name_plural = '域名信息'
		
		
@python_2_unicode_compatible
class SiteConfig(models.Model):
	site = models.ForeignKey(Site, default=None, related_name='configs', verbose_name='关联的站点')
	name = models.CharField(max_length=100, verbose_name='参数名称')
	val = models.CharField(max_length=254, verbose_name='参数值')
	create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	def __str__(self):
		return '%s:%s' % (self.site,self.name)

	class Meta:
		verbose_name = '各站点参数'
		verbose_name_plural = '各站点参数'
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
			