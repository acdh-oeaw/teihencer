from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^import/$', views.ImportTEI.as_view(), name='import_tei'),
]
