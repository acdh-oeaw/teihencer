from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^import-single-doc/$', views.ImportTEI.as_view(), name='import_tei'),
    url(r'^import-placelist/$', views.ImportPlaceListTEI.as_view(), name='import_placelist'),
]
