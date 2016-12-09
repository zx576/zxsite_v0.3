from django.conf.urls import url,include
from . import views

app_name = 'zxsite'

urlpatterns = [
#---------------------------主页------------------------------------------------------------------
    url(r'',views.index,name='index')
]