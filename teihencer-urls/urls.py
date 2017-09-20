from apis.urls import *

urlpatterns += url(r'teimporter/', include('teimporter.urls', namespace='teimporter'))
