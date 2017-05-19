from django.conf.urls import url, include
from . import views

urlpatterns = [
url(r'^$', views.start_view, name="start"),
url(r'^paas-project/$', views.paas_view, name="paas-project"),
url(r'^apis-project/$', views.apis_view, name="apis-project"),
url(r'^login/$', views.user_login, name='user_login'),
url(r'^accounts/login/$', views.user_login, name='user_login'),
url(r'^logout/$', views.user_logout, name='user_logout'),
]