import lxml.etree as ET
import hashlib
from templates import templates


class TeiReader():

    """ a class to read an process tei-documents"""

    def __init__(self, file):
        self.ns_tei = {'tei': "http://www.tei-c.org/ns/1.0"}
        self.ns_xml = {'xml': "http://www.w3.org/XML/1998/namespace"}
        self.file = file
        try:
            self.original = ET.parse(file)
        except:
            None
        try:
            self.tree = ET.parse(file)
        except:
            None
        try:
            self.parsed_file = ET.tostring(self.tree, encoding="utf-8")
        except:
            self.parsed_file = "parsing didn't work"

    def create_place(self, xml_id="something", text="someplace"):

        """ creates a tei:place element with an @xml:id and a child element tei:placeName"""

        place = ET.Element("place")
        place.attrib['{http://www.w3.org/XML/1998/namespace}id'] = xml_id
        placeName = ET.Element("placeName")
        placeName.text = text
        place.append(placeName)
        return place

    def get_places_elements(self, ids):

        """ takes a list of elements with a text node and a @ref attribute
        and returns a tei:placeList"""

        places = []
        for x in ids:
            text = x['text']
            ref = x['ref'][1:]
            place = (text, ref)
            places.append(place)
        place_elements = []
        for text, ref in set(places):
            place = self.create_place(ref, text)
            place_elements.append(place)
        return place_elements

    def find_elements(self, tei_element='placeName'):

        """ parses a tei:TEI//tei:text element,
        * extracts all nodes matching tei_element,
        * and reaturns a dictionary containing
        ** the name of the searched element: 'tei_element',
        ** the number of hits: 'nr_of_hits',
        ** and a list of the found element (as lxml element objects)
        """

        result = {'tei_element': tei_element}
        result['hits'] = self.tree.xpath(
            '//tei:text//tei:{}'.format(tei_element), namespaces=self.ns_tei
        )
        result['nr_of_hits'] = len(result['hits'])
        return result

    def add_ids(self, tei_element='placeName', id_prefix='some', export=False, export_file="updated"):

        """ reads an tei-xml document
        * looks for tei_elements,
        * adds generic @ref (hashed text-node),
        * and returns a tuple containing
        ** a list of elements,
        ** and the updated xml-tree object.
        """

        hits = self.find_elements(tei_element)['hits']
        ids = []
        for x in hits:
            if x.text is None:
                break
            try:
                x.attrib['ref']
                ids.append({'text': x.text, 'ref': x.attrib['ref'], 'node': x})
            except:
                ref = hashlib.md5(x.text.encode('utf-8')).hexdigest()
                x.attrib['ref'] = "#{}_{}".format(id_prefix, ref)
                ids.append({'text': x.text, 'ref': x.attrib['ref'], 'node': x})
        if export:
            file = "{}.xml".format(export_file)
            with open(file, 'wb') as f:
                f.write(ET.tostring(self.tree, pretty_print=True,encoding="UTF-8"))
        return ids, self.tree

    def create_index(self, nodes):

        """ takes a list of elements and transforms them into an index-file"""

        places = self.get_places_elements(nodes)
        list_place = ET.Element("listPlace")
        for x in places:
            list_place.append(x)
        new_doc = ET.fromstring(templates.tei_document)
        body = new_doc.xpath('//tei:body', namespaces=self.ns_tei)[0]
        body.append(list_place)
        return new_doc

    def export_tei(self, tei_doc, export_file='teihencer_export.xml'):

        """ writes any xml node to a file """

        file = export_file
        with open(file, 'wb') as f:
            f.write(ET.tostring(tei_doc, pretty_print=True, encoding="UTF-8"))
        return "file stored as {}".format(file)
