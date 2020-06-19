from django.urls import path

from . import views

app_name='article'
urlpatterns=[
    path('article-list/', views.article_list, name='article_list'),
    path('article-detail/<int:id>/',views.article_detail,name='article_detail'), #用尖括号<>定义需要传递的参数
    path('article-create/', views.article_create, name='article_create'),
    path('article-safe-delete/<int:id>/', views.article_safe_delete, name='article_safe_delete'),  # 用尖括号<>定义需要传递的参数
    path('article-update/<int:id>/', views.article_update, name='article_update'),  # 用尖括号<>定义需要传递的参数
    path('increase-likes/<int:id>/', views.IncreaseLikesView.as_view(), name='increase_likes'),  # 用尖括号<>定义需要传递的参数

]