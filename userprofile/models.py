from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):  #每个Profile模型对应唯一的一个User模型，形成了对User的外接扩展
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    phone=models.CharField(max_length=20,blank=True)
    #upload_to指定了图片上传的位置，即/media/avatar/%Y%m%d/。%Y%m%d是日期格式化的写法，
    # 会最终格式化为系统时间。比如说图片上传是2018年12月5日，则图片会保存在/media/avatar/2018205/中
    avatar=models.ImageField(upload_to='avatar/%Y%m%d/',blank=True)
    bio=models.TextField(max_length=500,blank=True)
    def __str__(self):
        return 'user {}'.format(self.user.username)

# @receiver(post_save,sender=User)  #post_save就是一个内置信号，它可以在模型调用save()方法后发出信号
# def creare_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save,sender=User)
# def save_user_profile(sender,instance,**kwarge):
#     instance.profile.save()