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
				template =	'admin/%s/%s' % (template_name,pagename)
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
	
	
@python_2_unicode_compatible
class Category(models.Model):
	site = models.ForeignKey(Site, default=None, related_name='categorys', verbose_name='关联的站点')
	
	code = models.CharField(max_length=100, default='', db_index=True, unique=True, verbose_name='分类代码')
	name = models.CharField(max_length=100, default='', verbose_name='分类名称')
	page_title = models.CharField(max_length=100, blank=True, default='', verbose_name='网页标题')
	keywords = models.CharField(max_length=254, default='', blank=True, verbose_name='关键字')
	short_desc = models.CharField(max_length=1024, default='', blank=True, verbose_name='简略描述')
	description = models.CharField(max_length=1024, default='', blank=True, verbose_name='分类描述')
	sort_order = models.CharField(max_length=100, default='', verbose_name='排序序号')
	parent = models.ForeignKey('self', null=True, default=None, related_name='childrens', blank=True,
							   verbose_name='上级分类')
	detail_template = models.CharField(max_length=254, default='', blank=True, verbose_name='商品详情页指定模板')
	category_template = models.CharField(max_length=254, default='', blank=True, verbose_name='分类指定模板')
	static_file_name = models.CharField(max_length=254, db_index=True, unique=True, null=True, blank=True,
										verbose_name='静态文件名(不包含路径，以html结尾)')
	create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	def get_parent_stack(self):
		from shopcart.utils import Stack
		s = Stack(20);
		target = self
		while target is not None:
			s.push(target)
			target = target.parent
		return s

	def get_dirs(self):
		from shopcart.utils import Stack
		s = self.get_parent_stack()
		dir = ''
		while not s.isempty():
			dir = dir + s.pop().code + '/'
		return dir

	def get_childrens(self):
		return self.childrens.all().order_by('-sort_order')

	def get_url(self):
		from shopcart.functions.product_util_func import get_url
		return get_url(self)

	def get_leveled_parents(self):
		from shopcart.utils import Stack
		s = self.get_parent_stack()
		parent_list = []
		while not s.isempty():
			parent_list.append(s.pop())
		return parent_list

	def get_parent(cat):
		if cat.parent:
			return get_parent(cat.parent)
		else:
			return cat

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '商品分类'
		verbose_name_plural = '商品分类'
	
	
