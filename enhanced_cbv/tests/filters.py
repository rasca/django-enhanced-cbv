import django_filters

from enhanced_cbv.tests.models import Author

class AuthorFilterSet(django_filters.FilterSet):
    class Meta:
        model = Author
        fields = ['name', ]
