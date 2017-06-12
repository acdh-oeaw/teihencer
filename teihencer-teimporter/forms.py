from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from metainfo.models import Collection

XPATH_CHOICES = (
    ('placeName', 'placeName'),
    ('country', 'country'),
    ("rs[@type='place']", "rs[@type='place']"),
)


class GenericFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(GenericFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.add_input(Submit('Filter', 'search'))


class UploadFileForm(forms.Form):
    xpath = forms.ChoiceField(choices=XPATH_CHOICES, required=True)
    collection = forms.CharField(required=False)
    new_collection = forms.CharField(required=False)
    enrich = forms.BooleanField(required=False)
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)

        def get_choices():
            collection = [('', '')]
            collection = collection + [(x.name, x.name) for x in Collection.objects.all()]
            return collection

        self.fields['collection'] = forms.ChoiceField(choices=get_choices(), required=False)
        self.fields['collection'].initial = ''
        self.fields['xpath'].initial = "rs[@type='place']"
        self.fields['enrich'].initial = False
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'import'),)
