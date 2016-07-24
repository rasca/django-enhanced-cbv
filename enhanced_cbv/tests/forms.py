from django import forms

from enhanced_cbv.views.edit import (EnhancedFormSet, EnhancedModelFormSet,
                                     EnhancedInlineFormSet)
from enhanced_cbv.tests.models import Article, Author


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'pub_date')



class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name', )


class ArticleEnhancedFormSet(EnhancedFormSet):
    form_class = ArticleForm
    fields = ('title', 'pub_date', 'author')



class AuthorEnhancedFormSet(EnhancedFormSet):
    form_class = AuthorForm
    fields = ('name', )



class ArticleEnhancedModelFormSet(EnhancedModelFormSet):
    model = Article
    fields = ('title', 'pub_date', 'author', )


class AuthorEnhancedModelFormSet(EnhancedModelFormSet):
    model = Author
    fields = ('name', )


class ArticleEnhancedInlineFormSet(EnhancedInlineFormSet):
    model = Article
    fields = ('title', 'pub_date', 'author', )
