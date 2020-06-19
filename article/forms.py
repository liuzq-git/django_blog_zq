from django import forms

from .models import ArticlePost


class ArticlePostForm(forms.ModelForm):  #ArticlePostForm类继承了Django的表单类forms.ModelForm，
    class Meta:                          #并在类中定义了内部类class Meta，指明了数据模型的来源，以及表单中应该包含数据模型的哪些字段
        model=ArticlePost
        fields=('title','body','tags','avatar')