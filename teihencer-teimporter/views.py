import lxml.etree as ET
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic.edit import FormView
from .tei import TeiReader, TeiPlaceList
from .forms import UploadFileForm, UploadPlaceListForm
from .helper import get_or_create_place, create_metatdata
from entities.models import *
from metainfo.models import *
from helper_functions.RDFparsers import GenericRDFParser
from vocabularies.models import TextType


@method_decorator(login_required, name="dispatch")
class ImportPlaceListTEI(FormView):
    template_name = 'teimporter/import_placelist.html'
    form_class = UploadPlaceListForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(ImportPlaceListTEI, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form, **kwargs):
        context = super(ImportPlaceListTEI, self).get_context_data(**kwargs)
        current_user = self.request.user
        metadata = create_metatdata(current_user, form)
        teifile = TeiPlaceList(metadata['file'])
        places = teifile.parse_placelist()
        before = len(Place.objects.all())
        fails = []
        cd = form.cleaned_data
        print(places['amount'])
        if cd['xpath'] == "":
            for x in places['places']:
                place = teifile.place2dict(x)
                new_place = get_or_create_place(
                    place['xml:id'][0],
                    place['placeNames'][0]['text'],
                    base_url=metadata['col'].name
                )
                new_place.collection.add(metadata['col'])
                new_place.source = metadata['src']
                new_place.text.add(metadata['text'])
                new_place.save()
        else:
            for x in places['places']:
                place_uri = teifile.fetch_ID(x, cd['xpath'], 'geonames')
                print(place_uri)
                if place_uri['status']:
                    try:
                        # new_place = PlaceUri(place_uri['fetched_id']).place
                        GenericRDFParser(place_uri, 'Place')
                        # new_place = GenericRDFParser.get_or_create
                        new_place.collection.add(metadata['col'])
                        new_place.source = metadata['src']
                        new_place.text.add(metadata['text'])
                        new_place.save()
                    except:
                        pass

        after = len(Place.objects.all())
        context['counter'] = [before, after]
        return render(self.request, self.template_name, context)


@method_decorator(login_required, name="dispatch")
class ImportTEI(FormView):
    template_name = 'teimporter/import_tei.html'
    form_class = UploadFileForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(ImportTEI, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form, **kwargs):
        context = super(ImportTEI, self).get_context_data(**kwargs)
        current_user = self.request.user
        metadata = create_metatdata(current_user, form)
        cd = form.cleaned_data
        xpath = cd['xpath']
        teifile = TeiReader(metadata['file'])
        added_ids = teifile.add_ids(xpath)
        place_list = teifile.create_place_index(added_ids[0])
        context['place_list'] = ET.tostring(place_list, pretty_print=True, encoding="UTF-8")
        context['processd_file'] = ET.tostring(
            added_ids[1], pretty_print=True, encoding="UTF-8"
        )
        text, _ = Text.objects.get_or_create(text=context['processd_file'], source=metadata['src'])
        kind, _ = TextType.objects.get_or_create(name='process TEI DOC', entity='place')
        kind.collections.add(metadata['col'])
        kind.save()
        text.kind = kind
        text.save()

        placeindex, _ = Text.objects.get_or_create(text=context['place_list'], source=metadata['src'])
        kind, _ = TextType.objects.get_or_create(name='generated place list', entity='place')
        kind.collections.add(metadata['col'])
        kind.save()
        placeindex.kind = kind
        placeindex.save()
        if cd['enrich']:
            for x in added_ids[0]:
                new_place = get_or_create_place(
                    x['ref'], x['text'], base_url=metadata['col'].name
                )
                new_place.text.add(text)
                new_place.text.add(placeindex)
                new_place.save()
        else:
            pass
        return render(self.request, self.template_name, context)
