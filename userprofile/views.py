from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm, ProfileForm

# Create your views here.
from .models import Profile


def user_login(request):
    if request.method=='POST':
        user_login_form=UserLoginForm(data=request.POST)

        if user_login_form.is_valid():
            data=user_login_form.cleaned_data  #通过cleaned_data属性访问清洗之后的数据
            print(data)

            user=authenticate(username=data['username'],password=data['password'])#验证用户名称和密码是否匹配，如果是，则将这个用户数据返回
            print(user)

            if user:
                login(request, user)  #实现用户登录，将用户数据保存在session中
                return redirect("article:article_list")
            else:
                return HttpResponse("账号密码输入有误。重输~")
        else:
            return HttpResponse("账号密码不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用postget请求数据")

def user_logout(request):
    logout(request)
    return redirect("article:article_list")

def user_register(request):
    if request.method=='POST':
        user_register_form=UserRegisterForm(data=request.POST)
        print('aaa')
        print(user_register_form)
        if user_register_form.is_valid():
            new_user=user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request,new_user)
            return redirect('article:article_list')
        else:
            return HttpResponse('注册表单输入有误。请重新输入~')

    elif request.method=="GET":
        user_register_form=UserRegisterForm()
        context ={'form':user_register_form}
        return render(request,'userprofile/register.html',context)
    else:
        return HttpResponse("请使用get或post请求数据")

@login_required(login_url='/userprofile/login/')  #要求调用user_delete()函数时，用户必须登录；如果未登录则不执行函数，将页面重定向到/userprofile/login/地址去。
def user_delete(request,id):
    if request.method=='POST':
        user=User.objects.get(id=id)
        if request.user==user:
            logout(request)
            user.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("你没有删除操作的权限。")
    else:
        return HttpResponse("仅接受post请求。")

@login_required(login_url='/userprofile/login/')
def profile_edit(request,id):
    # print('id:',id)
    user=User.objects.get(id=id)
    # print('user:',user)
    # profile=Profile.objects.get(user_id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile=Profile.objects.get(user_id=id)
    else:
        profile=Profile.objects.create(user=user)
    # print('profile:',profile)
    if request.method=='POST':
        # print('request.user:',request.user)
        # print('user:',user)
        if request.user!=user:
            return HttpResponse("你没有权限修改此用户信息。")
        profile_form=ProfileForm(request.POST,request.FILES)
        # print('profile_form:',profile_form)
        if profile_form.is_valid():
            profile_cd=profile_form.cleaned_data
            profile.phone=profile_cd['phone']
            profile.bio=profile_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar=profile_cd['avatar']
            # print('profile:', profile)
            # print('profile.phone:', profile.phone)
            # print('profile.bio:', profile.bio)
            # print('profile.avatar:', profile.avatar)

            profile.save()
            return redirect("userprofile:edit",id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method=='GET':
        profile_form=ProfileForm()
        # print('GET_profile_form',profile_form)
        context={'profile_form':profile_form,'profile':profile,'user':user}
        return render(request,'userprofile/edit.html',context)
    else:
        return HttpResponse("请使用GET或POST请求数据")



