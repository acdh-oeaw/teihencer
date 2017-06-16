import lxml.etree as ET
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic.edit import FormView
from .tei import TeiReader, TeiPlaceList
from .forms import UploadFileForm, UploadPlaceListForm
from .helper import get_or_create_place
from entities.models import *
from metainfo.models import *
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
        current_user = self.request.user
        context = super(ImportPlaceListTEI, self).get_context_data(**kwargs)
        super_collection, _ = Collection.objects.get_or_create(name='teihencer-all')
        current_group, _ = Group.objects.get_or_create(name=current_user.username)
        current_group.user_set.add(current_user)
        cd = form.cleaned_data
        file = cd['file'].read()
        src, _ = Source.objects.get_or_create(orig_filename=cd['file'].name, author=current_user)
        text, _ = Text.objects.get_or_create(text=file, source=src)
        kind, _ = TextType.objects.get_or_create(name='process TEI DOC', entity='place')

        if cd['new_sub_collection'] == "":
            col, _ = Collection.objects.get_or_create(
                name=cd['collection']
            )
            if col.parent_class is None:
                print(col.parent_class)
                col.parent_class = super_collection
                col.save()
            else:
                pass
        else:
            parent_collection, _ = Collection.objects.get_or_create(
                name=cd['collection'],
                parent_class=super_collection,
            )
            parent_collection.groups_allowed.add(current_group)
            parent_collection.save()
            col, _ = Collection.objects.get_or_create(
                name=cd['new_sub_collection'],
                parent_class=parent_collection,
            )
        col.groups_allowed.add(current_group)
        col.save()

        teifile = TeiPlaceList(file)
        places = teifile.parse_placelist()
        before = len(Place.objects.all())
        fails = []
        print(places['amount'])
        for x in places['places']:
            place = teifile.place2dict(x)
            new_place = get_or_create_place(
                place['xml:id'],
                place['placeNames'][0]['text'],
                col, src, base_url=col.name
            )
            new_place.collection.add(col)
            new_place.save()
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
        current_user = self.request.user
        # for x in Place.objects.all():
        #     x.delete()
        # for x in Collection.objects.all():
        #     x.delete()
        # for x in Text.objects.all():
        #     x.delete()
        # for x in Source.objects.all():
        #     x.delete()
        context = super(ImportTEI, self).get_context_data(**kwargs)
        super_collection, _ = Collection.objects.get_or_create(name='teihencer-all')
        current_group, _ = Group.objects.get_or_create(name=current_user.username)
        current_group.user_set.add(current_user)
        cd = form.cleaned_data

        if cd['new_sub_collection'] == "":
            col, _ = Collection.objects.get_or_create(
                name=cd['collection']
            )
            if col.parent_class is None:
                print(col.parent_class)
                col.parent_class = super_collection
                col.save()
            else:
                pass
        else:
            parent_collection, _ = Collection.objects.get_or_create(
                name=cd['collection'],
                parent_class=super_collection,
            )
            parent_collection.groups_allowed.add(current_group)
            parent_collection.save()
            col, _ = Collection.objects.get_or_create(
                name=cd['new_sub_collection'],
                parent_class=parent_collection,
            )
        src, _ = Source.objects.get_or_create(orig_filename=cd['file'].name, author=current_user)
        col.groups_allowed.add(current_group)
        col.save()
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
                    x['ref'], x['text'], col, src, base_url=col.name)
                new_place.text.add(text)
                new_place.text.add(placeindex)
                new_place.save()
        else:
            pass
        return render(self.request, self.template_name, context)
