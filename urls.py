from django.conf.urls.defaults import *

from beijing_air import views

urlpatterns = patterns('',
    url(r'^$',
        views.index,
        name="beijingair_index"
        ),
    
    url(r'^data.txt$',
        views.timeplot_csv,
        name="beijingair_timeplot_csv"
        ),
)