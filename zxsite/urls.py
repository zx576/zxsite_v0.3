from django.conf.urls import url,include
from . import views

app_name = 'zxsite'

urlpatterns = [
#---------------------------主页------------------------------------------------------------------
    url(r'^$',views.index,name='index'),
#---------------------------主页------------------------------------------------------------------
    url(r'^search/$',views.search,name='search'),
#---------------------------管理页------------------------------------------------------------------
    url(r'^manage/$',views.manage,name='manage'),
    url(r'^manage/newarticle/$',views.newarticle,name='newarticle'),
    url(r'^manage/newarticle/save/$',views.savearticle,name='savearticle'),
    url(r'^manage/edit/$',views.managedit,name='managedit'),
    url(r'^manage/delete/$',views.managedelete,name='managedelete'),
    url(r'^article/edit/(?P<atc_id>[0-9]+)/$',views.editarticle,name='editarticle'),
    url(r'^article/delete/(?P<atc_id>[0-9]+)/$',views.deletearticle,name='deletearticle'),
    url(r'^article/truelydelete/(?P<atc_id>[0-9]+)/$',views.truelydeletearticle,name='truelydeletearticle'),
    url(r'^article/redit/(?P<atc_id>[0-9]+)/$',views.redit,name='redit'),

#---------------------------登录注册注销-------------------------------------------------------------
    url(r'^login/$',views.log_in,name='login'),
    url(r'^logout/$',views.log_out,name='logout'),
    url(r'^register/$',views.register,name='regiter'),
    url(r'^register/verifyname/$',views.verifyname,name='verifyname'),
#---------------------------文章页------------------------------------------------------------------
    url(r'^article/(?P<atc_id>[0-9]+)/$',views.article_ins,name='articleins'),
    url(r'^comment/(?P<atc_id>[0-9]+)/$',views.newcomment,name='newcomment'),
#---------------------------about------------------------------------------------------------------
    url(r'^about/$',views.about,name='about'),
#---------------------------索引------------------------------------------------------------------
    url(r'^indexbydate/$',views.indexbydate,name='indexbydate'),
    # url(r'^indexbydate/more/$',views.datemore,name='datemore')
    #tag索引
    url(r'^indexbytag/$',views.indexbytag,name='indexbutag'),
    url(r'^tags/(?P<tagid>[0-9]+)/$',views.tag_ins,name='tagins'),
#---------------------------主页------------------------------------------------------------------
    url(r'user/(?P<userid>[0-9]+)/$',views.edituser,name='edituser'),
    # url(r'^/',views.errorpage,name='errors')
#---------------------------echarts------------------------------------------------------------------
    url(r'^echarts/$',views.echarts,name='echarts'),

]