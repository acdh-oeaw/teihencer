import re
import json
import requests

gn = "http://www.geonames.org/ontology#"
stb_base = 'http://enrich.acdh.oeaw.ac.at/entityhub/site/'
URL_geonames = stb_base + "geoNames_%s/query"
wgs84_pos = "http://www.w3.org/2003/01/geo/wgs84_pos#"
stb_find = stb_base + u'{}/find'


autocomp_settings = {
    'score': u'http://stanbol.apache.org/ontology/entityhub/query#score',
    'uri': 'id',
    'label': u'http://www.w3.org/2000/01/rdf-schema#label',
    'Place': [
        {'source': 'Geonames',
        'type': False,
        'url': stb_find.format('geoNames_S_P_A'),
        'fields': {
            'descr': (gn + 'featureCode','String'),
            'name': (gn + 'name','String'),
            'long': (wgs84_pos + 'long','String'),
            'lat': (wgs84_pos + 'lat','String')
        }},
        {'source': 'GeonamesRGN',
        'type': False,
        'url': stb_find.format('geoNames_RGN'),
        'fields': {
            'descr': (gn + 'featureCode','String'),
            'name': (gn + 'name','String'),
            'long': (wgs84_pos + 'long','String'),
            'lat': (wgs84_pos + 'lat','String')
        }},
        {'source': 'GeonamesVAL',
        'type': False,
        'url': stb_find.format('geoNames_VAL'),
        'fields': {
            'descr': (gn + 'featureCode','String'),
            'name': (gn + 'name','String'),
            'long': (wgs84_pos + 'long','String'),
            'lat': (wgs84_pos + 'lat','String')
        }},
        {'source': 'GND',
        'type': u'http://d-nb.info/standards/elementset/gnd#TerritorialCorporateBodyOrAdministrativeUnit',
        'url': stb_find.format('gndTerritorialCorporateBodyOrAdministrativeUnits'),
        'fields': {
            'name': (u'http://d-nb.info/standards/elementset/gnd#preferredNameForThePlaceOrGeographicName','String'),
            'descr': (u'http://d-nb.info/standards/elementset/gnd#definition','String'),}},
        ],
    'Institution': [{
        'source': 'GND',
        'type': u'http://d-nb.info/standards/elementset/gnd#CorporateBody',
        'url': stb_find.format('gndCorporateBodyAndOrganOfCorporateBody'),
        'fields': {
            'descr': (u'http://d-nb.info/standards/elementset/gnd#definition','String'),
            'name': (u'http://d-nb.info/standards/elementset/gnd#preferredNameForTheCorporateBody','String')}},
            {
        'source': 'GND',
        'type': u'http://d-nb.info/standards/elementset/gnd#OrganOfCorporateBody',
        'url': stb_find.format('gndCorporateBodyAndOrganOfCorporateBody'),
        'fields': {
            'descr': (u'http://d-nb.info/standards/elementset/gnd#definition','String'),
            'name': (u'http://d-nb.info/standards/elementset/gnd#preferredNameForTheCorporateBody','String')}}],
    'Person': [{
        'source': 'GND',
        'type': u'http://d-nb.info/standards/elementset/gnd#DifferentiatedPerson',
        'url': stb_find.format('gndPersons'),
        'fields': {
            'descr': (u'http://d-nb.info/standards/elementset/gnd#biographicalOrHistoricalInformation','String'),
            'name': (u'http://d-nb.info/standards/elementset/gnd#preferredNameForThePerson','String'),
            'dateOfBirth': (u'http://d-nb.info/standards/elementset/gnd#dateOfBirth', 'GNDDate'),
            'dateOfDeath': (u'http://d-nb.info/standards/elementset/gnd#dateOfDeath', 'GNDDate')}}],
    'Event': [{
        'source': 'GND',
        'type': u'http://d-nb.info/standards/elementset/gnd#HistoricSingleEventOrEra',
        'url': stb_find.format('gndHistoricEvent'),
        'fields': {
            'descr': (u'http://d-nb.info/standards/elementset/gnd#definition','String'),
            'name': (u'http://d-nb.info/standards/elementset/gnd#preferredNameForTheSubjectHeading','String')}}],
    'Work': []
}

