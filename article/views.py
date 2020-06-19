import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View
from django.views.generic import DetailView

from comment.forms import CommentForm
from comment.models import Comment
from .forms import ArticlePostForm
from .models import ArticlePost, ArticleColumn


def article_list(request):

    search=request.GET.get('search')
    order=request.GET.get('order')
    column=request.GET.get('column')
    tag=request.GET.get('tag')
    article_list=ArticlePost.objects.all()
    if search:
        article_list=article_list.filter(
            Q(title__icontains=search)|Q(body__icontains=search)
        )
        if order=='total_views':
            article_list=ArticlePost.objects.filter(
                Q(title__icontains=search)|Q(body__icontains=search)
            ).order_by('-total_views')
        else:  #icontains是不区分大小写的包含
            article_list=ArticlePost.objects.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
    else:
        search=''
        if order=='total_views':
            article_list=ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list=ArticlePost.objects.all()

    if tag and tag!='None':
        article_list=article_list.filter(tags__name__in=[tag])
    if column is not None and column.isdigit():
        article_list=article_list.filter(column=column)
    if order=='total_views':
        article_list = article_list.order_by('-total_views')
    paginator=Paginator(article_list,3)
    page=request.GET.get('page')
    articles=paginator.get_page(page)
    context={'articles':articles,
             'order':order,
             'search':search,
             'column':column,
             'tag':tag,
             }  #定义了需要传递给模板的上下文，这里即articles
    print(articles)
    return render(request,'article/list.html',context) #render函数:把context的内容，加载进模板，并通过浏览器呈现
    # return HttpResponse('Hello World!')

def article_detail(request,id):
    # article = ArticlePost.objects.get(id=id) #在所有文章中，取出id值相符合的唯一的一篇文章
    article = get_object_or_404(ArticlePost,id=id) #在所有文章中，取出id值相符合的唯一的一篇文章
    article.total_views+=1
    article.save(update_fields=['total_views'])  #update_fields=[]指定了数据库只更新total_views字段
    comments=Comment.objects.filter(article=id)
    comment_form=CommentForm()
    md=markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    article.body=md.convert(article.body)
    # print('article')
    # print(article)
    # print('comments')
    # print(comments)
    context = {'article': article, 'toc': md.toc,'comments':comments,'comment_form':comment_form}  # 定义了需要传递给模板的上下文，这里即articles
    return render(request, 'article/detail.html', context)  # render函数:把context的内容，加载进模板，并通过浏览器呈现

@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method=="POST":
        article_post_form=ArticlePostForm(request.POST,request.FILES)
        if article_post_form.is_valid():   #判断提交的数据是否满足模型的要求。
            new_article=article_post_form.save(commit=False) #保存表单中的数据（但是commit=False暂时不提交到数据库，因为author还未指定）
            new_article.author=User.objects.get(id=request.user.id)  #指定author为id=1的管理员用户
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()  #提交到数据库
            article_post_form.save_m2m() #保存 tags 的多对多关系
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:          #如果用户是获取数据，则返回一个空的表单类对象，提供给用户填写。
        article_post_form=ArticlePostForm()
        columns=ArticleColumn.objects.all()
        context={'article_post_form':article_post_form,'columns': columns}
        return render(request,'article/create.html',context)

def article_safe_delete(request,id):
    if request.method=='POST':
        article=ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")

@login_required(login_url='/userprofile/login/')  #过滤未登录的用户
def article_update(request,id):
    article=ArticlePost.objects.get(id=id)
    #过滤非作者的用户
    if request.user!=article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    if request.method=='POST':
        article_post_form=ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title=request.POST['title']
            article.body=request.POST['body']
            if request.FILES.get('avatar'):
                article.avatar=request.FILES.get('avatar')
            if request.POST['column']!='none':
                article.column=ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column=None
            #tags.set()和tags.names()就是库提供的接口了，分别用于更新数据和获取标签名
            article.tags.set(*request.POST.get('tags').split(','),clear=True)
            article.save()
            return redirect("article:article_detail",id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        columns=ArticleColumn.objects.all()
        article_post_form=ArticlePostForm()
        context={'article':article,'article_post_form':article_post_form,'columns':columns,
                 'tags':','.join([x for x in article.tags.names()]),
                 }
        return render(request,'article/update.html',context)

class IncreaseLikesView(View):
    def post(self,request,*args,**kwargs):
        article=ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes+=1
        article.save()
        return HttpResponse('success')