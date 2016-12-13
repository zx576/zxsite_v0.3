from django.conf.urls import url,include
from . import views

app_name = 'zxsite'

urlpatterns = [
#---------------------------主页------------------------------------------------------------------
    url(r'^$',views.index,name='index'),
#---------------------------管理页------------------------------------------------------------------
    url(r'^manage/$',views.manage),
    url(r'^manage/newarticle/$',views.newarticle),
#---------------------------登录注册注销------------------------------------------------------------------
    url(r'^login/$',views.log_in),
    url(r'^logout/$',views.log_out),
    url(r'^register/$',views.register),
    url(r'^register/verifyname/$',views.verifyname),
]