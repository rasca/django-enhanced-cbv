from enhanced_cbv.views import FormSetsView, ModelFormSetsView

from enhanced_cbv.tests.forms import (
    ArticleEnhancedFormSet, AuthorEnhancedFormSet,
    ArticleEnhancedModelFormSet, AuthorEnhancedModelFormSet,
)


class AuthorsArticlesView(FormSetsView):
    formsets = [ArticleEnhancedFormSet, AuthorEnhancedFormSet]
    template_name = 'authors_articles.html'
    success_url = '/success/'
    

class AuthorsArticlesModelsView(ModelFormSetsView):
    formsets = [ArticleEnhancedModelFormSet, AuthorEnhancedModelFormSet]
    template_name = 'authors_articles.html'
    success_url = '/success/'
