from enhanced_cbv.views import (FormSetsView, ModelFormSetsView,
                                InlineFormSetsView)

from enhanced_cbv.tests.forms import (
    ArticleEnhancedFormSet, AuthorEnhancedFormSet,
    ArticleEnhancedModelFormSet, AuthorEnhancedModelFormSet,
    ArticleEnhancedInlineFormSet
)
from enhanced_cbv.tests.models import Author


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
