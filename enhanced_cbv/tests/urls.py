from django.conf.urls.defaults import *

from enhanced_cbv.tests.views import AuthorsArticlesView


urlpatterns = patterns('',

    # FormSetsView
    (r'^edit/formsets/$',
        AuthorsArticlesView.as_view()),
)
