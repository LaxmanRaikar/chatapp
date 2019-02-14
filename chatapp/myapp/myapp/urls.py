from django.conf.urls import include, url
from django.contrib import admin

from chat import views
urlpatterns = [

    url('', include('chat.urls')),
    url(r'^special/', views.special, name='special'),
    url(r'^chat/',include('chat.urls')),
    url(r'^logout/$', views.user_logout, name='logout'),
    #
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    #
    url(r'^enter/', views.enter, name='enter')


]