from entities.models import *
from metainfo.models import *


def create_metatdata(user, some_form):
    current_user = user
    cd = some_form.cleaned_data
    super_collection, _ = Collection.objects.get_or_create(name='teihencer-all')
    current_group, _ = Group.objects.get_or_create(name=current_user.username)
    current_group.user_set.add(current_user)
    file = cd['file'].read()
    print(file)
    src, _ = Source.objects.get_or_create(orig_filename=cd['file'].name, author=current_user)
    kind, _ = TextType.objects.get_or_create(name='process tei:listPlace', entity='place')
    text, _ = Text.objects.get_or_create(text=file, source=src, kind=kind)
    if cd['new_sub_collection'] == "":
        col, _ = Collection.objects.get_or_create(
            name="{}".format(cd['collection'])
        )
        if col.parent_class is None:
            col.parent_class = super_collection
            col.save()
        else:
            pass
    else:
        parent_collection, _ = Collection.objects.get_or_create(
            name=cd['collection'],
            parent_class=super_collection
        )
        parent_collection.groups_allowed.add(current_group)
        parent_collection.save()
        col, _ = Collection.objects.get_or_create(
            name=cd['new_sub_collection'],
            parent_class=parent_collection,
        )
    col.groups_allowed.add(current_group)
    col.save()
    return {'col': col, 'src': src, 'text': text, 'file': file}
