# teihencer

an [APIS](https://apis.acdh.oeaw.ac.at) based application to enhance TEI documents (therefore this hilarious project name)

We are currently updating the code base.

## installation

1. clone the repo `git clone https://github.com/acdh-oeaw/teihencer.git`
2. init apis-submodule `git submodule update --init`
3. create symbolic links from `teihencer-teimporter`, `teihencer-webapp`, and `teihencer-urls` to `apis-core/teimporter`, `apis-core/webpage` and `apis-core/custom_urls` (on windows use  `mklink /d webpage ..\teihencer-webapp`)
4. create symbolic link from `teihencer-settings` to `apis-core/apis/settings`
5. Make migrations `python manage.py makemigrations entities highlighter labels metainfo relations vocabularies webpage --settings=apis.settings.dev`

## set up (merely for internal development)

1. create a git repo e.g. 'teihencer'
2. `cd teihencer`
3. `git submodule add https://github.com/acdh-oeaw/apis-core.git`

now your root directory should contain a directory called *apis-core*, and a *.gitmodules* file.

1. create a webpage application (or copy it from somewhere else) in the root directory and name it e.g teihencer-webapp
2. after this, you need to link from `apis-core/apis` to your webpage application directory. This can be achieved with a symbolic link. To create such a link on windows, type `mklink /d webpage ..\teihencer-webapp`
3. now you need to create a virtual environment and install needed packages (on windows this can be bit cumerbosome because you might have to download precompiled packages first)
4. after you env is set up, you have to create migraion files `python manage.py makemigrations entities highlighter labels metainfo relations vocabularies webpage --settings=apis.settings.dev` make sure to do this for all apps in your project

python manage.py makemigrations entities highlighter labels metainfo relations vocabularies webpage --settings=apis.settings.dev

# Workflow

## Registration (not yet implemented)

A user account is needed for managing the data created/curated/published by users.

* simple form with username, password (to decide if also email)
* A group {username} is created.
* The user {username} is linked to group {username}
* A collection {username} is created. This collection {username} has a parent collection {teihencer-all}
* The {username}-collection is related to group {user-name} and all CRUD rights for this collection given to user {username}

## Upload/Process

* user needs to be logged in
* user can upload 1-n TEI-Document(s)
* upload form requests the name of a {current-upload}-collection
** this collection can already exist (select from list)
** or this collection will be created
* anyway this collection always has a `parent_collection` the {username}-collection.
* derived entities from the uploaded document(s) will be related to {current-upload}-collection
* derived entities from the uploaded document(s) will be related to source-objects which will be created on the fly, with names taken from uploaded/processed files

# Use cases

## place entities tagged but not linked to any index

You have 1:n TEI files which are semantically annotated in a sense that place like entities a tagged like e.g. `<tei:placeName/>` or `<tei:rs[@type='place']/>`. But those elements are not in any way linked to an index like a `<listPlace>`. If so, you can upload you file and *TEIHencer* will

* add `@ref` attributes to those entities. The attribute values are md5 hashes derieved from the elements text nodes. This ensures that entities with the same text-nodes share the same `@ref`-value.
* *TEIHencer* takes the text-nodes and reconciles them against [geonames.org](http://www.geonames.org/). It tries to find matches and stores those matches in a specific collection, which can then be manually post processed/curated in a graphical user interface.
* After this curation process, the enhanced and curated place objects can be exported as TEI document.

## enrich an existing place index (`<tei:listPlace/>`)

You have already one place index but the entries are not linked to geonames (or [GND](https://portal.dnb.de)) but you want to enhance your index with information (IDs, coordinates, ...) findable on [geonames.org](http://www.geonames.org/).
To do so you can

* Upload your TEI document containing the place index.
* *TEIHencer* will parse this document and store as much information as possible (e.g. alternative placenames, place types) in it's database.
* *TEIHencer* will reconcile all parsed entities against [geonames.org](http://www.geonames.org/). It tries to find matches and stores those matches in a specific collection, which can then be manually post processed/curated in a graphical user interface.
* After this curation process, the enhanced and curated can be exported as TEI document.

# Limitations:

Geonames-API allows 2000 requests per IP per hour.
