# teihencer

an [APIS](https://apis.acdh.oeaw.ac.at) based application to enhance TEI documents (therefore this hilarious project name)

## set up

1. create a git repo e.g. 'teihencer'
2. `cd teihencer`
3. `git submodule add https://redmine.acdh.oeaw.ac.at/apis-core.git`

now your root directory should contain a directory called *apis-core*, and a *.gitmodules* file.

create a webpage application (or copy it from somewhere else)

after this, you need to link form apis-core/apis to your webpage application directory. This can be acchived with a symbolic link. To create such a link on windows, type

mklink /d C:\Users\pandorfer\ownCloud\GIT\Redmine\teihencer\apis-core\webpage ..\teihencer-webpage
