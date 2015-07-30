from django.conf.urls import url

from enhanced_cbv.tests.views import (
    AuthorsArticlesView, AuthorsArticlesModelsView, AuthorsInlinesView,
    AuthorsListFilteredView, ArticleExport)


urlpatterns = [
    # FormSetsView
    url(r'^edit/formsets/$', AuthorsArticlesView.as_view()),
    url(r'^edit/modelformsets/$', AuthorsArticlesModelsView.as_view()),
    url(r'^edit/inlineformsets/$', AuthorsInlinesView.as_view()),
    url(r'^edit/inlineformsets/(?P<pk>\d)/$', AuthorsInlinesView.as_view()),
    url(r'^list/filtered/$', AuthorsListFilteredView.as_view()),
    url(r'^list/export/$', ArticleExport.as_view())
]
