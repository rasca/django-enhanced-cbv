from django import forms

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
        fields = ('name', )


class ArticleEnhancedFormSet(EnhancedFormSet):
    form_class = ArticleForm


class AuthorEnhancedFormSet(EnhancedFormSet):
    form_class = AuthorForm


class ArticleEnhancedModelFormSet(EnhancedModelFormSet):
    model = Article
    fields = ('title', 'pub_date', 'author', )


class AuthorEnhancedModelFormSet(EnhancedModelFormSet):
    model = Author
    fields = ('name', )


class ArticleEnhancedInlineFormSet(EnhancedInlineFormSet):
    model = Article
    fields = ('title', 'pub_date', 'author', )
