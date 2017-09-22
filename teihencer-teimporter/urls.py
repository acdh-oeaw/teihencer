from django.conf.urls import url
from . import import_views
from . import export_views
from . import overridden_views


urlpatterns = [
    url(r'^import-single-doc/$', import_views.ImportTEI.as_view(), name='import_tei'),
    url(r'^import-placelist/$', import_views.ImportPlaceListTEI.as_view(), name='import_placelist'),
    url(
        r'^place/list/export-as-tei$',
        export_views.ExportTeiListPlace.as_view(),
        name='place_list_as_tei'
    ),
    url(r'^place/list/tei$', overridden_views.TeiPlaceListView.as_view(), name='place_list_tei'),
]
