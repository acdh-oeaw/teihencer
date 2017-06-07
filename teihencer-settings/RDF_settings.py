gno = 'http://www.geonames.org/ontology#'
wgs84 = "http://www.w3.org/2003/01/geo/wgs84_pos#"
gndo = 'http://d-nb.info/standards/elementset/gnd#'
owl = "http://www.w3.org/2002/07/owl#"
geo = "http://www.opengis.net/ont/geosparql#"

sett_RDF_generic_depricated = {
    'Place': {
        'data': [
            {
                'base_url': 'http://sws.geonames.org/',
                'url_appendix': 'about.rdf',
                'attributes': [
                    {
                        'name': 'name',
                        'identifiers': (
                            (('objects', 'prefName', gno + 'officialName', ('language', 'de')),),
                            (('objects', 'prefName', gno + 'alternateName', ('language', 'pl')),)
                        )
                    },
                    {
                        'name': 'lat',
                        'identifiers': (
                            (('objects', 'lat', wgs84 + 'lat', None),),
                        )
                    },
                    {
                        'name': 'long',
                        'identifiers': (
                            (('objects','lng', wgs84 + 'long', None),),
                        )
                    }
                ]
            }
        ],
        'matching': {
            'name': ['string', (('prefName', None), ),], #tuple of attribute names and strings (used for joins)
            'lng': ['integer', (('lng', None), ),],
            'lat': ['integer', (('lat', None), ),]

        }
    },
    'Person': {
        'data': [
            {
                'base_url': 'http://d-nb.info/gnd/',
                'url_appendix': 'about/rdf',
                'attributes': [
                    {
                        'name': 'name',
                        'identifiers': (
                            (
                             ('objects', 'prefNameNode', gndo + 'preferredNameEntityForThePerson', None),'>',
                             ('objects', 'forename', gndo + 'forename', None), '=',
                             ('objects', 'surname', gndo + 'surname', None)
                        ),
                            (
                              ('objects', 'prefNameNode', gndo + 'variantNameEntityForThePerson', None), '>',
                                ('objects', 'descriptionNode', gndo + 'Description', None), '>',
                                ('objects', 'personalName', gndo + 'personalName', None), '=',
                                ('objects', 'personalNameAddition', gndo + 'nameAddition', None), '=',
                                ('objects', 'personalNameCounting', gndo + 'counting', None)
                            ),

                        )
                    },
                    {
                        'name': 'label',
                        'identifiers': (
                            (
                             ('objects', 'prefNameNode', gndo + 'variantNameEntityForThePerson', None),'>',
                             ('objects', 'forename', gndo + 'forename', None), '=',
                             ('objects', 'surname', gndo + 'surname', None)
                        ),
                        )
                    }
                ]
            }
        ],
        'matching': {
            'first_name': ['string', (('forename', None),),],
            'name': ['string', (('surname', None),), (('personalName', None), '-', ('personalNameAddition', None), ' ', ('personalNameCounting', None)), (('name', None),)],
            'label': ['label', (('label', None),),],
        }
    }
}

