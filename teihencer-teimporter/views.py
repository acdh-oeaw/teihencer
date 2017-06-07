from io import TextIOWrapper, BytesIO, StringIO
from django.shortcuts import render
from .tei import TeiReader
from .forms import UploadFileForm


def import_tei(request):
    context = {}
    if request.method == 'POST':
        context["form"] = UploadFileForm(request.POST, request.FILES)
        if context["form"].is_valid():
            xpath = context["form"].cleaned_data['xpath']
            file = TextIOWrapper(request.FILES['file'].file, encoding='utf-8').read()
            file = file.replace(r'encoding="UTF-8"', '')
            teifile = TeiReader(file)
            context['worked'] = teifile.find_elements(xpath)
            return render(request, 'teimporter/import_tei.html', context)
    else:
        context["form"] = UploadFileForm()
        context['worked'] = "upload something first"
    return render(request, 'teimporter/import_tei.html', context)
