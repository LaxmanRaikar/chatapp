from django.conf.urls import url
from . import views
app_name='chat'
urlpatterns = [
    url(r'^$', views.index, name='index'),  # 127.0.0.0:8000/
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login,name='user_login'),
    url(r'^room/(?P<room_name>[^/]+)/$', views.room, name='room'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate')
]



