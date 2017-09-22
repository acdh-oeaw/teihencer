from entities.views import PlaceListView


class TeiPlaceListView(PlaceListView):

    def get_template_names(self):
        return 'teimporter/places_tei.html'
