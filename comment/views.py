from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from article.models import ArticlePost
from .forms import CommentForm
from .models import Comment
from notifications.signals import notify

@login_required(login_url='/userprofile/login/')
def post_comment(request,article_id,parent_comment_id=None):

    article=get_object_or_404(ArticlePost,id=article_id)
    #ArticlePost.objects.get(id=article_id)
    # print('post_comment')
    if request.method=='POST':
        comment_form=CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.article=article
            new_comment.user=request.user


            # 二级回复
            if parent_comment_id:
                parent_comment=Comment.objects.get(id=parent_comment_id)
                new_comment.parent_id=parent_comment.get_root().id
                new_comment.reply_to=parent_comment.user
                new_comment.save()
                # 给其他用户发送通知
                if not parent_comment.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )
                return JsonResponse({"code":"200 OK","new_comment_id":new_comment.id})
                # redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
                # return redirect(redirect_url)
            new_comment.save()
            # 给管理员发送通知
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=article,
                    action_object=new_comment,
                )
                print(article)
                print(new_comment)
            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    elif request.method=='GET':
        # print('GET')

        comment_form=CommentForm()
        context={
            'comment_form':comment_form,
            'article_id':article_id,
            'parent_comment_id':parent_comment_id
        }
        return render(request,'comment/reply.html',context)

    else:
        # print(article)

        return HttpResponse("发表评论仅接受POST请求。")
