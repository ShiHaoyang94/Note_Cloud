from django.db import models

# Create your models here.
class User(models.Model):

    username = models.CharField('用户名',max_length=30,unique=True)

    password = models.CharField('密码',max_length=32)

    email = models.EmailField('邮箱',default='NULL')

    creatd_time = models.DateTimeField('创建时间',auto_now_add=True)

    updated_time = models.DateTimeField('更新时间', auto_now=True)

    is_active = models.BooleanField('是否活跃',default=True)

    def __str__(self):
        return '%s %s %s %s'%(self.username,self.creatd_time,self.updated_time,self.is_active)


