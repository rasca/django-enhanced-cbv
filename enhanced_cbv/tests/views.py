from enhanced_cbv.views import FormSetsView

from enhanced_cbv.tests.forms import (ArticleEnhancedFormSet,
                                      AuthorEnhancedFormSet)


class AuthorsArticlesView(FormSetsView):
    formsets = [ArticleEnhancedFormSet, AuthorEnhancedFormSet]
    template_name = 'authors_articles.html'
    success_url = '/success/'