sett_RDF_generic = {
    'Place': {
        'data': [
            {
                'base_url': 'http://sws.geonames.org/',
                'url_appendix': 'about.rdf',
                'kind': (
                    (gno + 'featureCode', None),
                    ),
                'attributes': [
                    {
                        'name': 'name',
                        'identifiers': (
                            (('objects', 'prefName', gno + 'officialName', ('language', 'de')),),
                            (('objects', 'prefName', gno + 'officialName', ('language', 'en')),),
                            (('objects', 'prefName', gno + 'name', None),),
                            (('objects', 'prefName', gno + 'alternateName', ('language', 'de')),),
                            (('objects', 'prefName', gno + 'alternateName', ('language', 'en')),)
                        )
                    },
                    {
                        'name': 'label',
                        'identifiers': (
                            (('objects', 'label', gno + 'alternateName', ('language', 'de')),),
                            (('objects', 'label', gno + 'alternateName', ('language', 'en')),)
                        )
                    },
                    {
                        'name': 'lat',
                        'identifiers': (
                            (('objects', 'lat', wgs84 + 'lat', None),),
                        )
                    },
                    {
                        'name': 'long',
                        'identifiers': (
                            (('objects','lng', wgs84 + 'long', None),),
                        )
                    },
                    {
                        'name': 'parentFeature',
                        'identifiers': (
                            (('objects', 'parentFeature', gno + 'parentFeature', None),),
                        )
                    },
                    {
                        'name': 'parentCountry',
                        'identifiers': (
                            (('objects', 'parentCountry', gno + 'parentCountry', None),),
                        )
                    },
                ]
            },
            {
                'base_url': 'http://d-nb.info/gnd/',
                'url_appendix': 'about/rdf',
                'attributes': [
                    {
                        'name': 'name',
                        'identifiers': (
                            (('objects', 'prefName', gndo + 'preferredNameForThePlaceOrGeographicName', None),),
                        )
                    },
                    {
                        'name': 'label',
                        'identifiers': (
                            (
                                ('objects', 'label', gndo + 'variantNameForThePlaceOrGeographicName', None),
                            ),
                        ),
                    },
                    {
                        'name': 'latlong',
                        'identifiers': (
                            (('objects', 'latlong_base', geo + 'hasGeometry', None), '>',
                             ('objects', 'latlong_geonode', geo + 'asWKT', None)
                             ),
                        )
                    },
                ]
            }
        ],
        'matching': {
            'attributes': {
                'name': (
                    (('prefName', None),),
                ),
                'lat': (
                    (('lat', None),),
                    (('latlong_geonode', ('Point \( [+-]([0-9\.]+) [+-]([0-9\.]+)', 1)),)
                ),
                'lng': (
                    (('lng', None),),
                    (('latlong_geonode', ('Point \( [+-]([0-9\.]+) [+-]([0-9\.]+)', 2)),)
                ),
            },
            'labels': {
                'alternative name': (
                    ('label', None),
                ),
                },
            'linked objects':
            [
            {
                'type': 'Place',
                'kind': 'located in',
                'object': (
                    ('parentFeature', None),
            )
            },
            {
                'type': 'Place',
                'kind': 'located in',
                'object': (
                    ('parentCountry', None),
            )
            },
            ],
        }
    },
    'Person': {
        'data': [
            {
                'base_url': 'http://d-nb.info/gnd/',
                'url_appendix': 'about/rdf',
                'attributes': [
                    {
                        'name': 'name',
                        'identifiers': (
                            (
                             ('objects', 'prefNameNode', gndo + 'preferredNameEntityForThePerson', None),'>',
                             ('objects', 'forename', gndo + 'forename', None), '=',
                             ('objects', 'surname', gndo + 'surname', None)
                        ),
                            (
                              ('objects', 'prefNameNode', gndo + 'variantNameEntityForThePerson', None), '>',
                                ('objects', 'descriptionNode', gndo + 'Description', None), '>',
                                ('objects', 'personalName', gndo + 'personalName', None), '=',
                                ('objects', 'personalNameAddition', gndo + 'nameAddition', None), '=',
                                ('objects', 'personalNameCounting', gndo + 'counting', None)
                            ),

                        )
                    },
                    {
                        'name': 'label',
                        'identifiers': (
                            (

                                ('objects', 'label', gndo + 'variantNameForThePerson', None),

                            ),
                        ),
                    },
                    {
                        'name': 'place of birth',
                        'identifiers': (
                        (
                            ('objects', 'place of birth', gndo + 'placeOfBirth', None),
                        ),
                    ),
                    },
                    {
                        'name': 'place of death',
                        'identifiers': (
                        (
                            ('objects', 'place of death', gndo + 'placeOfDeath', None),
                        ),
                    ),
                    },
                    {
                        'name': 'date of birth',
                        'identifiers': (
                        (
                            ('objects', 'date of birth', gndo + 'dateOfBirth', None),
                        ),
                    ),
                    },
                    {
                        'name': 'date of death',
                        'identifiers': (
                        (
                            ('objects', 'date of death', gndo + 'dateOfDeath', None),
                        ),
                    ),
                    },
                ]
            }
        ],
        'matching': {
            'attributes': {
                'name': (
                    (('surname', None),),
                ),
                'first_name': (
                    (('forename', None),),
                ),
                'start_date_written': (
                    (('date of birth', None),),
                ),
                'end_date_written': (
                    (('date of death', None),),
                ),
            },
            'labels': {
                'alternative name': (
                    ('label', None),
                ),
            },
            'linked objects':
            [
            {
                'type': 'Place',
                'kind': 'place of birth',
                'object': (
                    ('place of birth', None),
            )
            },
            {
                'type': 'Place',
                'kind': 'place of death',
                'object': (
                    ('place of death', None),
            )
            },
            ]
        }
    },
    'Event': {
        'data': [
            {
                'base_url': 'http://d-nb.info/gnd/',
                'url_appendix': 'about/rdf',
                'attributes': [
                    {
                        'name': 'name',
                        'identifiers': (
                            (('objects', 'prefName', gndo + 'preferredNameForTheSubjectHeading', None),),
                        )
                    },
                    {
                        'name': 'start',
                        'identifiers': (
                            (('objects', 'start_date', gndo + 'dateOfEstablishment', None),),
                        )
                    },
                    {
                        'name': 'end',
                        'identifiers': (
                            (('objects', 'end_date', gndo + 'dateOfTermination', None),),
                        )
                    },
                    {
                        'name': 'label',
                        'identifiers': (
                            (('objects', 'label', gndo + 'variantNameForTheSubjectHeading', None),),
                        )
                    },
                    {
                        'name': 'place of event',
                        'identifiers': (
                            (('objects', 'place of event', gndo + 'place', None),),
                        )
                    }
                ],
            }
        ],
        'matching': {
            'attributes': {
                'name': (
                    (('prefName', None),),
                ),
                'start_date_written': (
                    (('start_date', None),),
                ),
                'end_date_written': (
                    (('end_date', None),),
                )
            },
            'labels': {
                'alternative name': (
                    ('label', None),
                )
            },
            'linked objects': [
            {
                'type': 'Place',
                'kind': 'place of event',
                'object': (
                    ('place of event', None),
            )
            },
            ],
        }
    }
}
