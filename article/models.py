
# Create your models here.
from PIL import Image
from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
# from imagekit.models import ProcessedImageField


class ArticleColumn(models.Model):
    title=models.CharField(max_length=100,blank=True)
    created=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title


# 博客文章数据模型
class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags=TaggableManager(blank=True)
    column=models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()

    #PositiveIntegerField是用于存储正整数的字段
    total_views=models.PositiveIntegerField(default=0)

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)
    avatar=models.ImageField(upload_to='article/%Y%m%d/',blank=True)
    likes=models.PositiveIntegerField(default=0)
    class Meta:
        ordering=('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail',args=[self.id])
    #save()是model内置的方法，它会在model实例每次保存时调用。
    # 这里改写它，将处理图片的逻辑“塞进去”
    def save(self,*args,**kwargs):
        #调用父类中原有的save()方法，即将model中的字段数据保存到数据库中。
        article=super(ArticlePost, self).save(*args,**kwargs)
        #剔除掉没有标题图的文章，这些文章不需要处理图片。
        #为了排除掉统计浏览量调用的save()，免得每次用户进入文章详情页面都要处理标题图，太影响性能
        if self.avatar and not kwargs.get('update_field'):
            image=Image.open(self.avatar)
            (x,y)=image.size
            new_x=400
            new_y=int(new_x*(y/x))
            #Image.ANTIALIAS表示缩放采用平滑滤波
            resized_image=image.resize((new_x,new_y),Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article

    def was_created_recently(self):
        diff=timezone.now()-self.created
        if diff.days==0 and diff.seconds<60 and diff.seconds>=0:
            return True
        else:
            return False