from django import forms
from django.forms.formsets import formset_factory

from enhanced_cbv.views.edit import EnhancedFormSet


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField(required=True)

class AuthorForm(forms.Form):
    name = forms.CharField()

class ArticleEnhancedFormSet(EnhancedFormSet):
    form_class = ArticleForm

class AuthorEnhancedFormSet(EnhancedFormSet):
    form_class = AuthorForm