geonames_feature_codes = {
    "ADM1": (
        "first-order administrative division",
        "a primary administrative division of a country, such as a state in the United States"),
    "ADM1H": (
        "historical first-order administrative division",
        "a former first-order administrative division"),
    "ADM2": (
        "second-order administrative division",
        "a subdivision of a first-order administrative division"),
    "ADM2H": (
        "historical second-order administrative division",
        "a former second-order administrative division"),
    "ADM3": (
        "third-order administrative division",
        "a subdivision of a second-order administrative division"),
    "ADM3H": (
        "historical third-order administrative division",
        "a former third-order administrative division"),
    "ADM4": (
        "fourth-order administrative division",
        "a subdivision of a third-order administrative division"),
    "ADM4H": (
        "historical fourth-order administrative division",
        "a former fourth-order administrative division"),
    "ADM5": (
        "fifth-order administrative division",
        "a subdivision of a fourth-order administrative division"),
    "ADMD": (
        "administrative division",
        "an administrative division of a country, undifferentiated as to administrative level"),
    "ADMDH": (
        "historical administrative division",
        "a former administrative division of a political entity, \
        undifferentiated as to administrative level"),
    "LTER": (
        "leased area",
        "a tract of land leased to another country, usually for military installations"),
    "PCL": ("political entity", ""),
    "PCLD": ("dependent political entity", ""),
    "PCLF": ("freely associated state", ""),
    "PCLH": ("historical political entity", "a former political entity"),
    "PCLI": ("independent political entity", ""),
    "PCLIX": ("section of independent political entity", ""),
    "PCLS": ("semi-independent political entity", ""),
    "PRSH": ("parish", "an ecclesiastical district"),
    "TERR": ("territory", ""),
    "ZN": ("zone", ""),
    "ZNB": (
        "buffer zone",
        "a zone recognized as a buffer between two nations in which \
        military presence is minimal or absent"),
    "PPL": (
        "populated place",
        "a city, town, village, or other agglomeration of buildings where people live and work"),
    "PPLA": (
        "seat of a first-order administrative division",
        "seat of a first-order administrative division (PPLC takes precedence over PPLA),"),
    "PPLA2": ("seat of a second-order administrative division", ""),
    "PPLA3": ("seat of a third-order administrative division", ""),
    "PPLA4": ("seat of a fourth-order administrative division", ""),
    "PPLC": ("capital of a political entity", ""),
    "PPLCH": (
        "historical capital of a political entity",
        "a former capital of a political entity"),
    "PPLF": (
        "farm village",
        "a populated place where the population is largely engaged in agricultural activities"),
    "PPLG": ("seat of government of a political entity", ""),
    "PPLH": (
        "historical populated place",
        "a populated place that no longer exists"),
    "PPLL": (
        "populated locality",
        "an area similar to a locality but with a small group of dwellings or other buildings"),
    "PPLQ": ("abandoned populated place", ""),
    "PPLR": (
        "religious populated place",
        "a populated place whose population is largely engaged in religious occupations"),
    "PPLS": (
        "populated places",
        "cities, towns, villages, or other agglomerations of buildings where people live and work"),
    "PPLW": (
        "destroyed populated place",
        "a village, town or city destroyed by a natural disaster, or by war"),
    "PPLX": ("section of populated place", ""),
    "STLMT": ("israeli settlement", ""),
    "RGN": ("region", "an area distinguished by one or more observable physical or cultural characteristics")}


class StbGeoQuerySettings:

    def __init__(self, kind='place'):
        self.kind = kind
        self.score = u'http://stanbol.apache.org/ontology/entityhub/query#score'
        self.uri = 'id'
        self.label = u'http://www.w3.org/2000/01/rdf-schema#label'
        self.kind = kind
        self.last_selected = 0

        if kind == 'place':
            self.selected = [gn+'name', gn+'parentPCLI', gn+'parentCountry',
                                gn+'parentADM1', gn+'parentADM2', gn+'parentADM3',
                                gn+'population', gn+'featureCode', wgs84_pos+'lat',
                                wgs84_pos+'long', gn+'alternateName', gn+'officialName',
                                gn+'shortName', gn+'countryCode', gn+'parentFeature']
            self.stored_feature = {
                    'feature': gn+'PPLC',
                    'URL': URL_geonames % 'PPLC'
            }
            self.features = [{
                    'feature': gn+'PPLC',
                    'URL': URL_geonames % 'PPLC'
            },
             {
                    'feature': gn+'PPLA',
                    'URL': URL_geonames % 'PPLA'
            },
                {
                    'feature': gn+'PPLA2',
                    'URL': URL_geonames % 'PPLA2'
            },
                {
                    'feature': gn+'PPLA3',
                    'URL': URL_geonames % 'PPLA3'
            },
                {
                    'feature': gn+'PPLA4',
                    'URL': URL_geonames % 'PPLA4'
            },
                {
                    'feature': gn+'PPL',
                    'URL': URL_geonames % 'PPL'
            }]
        elif kind == 'admin':
            self.selected = [gn+'featureCode']
            self.stored_feature = {
                    'feature': gn+'PCLI',
                    'URL': URL_geonames % 'PCLI'
            }
            self.features = [{
                    'feature': gn+'PCLI',
                    'URL': URL_geonames % 'PCLI'
            },
                {
                    'feature': gn+'ADM1',
                    'URL': URL_geonames % 'ADM1'
            },
                {
                    'feature': gn+'ADM2',
                    'URL': URL_geonames % 'ADM2'
            },
                {
                    'feature': gn+'ADM3',
                    'URL': URL_geonames % 'ADM3'
            }
            ]

    def get_next_feature(self, ft=False):
        if self.last_selected > len(self.features)-1:
            self.stored_feature = False
            return False
        if not ft:
            ft = self.features[self.last_selected]['feature']
        for idnx, x in enumerate(self.features):
            if x['feature'] == ft:
                try:
                    self.last_selected = idnx+1
                    self.stored_feature = self.features[idnx+1]
                    return self.features[idnx+1]
                except:
                    return None
        return self.features[0]

    def get_data(self, query, adm=False):
        if self.kind == 'place' and adm:
            data = {
                'limit': 20, 'constraints': [{
                    'type': 'text',
                    'field': 'http://www.w3.org/2000/01/rdf-schema#label',
                    'text': query},
                    {'type': 'reference', 'field': adm[1], 'value': adm[0]}
                                    ],
                'selected': self.selected
            }
        else:
            data = {
                'limit': 20, 'constraints': [{
                    'type': 'text',
                    'field': 'http://www.w3.org/2000/01/rdf-schema#label',
                    'text': query},
                                    ],
                'selected': self.selected}

        return data


