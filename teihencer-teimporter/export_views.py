import lxml.etree as ET
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from metainfo.models import Uri
from entities.views import GenericListView
from entities.models import Place
from entities.tables import PlaceTable
from entities.filters import PlaceListFilter
from entities.forms import GenericFilterFormHelper
from teimporter import tei


class ExportTeiListPlace(GenericListView):

    """ serializes the filtered entites as TEI-doc (tei:listPlace)"""

    model = Place
    table_class = PlaceTable
    filter_class = PlaceListFilter
    formhelper_class = GenericFilterFormHelper

    def get(self, request):
        teiprocessor = tei.TeiPlaceList(tei.tei_document)
        queryset = self.get_queryset()
        places = []
        for x in queryset:
            uris = Uri.objects.filter(entity=x.id)
            if len(uris) > 1:
                xmlid = uris[1].uri
                idno = uris[0].uri
            else:
                xmlid = uris[0].uri
                idno = uris[0].uri
            places.append(teiprocessor.create_place(
                xmlid, x.name, x.lat, x.lng, idno)
            )
        placelist = teiprocessor.create_place_index_from_place_elements(places)
        output = ET.tostring(placelist, encoding="utf-8")
        response = HttpResponse(output, content_type='application/xhtml+xml')
        return response
