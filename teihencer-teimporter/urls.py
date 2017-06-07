from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^import/$', views.import_tei, name='import_tei'),
]
