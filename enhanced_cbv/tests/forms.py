from django import forms
from django.forms.formsets import formset_factory

from enhanced_cbv.views.edit import (EnhancedFormSet, EnhancedModelFormSet,
                                     EnhancedInlineFormSet)
from enhanced_cbv.tests.models import Article, Author


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('author', )

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author

class ArticleEnhancedFormSet(EnhancedFormSet):
    form_class = ArticleForm

class AuthorEnhancedFormSet(EnhancedFormSet):
    form_class = AuthorForm

class ArticleEnhancedModelFormSet(EnhancedModelFormSet):
    model = Article

class AuthorEnhancedModelFormSet(EnhancedModelFormSet):
    model = Author

class ArticleEnhancedInlineFormSet(EnhancedInlineFormSet):
    model = Article
