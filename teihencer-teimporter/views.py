import lxml.etree as ET
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic.edit import FormView
from .tei import TeiReader
from .stanbol import StbGeoQuerySettings, find_loc, decide_stanbol
from .forms import UploadFileForm
from entities.models import *
from metainfo.models import *
from vocabularies.models import CollectionType, TextType
from helper_functions.RDFparsers import PlaceUri


def get_or_create_place(xml_id, place_name, col, src, base_url="https://teihencer.acdh.oeaw.ac.at/origid/"):
    o_name = place_name
    url = '{}{}'.format(base_url, xml_id)
    place = Place.get_or_create_uri(url)
    if place:
        return place
    else:
        loc = find_loc([o_name])
        if loc == (False, False):
            place = Place.objects.create(name=o_name, status='no match')
        else:
            if len(loc[1]) > 1:
                loc = decide_stanbol(loc[1], distance=20)
                if len(loc) > 1:
                    place = Place.objects.create(name=o_name, status='ambigue')
                    for zz in loc:
                        uri2 = UriCandidate.objects.create(
                            uri=zz['id'], entity=place, responsible='stanbol',
                            confidence=zz['http://stanbol.apache.org/ontology/entityhub/query#score'][0]['value']
                        )
                else:
                    place = PlaceUri(loc[0]['id']).place
            else:
                try:
                    place = PlaceUri(loc[1]['id']).place
                except:
                    place = PlaceUri(loc[1][0]['id']).place

        try:
            uri = Uri.objects.create(uri=url, entity=place)
        except:
            print('error double entry: {}'.format(url))
        place.source = src
        place.collection.add(col)
        place.save()
        return place


@method_decorator(login_required, name="dispatch")
class ImportTEI(FormView):
    template_name = 'teimporter/import_tei.html'
    form_class = UploadFileForm
    success_url = '.'

    def form_valid(self, form, **kwargs):
        for x in Place.objects.all():
            x.delete()
        for x in Collection.objects.all():
            x.delete()
        for x in Text.objects.all():
            x.delete()
        for x in Source.objects.all():
            x.delete()
        context = super(ImportTEI, self).get_context_data(**kwargs)
        cd = form.cleaned_data
        current_user = self.request.user
        if cd['collection']:
            current_collection = "{}".format(cd['collection'])
        elif cd['new_collection']:
            current_collection = "{}_{}".format(current_user.username, cd['new_collection'])
        else:
            current_collection = "{}".format(current_user.username)
        print(current_user.username, current_collection)
        src, _ = Source.objects.get_or_create(orig_filename=cd['file'].name, author=current_user)
        col, _ = Collection.objects.get_or_create(name=current_collection)
        xpath = cd['xpath']
        file = cd['file'].read()
        teifile = TeiReader(file)
        added_ids = teifile.add_ids(xpath)
        place_list = teifile.create_place_index(added_ids[0])
        context['place_list'] = ET.tostring(place_list, pretty_print=True, encoding="UTF-8")
        context['processd_file'] = ET.tostring(
            added_ids[1], pretty_print=True, encoding="UTF-8"
        )
        text, _ = Text.objects.get_or_create(text=context['processd_file'], source=src)
        kind, _ = TextType.objects.get_or_create(name='process TEI DOC', entity='place')
        kind.collections.add(col)
        kind.save()
        text.kind = kind
        text.save()

        placeindex, _ = Text.objects.get_or_create(text=context['place_list'], source=src)
        kind, _ = TextType.objects.get_or_create(name='generated place list', entity='place')
        kind.collections.add(col)
        kind.save()
        placeindex.kind = kind
        placeindex.save()
        if cd['enrich']:
            for x in added_ids[0]:
                new_place = get_or_create_place(
                    x['ref'], x['text'], col, src, base_url="https://schnitzler-diary/")
                new_place.text.add(text)
                new_place.text.add(placeindex)
                new_place.save()
        else:
            pass
        return render(self.request, self.template_name, context)
