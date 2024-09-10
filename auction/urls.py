from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('user',views.user,name='user'),
    path('signup',views.signup,name='signup'),
    path('userdata',views.userdata,name='userdata'),
    path('login',views.login,name='login'),
    path('sell',views.sell,name='sell'),
    path('product',views.product,name='product'),
    path('bid',views.bid,name='bid'),
    path('bidprod',views.bidprod,name='bidprod'),
    path('yourprod',views.yourprod,name='yourprod'),
    path('bidd',views.bidd,name='bidd'),
    path('raisebid',views.raisebid,name='raisebid'),
    path('bidding',views.bidding,name='bidding'),
    path('prod',views.prod,name='prod'),
    path('info1',views.info1,name='info1'),
    path('info2',views.info2,name='info2')   
] 