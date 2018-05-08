from django.db import models

# Create your models here.
class Passport(models.Model):
    '''用户模型类'''
    username = models.CharField(max_length=20, verbose_name='用户名称')
    password = models.CharField(max_length=40, verbose_name='用户密码')
    email = models.EmailField(verbose_name='用户邮箱')
    is_active = models.BooleanField(default=False, verbose_name='激活状态')
    
    # 如果已经有数据库了，不需要迁移数据库和脚本，查询数据的时候，没有model也可以查询，但是在api页面post的数据，显示的是此模型中的数据的内容
    # 建立的模型需要与原来的数据库的模型的字段相对应，在post数据的时候，否则报错！！！！！！！！！！！！！！！！！！
    is_del = models.BooleanField(default=False, verbose_name='删除标记')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 's_user_account'


class Address(models.Model):
    '''地址模型类'''
    recipient_name = models.CharField(max_length=20, verbose_name='收件人')
    recipient_addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, verbose_name='邮政编码')
    recipient_phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    passport = models.ForeignKey('Passport', verbose_name='账户', on_delete=models.CASCADE)

    class Meta:
        db_table = 's_user_address'
