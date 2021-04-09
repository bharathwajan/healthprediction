from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='homepage'),
    path('index.html',views.home,name='homepage'),
    path('login.html', views.login,name='login_page'),
    path('aboutus.html', views.aboutus,name='homepage'),
    path('register.html', views.register,name='homepage'),
    path('registernew',views.newmember,name='newmember'),
    path('newlogin',views.newlogin,name='login'),
    path('hey.html',views.hey,name='hey'),
    path('logout',views.logout,name='logout'),
    path('question.html',views.question,name='main'),
    path('predict',views.predict,name='prediction'),
    path('result_prediction',views.result_prediction,name='result_prediction')
    
]