@python_2_unicode_compatible
class Product(models.Model):
	site = models.ForeignKey(Site, default=None, related_name='products', verbose_name='关联的站点')
	
	item_number = models.CharField(max_length=100, default='', db_index=True, blank=True, verbose_name='商品编号')
	name = models.CharField(max_length=100, default='', db_index=True, verbose_name='商品名称')
	type = models.CharField(max_length=20, default='B2B+B2C', verbose_name='商品类型')
	click_count = models.IntegerField(default=0, verbose_name='浏览次数')
	quantity = models.IntegerField(default=0, verbose_name='库存数量')
	warn_quantity = models.IntegerField(default=0, verbose_name='预警库存')
	price = models.FloatField(default=0.0, verbose_name='基准价格')
	market_price = models.FloatField(default=0.0, verbose_name='市场价')
	page_title = models.CharField(max_length=100, blank=True, default='', verbose_name='网页标题')
	keywords = models.CharField(max_length=254, default='', blank=True, verbose_name='关键字')
	short_desc = models.CharField(max_length=1024, default='', blank=True, verbose_name='简略描述')
	seo_desc = models.CharField(max_length=1024, default='', blank=True, verbose_name='SEO描述')
	description = models.TextField(blank=True, verbose_name='详细描述')
	youtube = models.CharField(max_length=1024, default='', blank=True, verbose_name='youtube视频地址')
	is_free_shipping = models.BooleanField(default=False, verbose_name='是否包邮')
	sort_order = models.IntegerField(default=0, verbose_name='排序序号')
	static_file_name = models.CharField(max_length=254, default=None, null=True, db_index=True, blank=True,
										verbose_name='静态文件名(不包含路径，以html结尾)')
	categorys = models.ManyToManyField(Category, verbose_name='商品分类', related_name="products")
	min_order_quantity = models.IntegerField(default=0, verbose_name='最小下单数量')
	is_publish = models.BooleanField(default=False, verbose_name='上架')
	detail_template = models.CharField(max_length=254, default='', blank=True, verbose_name='详情页指定模板')
	related_products = models.ManyToManyField('self', null=True, blank=True, related_name='parent_product',
											  verbose_name='关联商品')
	weight = models.FloatField(default=0.0, verbose_name='重量，克')
	cuboid_long = models.FloatField(default=0.0, verbose_name='体积_长_毫米')
	cuboid_width = models.FloatField(default=0.0, verbose_name='体积_宽_毫米')
	cuboid_height = models.FloatField(default=0.0, verbose_name='体积_高_毫米')

	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)

	def get_related_products(self):
		return self.related_products.all()

	def get_one_category(self):
		list = self.categorys.all()
		if len(list) > 0:
			return list[0]
		else:
			return None

	def get_main_image(self):
		return self.get_images(method='single')

	def get_main_image_list(self):
		return self.get_images(method='main')

	def get_main_image_list_attachment(self):
		image_list = Album.objects.filter(item_type='attachment', item_id=self.id)
		image_list = list(image_list)
		logger.debug("获取到的list:%s" % image_list)
		return image_list

	def get_main_image_list_attachment_pdf(self):
		image_list = Album.objects.filter(item_type='attachment', item_id=self.id)
		image_list = list(image_list)
		new_images_list = []
		# 允许上传的类型
		file_allow = ['PDF']
		logger.debug("获取到的list:%s" % image_list)
		for img in image_list:
			ext = img.image.split('.')[-1]
			logger.debug(str(ext))
			if ext.upper() not in file_allow:
				logger.info(image_list)
			else:
				new_images_list.append(img)
				logger.info(img.image)
		return new_images_list

	def get_main_image_list_attachment_rar(self):
		image_list = Album.objects.filter(item_type='attachment', item_id=self.id)
		image_list = list(image_list)
		new_images_list = []
		# 允许上传的类型
		file_allow = ['RAR', 'ZIP']
		logger.debug("获取到的list:%s" % image_list)
		for img in image_list:
			ext = img.image.split('.')[-1]
			logger.debug(str(ext))
			if ext.upper() not in file_allow:
				logger.info(image_list)
			else:
				new_images_list.append(img)
				logger.info(img.image)
		return new_images_list

	def get_all_image_list(self):
		return self.get_images(method='all')

	def get_images(self, method, sort_by='sort_order'):
		image_list = self.images.all()
		if method == 'main':
			image_list = image_list.filter(is_show_in_product_detail=True)

		if sort_by == 'sort_order':
			image_list = sorted(image_list, key=lambda image: image.sort, reverse=True)
		elif sort_by == 'create_time':
			image_list = sorted(image_list, key=lambda image: image.create_time, reverse=True)

		main_image_url = self.image
		main_image = None
		for img in image_list:
			if img.image == main_image_url:
				logger.debug('Find the main image. Remove it to top.')
				main_image = img
				break

		# logger.debug('main_img:%s	  alt:%s' % (main_image,main_image.alt_value))

		if main_image:
			image_list.remove(main_image)
			image_list.insert(0, main_image)

		if method == 'single':
			if len(image_list) > 0:
				return image_list[0]
			else:
				return None
		else:
			return image_list

	def get_attributes(self):
		pa_list = self.attributes.all()
		attribute_list = Attribute.objects.filter(product_attribute__in=pa_list).distinct()
		attribute_group_list = list(set([attr.group for attr in attribute_list]))  # 用set去重后，再转回list
		attribute_group_list.sort(key=lambda x: x.position)	 # 利用position字段排序

		for ag in attribute_group_list:
			ag.attr_list = [attr for attr in attribute_list if attr.group == ag]
			ag.attr_list.sort(key=lambda x: x.position)

		return attribute_group_list

	def get_product_detail_images(self):
		return self.images.filter(is_show_in_product_detail=True).order_by('sort')

	def get_url(self):
		from shopcart.functions.product_util_func import get_url
		return get_url(self)

	def get_stere(self, unit=None):
		stere_cm = self.cuboid_long * self.cuboid_width * self.cuboid_height
		if unit == None or unit == 'm':
			# 换算成立方米
			return stere_cm / (1000 * 1000 * 1000)
		else:
			return stere_cm

	def get_weight(self, unit=None):
		if unit == None or unit == 'kg':
			# 换算成千克
			return self.weight / 1000
		else:
			return self.weight

	def get_min_price(self):
		return self.get_price_for_show('min')

	def get_max_price(self):
		return self.get_price_for_show('max')

	def get_price(self):
		return self.get_price_for_show('min-max')

	def has_price_range(self):
		if self.get_max_price() - self.get_min_price() > 0.01:
			return True
		else:
			return False

	def get_price_for_show(self, method='min'):
		price_min = 0.0
		price_max = 0.0
		price_list = []

		if self.prices.all().count() > 0:
			for p in self.prices.all():
				if p.price > 0:
					price_list.append(p.price)

			if len(price_list) > 0:
				price_min = min(price_list)
				price_max = max(price_list)
			else:
				price_min = self.price
				price_max = self.price
		else:
			price_min = self.price
			price_max = self.price

		if method == 'min':
			return price_min
		elif method == 'max':
			return price_max
		elif method == 'min-max':
			if price_max - price_min > 0.01:
				return '%s - %s' % (price_min, price_max)
			else:
				return price_max
		else:
			return price_min

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '商品'
		verbose_name_plural = '商品'	
	

@python_2_unicode_compatible
class Product_Images(models.Model):
    product = models.ForeignKey(Product, default=None, related_name='images', verbose_name='关联的商品')
    is_show_in_product_detail = models.BooleanField(default=False, verbose_name='是否在商品详情中展示')
    sort = models.IntegerField(default=0, verbose_name='排序序号')
    alt_value = models.CharField(max_length=100, default='', verbose_name='Alt值')
    file_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='文件名')
    thumb_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='文件名')
    path = models.CharField(max_length=254, null=True, blank=True, verbose_name='文件路径')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def get_image_url(self):
        return self.get_picture_url('image')

    def get_thumb_url(self):
        return self.get_picture_url('thumb')

    def get_picture_url(self, method='image'):
        # 整理路径，如果有\则替换为/
        if method == 'image':
            filename = self.file_name
        else:
            filename = self.thumb_name

        if not filename:
            if method == 'image':
                return self.image
            else:
                return self.thumb

        else:
            path = self.path.replace('\\', '/')
            if not path.endswith('/'):
                path = path + '/'
            base_url = System_Config.objects.get(name='base_url').val
            if not base_url.endswith('/'):
                base_url = base_url + "/"
            return base_url + path + filename

    def __str__(self):
        return str(self.id) + ' ' + self.thumb

    class Meta:
        verbose_name = '商品相册'
        verbose_name_plural = '商品相册'
	
	
	
	
	
	
	
	
	
	
			