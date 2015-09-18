from django.views.generic import TemplateView

from enhanced_cbv.views import (FormSetsView, ModelFormSetsView,
                                InlineFormSetsView, ListFilteredView, )
from enhanced_cbv.views.base import CSVTemplateResponseMixin
from enhanced_cbv.tests.forms import (
    ArticleEnhancedFormSet, AuthorEnhancedFormSet,
    ArticleEnhancedModelFormSet, AuthorEnhancedModelFormSet,
    ArticleEnhancedInlineFormSet
)
from enhanced_cbv.tests.models import Author, Article
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
    formsets = [ArticleEnhancedInlineFormSet, ]
    template_name = 'authors_articles.html'
    success_url = '/success/'
    model = Author
    fields = ('name', )

    def get_context_data(self, **kwargs):
        context = super(AuthorsInlinesView, self).get_context_data(**kwargs)
        context['new_object'] = self.new_object
        return context


class AuthorsListFilteredView(ListFilteredView):
    model = Author
    filter_set = AuthorFilterSet
    template_name = 'authors_list.html'


class ArticleExport(CSVTemplateResponseMixin, TemplateView):
    model = Article
    template_name = 'dummy.html'
    filename = 'article_all.csv'
    fields = ('title', 'pub_date', 'author', )

    def get_queryset(self):
        return Article.objects.all()

    def get_header(self):
        return ['Title', 'Published date', 'Author', ]

    def get_row(self, obj):
        row = []
        for field in self.fields:
            try:
                row.append(getattr(obj, 'get_%s_display' % field)() or u'')
            except AttributeError:
                row.append(getattr(obj, field) or u'')
        return row
