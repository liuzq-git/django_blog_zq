from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from article.models import ArticlePost


class Comment(MPTTModel):
    article=models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # body=models.TextField()
    body = RichTextField()
    created=models.DateTimeField(auto_now_add=True)
    parent=TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    reply_to=models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )
    # class Meta:
    #     ordering = ('created',)
    class MPTTMeta:
        order_insertion_by=['created']
    def __str__(self):
        return self.body[:20]

    def get_absolute_url(self):
        return reverse('article:article_detail',args=[self.id])

