from django import forms
from django.contrib.auth.models import Group
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
    collection = forms.ChoiceField(required=False)
    new_sub_collection = forms.CharField(required=False)
    enrich = forms.BooleanField(required=False)
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        collections = [Collection.objects.all()]
        self.user = kwargs.pop('user', None)
        CHOICES = [
            (self.user.username, self.user.username),
        ]
        groups = self.user.groups.exclude(name='superuser')
        collections = Collection.objects.filter(groups_allowed__in=groups)
        for x in collections:
            CHOICES.append((x.name, x.name))
        print(collections)
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['collection'].choices = set(CHOICES)
        self.fields['xpath'].initial = "rs[@type='place']"
        self.fields['enrich'].initial = False
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'import'),)


class UploadPlaceListForm(forms.Form):
    collection = forms.ChoiceField(required=False)
    new_sub_collection = forms.CharField(required=False)
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        collections = [Collection.objects.all()]
        self.user = kwargs.pop('user', None)
        CHOICES = [
            (self.user.username, self.user.username),
        ]
        groups = self.user.groups.exclude(name='superuser')
        collections = Collection.objects.filter(groups_allowed__in=groups)
        for x in collections:
            CHOICES.append((x.name, x.name))
        print(collections)
        super(UploadPlaceListForm, self).__init__(*args, **kwargs)
        self.fields['collection'].choices = set(CHOICES)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'import'),)
