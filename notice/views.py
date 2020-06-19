from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView

from article.models import ArticlePost

# 继承自ListView，用于展示所有的未读通知
# 混入类LoginRequiredMixin，要求调用此视图必须先登录
class CommentNoticeListView(LoginRequiredMixin,ListView):
    context_object_name = 'notices'
    template_name = 'notice/list.html'
    login_url = '/userprofile/login/'
    # 返回了传递给模板的上下文对象
    def get_queryset(self):
        # unread()获取所有未读通知的集合
        return self.request.user.notifications.unread()

# 继承自View，获得了如get、post等基础的方法
class CommentNoticeUpdateView(View):
    def get(self,request):
        notice_id=request.GET.get('notice_id')
        # if语句用来判断转换单条还是所有未读通知。
        if notice_id:
            article=ArticlePost.objects.get(id=request.GET.get('article_id'))
            # mark_as_read()、mark_all_as_read都是模块提供的方法，用于将未读通知转换为已读
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(article)
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')