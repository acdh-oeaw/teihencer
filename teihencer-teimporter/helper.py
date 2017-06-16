from entities.models import *
from metainfo.models import *
from django.db import transaction
from .stanbol import StbGeoQuerySettings, find_loc, decide_stanbol
from helper_functions.RDFparsers import PlaceUri
# https://stackoverflow.com/questions/32205220/cant-execute-queries-until-end-of-atomic-block-in-my-data-migration-on-django-1


def get_or_create_place(
        xml_id, place_name, col, src, base_url="https://teihencer.acdh.oeaw.ac.at/origid/"):
    o_name = unicodedata.normalize('NFC', place_name)
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
        place.save()

        return place
