# teihencer

an [APIS](https://apis.acdh.oeaw.ac.at) based application to enhance TEI documents (therefore this hilarious project name)

## set up

1. create a git repo e.g. 'teihencer'
2. `cd teihencer`
3. `git submodule add https://redmine.acdh.oeaw.ac.at/apis-core.git`

now your root directory should contain a directory called *apis-core*, and a *.gitmodules* file.

1. create a webpage application (or copy it from somewhere else) in the root directory and name it e.g teihencer-webapp
2. after this, you need to link from `apis-core/apis` to your webpage application directory. This can be achieved with a symbolic link. To create such a link on windows, type `mklink /d webpage ..\teihencer-webapp`
3. now you need to create a virtual environment and install needed packages (on windows this can be bit cumerbosome because you might have to download precompiled packages first)
4. after you env is set up, you have to create migraion files `python manage.py makemigrations entities highlighter labels metainfo relations vocabularies webpage --settings=apis.settings.dev` make sure to do this for all apps in your project


python manage.py makemigrations entities highlighter labels metainfo relations vocabularies webpage --settings=apis.settings.dev
