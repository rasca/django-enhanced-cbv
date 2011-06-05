from enhanced_cbv.views import (FormSetsView, ModelFormSetsView,
                                InlineFormSetsView, ListFilteredView, )

from enhanced_cbv.tests.forms import (
    ArticleEnhancedFormSet, AuthorEnhancedFormSet,
    ArticleEnhancedModelFormSet, AuthorEnhancedModelFormSet,
    ArticleEnhancedInlineFormSet
)
from enhanced_cbv.tests.models import Author
from enhanced_cbv.tests.filters import AuthorFilterSet


class AuthorsArticlesView(FormSetsView):
    formsets = [ArticleEnhancedFormSet, AuthorEnhancedFormSet]
    template_name = 'authors_articles.html'
    success_url = '/success/'
    

class AuthorsArticlesModelsView(ModelFormSetsView):
    formsets = [ArticleEnhancedModelFormSet, AuthorEnhancedModelFormSet]
    template_name = 'authors_articles.html'
    success_url = '/success/'


class AuthorsInlinesView(InlineFormSetsView):
    formsets = [ArticleEnhancedInlineFormSet,]
    template_name = 'authors_articles.html'
    success_url = '/success/'
    model = Author


class AuthorsListFilteredView(ListFilteredView):
    model = Author
    filter_set = AuthorFilterSet
    template_name = 'authors_list.html'
