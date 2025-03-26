"""
URL configuration for FinP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from mysite.views import index,forget,index,aichat2,logout,user_authentication,yearfinal,dragon,disclaimer
from mysite import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path("admin/", admin.site.urls),
    path('', index, name='members'),
    path('index/', index, name='index'),
    path('login/', user_authentication, name='login'),
    path('we/', views.we, name='we'),
    path('forget/', forget, name='forget'),   
    path('logout/', logout, name='logout'),
    path('aboutme/', views.aboutme, name='aboutme'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),

    #書籍
    path('book/', views.bookpage, name='book'),
    path('book/<str:book_id>/', views.book_detail, name='book_detail'),

    #年
    path('year/', views.year, name='year'),
    path('yearfinal/', yearfinal, name='yearfinal'),
    path('year12/', views.year12, name='year12'),
    path('dragon/', dragon, name='dragon'),
    
    #日
    path('day/', views.day, name='day'),
    path('day12/', views.day12, name='day12'),

    #處理對話訊息
    path('aichat2/', aichat2, name='aichat2'),
    #建立聊天室
    path('create_chatroom/', views.create_chatroom, name='create_chatroom'),
    #刪除聊天室
    path('delete_chatroom/', views.delete_chatroom, name='delete_chatroom'),
    #改名
    path('rename_chatroom/<int:chatroom_id>/', views.rename_chatroom, name='rename_chatroom'),
    #傳送訊息
    path('chat/send/', views.send_message, name='send_message'),
    #取得聊天室訊息
    path('chat/messages/<int:chatroom_id>/', views.get_chat_messages, name='get_chat_messages'),


    #重製
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #改個人資料
    #path('view_birthday/', views.view_birthday, name='view_birthday'),
    path('update_birthday/', views.update_birthday, name='update_birthday'),
    path('update_birthday_time/', views.update_birthday_time, name='update_birthday_time'),
    path('update_sex/', views.update_sex, name='update_sex'),
]

















