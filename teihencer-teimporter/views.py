from io import TextIOWrapper, BytesIO, StringIO
import lxml.etree as ET
from django.shortcuts import render
from django.views.generic.edit import FormView
from .tei import TeiReader
from .forms import UploadFileForm


class ImportTEI(FormView):
    template_name = 'teimporter/import_tei.html'
    form_class = UploadFileForm
    success_url = '.'

    def form_valid(self, form, **kwargs):
        context = super(ImportTEI, self).get_context_data(**kwargs)
        xpath = form.cleaned_data['xpath']
        file = form.cleaned_data['file'].read()
        teifile = TeiReader(file)
        added_ids = teifile.add_ids(xpath)
        place_list = teifile.create_place_index(added_ids[0])
        context['place_list'] = ET.tostring(place_list, pretty_print=True, encoding="UTF-8")
        context['processd_file'] = ET.tostring(added_ids[1], pretty_print=True, encoding="UTF-8")
        return render(self.request, 'teimporter/import_tei.html', context)