def decide_stanbol(loc, distance=60):
    loc.sort(
        key=lambda tup: tup['http://stanbol.apache.org/ontology/entityhub/query#score'][0]['value']
    )
    second = loc[-2]['http://stanbol.apache.org/ontology/entityhub/query#score'][0]['value']+distance
    first = loc[-1]['http://stanbol.apache.org/ontology/entityhub/query#score'][0]['value']
    if second < first:
        return [loc[-1]]
    else:
        return loc


def decide_score_stanbol(results, dec_diff):
    difference = dec_diff
    val1 = results[0]['http://stanbol.apache.org/ontology/entityhub/query#score'][0]['value']
    val2 = results[1]['http://stanbol.apache.org/ontology/entityhub/query#score'][0]['value']
    if val1 > val2+difference:
        return results[0]
    else:
        return False


def find_geonames2(ca, name, adm=None, **kwargs):
    headers = {'Content-Type': 'application/json'}
    ca_feature = ca.stored_feature
    if not ca_feature:
        return False
    if adm:
        ca_data = ca.get_data(name, adm)
    else:
        ca_data = ca.get_data(name)
    ca.get_next_feature()
    r = requests.post(ca_feature['URL'], data=json.dumps(ca_data), headers=headers)
    if r.status_code == 200:
        res = r.json()
        if len(res['results']) == 1:
            return True, res['results'][0]
        elif len(res['results']) > 0:
            dec = decide_score_stanbol(res['results'], kwargs['dec_diff'])
            if dec:
                return True, dec
            else:
                return False, res['results']
        else:
            return False, False
    else:
        print(r.content)


def find_loc(lst, dec_diff=5):
    prev_elem = False
    t = False
    if len(lst) == 1:
        pl_selected_fields = StbGeoQuerySettings('place').selected
        headers = {'Content-Type': 'application/json'}
        results = []
        for s in autocomp_settings['Place']:
            ldpath = ""
            for d in pl_selected_fields:
                ldpath += "{} = <{}>;\n".format(d.split('#')[-1], d)
            data = {
                'limit': 20,
                'name': lst[0],
                'ldpath': ldpath
            }
            r = requests.get(s['url'], params=data, headers=headers)
            if r.status_code == 200:
                res = r.json()
                if len(res['results']) > 0:
                    results.extend(res['results'])
        if len(results) > 1:
            return False, results
        elif len(results) == 1:
            return True, results
        else:
            return False, False
    elif len(lst) > 1:
        for ind, c in enumerate(lst):
            if ind < len(lst)-1:
                if not t:
                    t = StbGeoQuerySettings('admin')
                if prev_elem:
                    countr = find_geonames2(t, c, prev_elem, dec_diff=dec_diff)
                else:
                    countr = find_geonames2(t, c, dec_diff=dec_diff)
                check = True
                while check:
                    if countr[0]:
                        if countr[1]['http://www.geonames.org/ontology#featureCode'][0]['value'] == 'http://www.geonames.org/ontology#A.PCLI':
                            prev_elem = (
                                countr[1]['id'],
                                'http://www.geonames.org/ontology#parentCountry'
                            )
                        else:
                            prev_elem = (countr[1]['id'], 'http://www.geonames.org/ontology#parent'+countr[1]['http://www.geonames.org/ontology#featureCode'][0]['value'].split('.')[-1])
                        check = False
                    if not countr[0]:
                        check = False
            else:
                o = StbGeoQuerySettings('place')
                if prev_elem:
                    place = find_geonames2(o, c, prev_elem, dec_diff=dec_diff)
                else:
                    place = find_geonames2(o, c, dec_diff=dec_diff)
                while place:
                    if place[1]:
                        return place
                    else:
                        if prev_elem:
                            place = find_geonames2(o, c, prev_elem, dec_diff=dec_diff)
                        else:
                            place = find_geonames2(o, c, dec_diff=dec_diff)
                return False


def retrieve_obj(uri):
    headers = {'Content-Type': 'application/json'}
    r = requests.get(
        'http://enrich.acdh.oeaw.ac.at/entityhub/site/geoNames_S_P_A/entity',
        params={'id': uri}, headers=headers
    )
    if r.status_code == 200:
        return r.json()
    else:
        return False
