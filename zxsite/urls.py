from django.conf.urls import url,include
from . import views

app_name = 'zxsite'

urlpatterns = [
#---------------------------主页------------------------------------------------------------------
    url(r'^$',views.index,name='index'),
#---------------------------管理页------------------------------------------------------------------
    url(r'^manage/$',views.manage,name='manage'),
    url(r'^manage/newarticle/$',views.newarticle,name='newarticle'),
    url(r'^manage/newarticle/save/$',views.savearticle,name='savearticle'),
#---------------------------登录注册注销-------------------------------------------------------------
    url(r'^login/$',views.log_in,name='login'),
    url(r'^logout/$',views.log_out,name='logout'),
    url(r'^register/$',views.register,name='regiter'),
    url(r'^register/verifyname/$',views.verifyname,name='verifyname'),
#---------------------------文章页------------------------------------------------------------------
    url(r'^article/(?P<atc_id>[0-9]+)/$',views.article_ins,name='articleins'),
#---------------------------about------------------------------------------------------------------
    url(r'^about/$',views.about,name='about'),
#---------------------------索引------------------------------------------------------------------
    url(r'^indexbydate/',views.indexbydate,name='indexbydate'),
    # url(r'^indexbydate/more/$',views.datemore,name='datemore')
]