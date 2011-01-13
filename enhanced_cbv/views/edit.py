from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.forms.formsets import formset_factory, BaseFormSet, all_valid

from django.views.generic.base import View, TemplateResponseMixin


class EnhancedFormSet(object):
    """
    A base class for generic formsets
    """

    form_class = None
    formset_class = BaseFormSet

    # formset_factory kwargs
    extra = 3
    can_order = False
    can_delete = False
    max_num = None

    def get_formset(self, prefix=None, **kwargs):
        """
        Returns the instantiated formset
        """
        formset = self.get_factory()(**self.get_kwargs())
        return formset(prefix=prefix, **kwargs)

    def get_factory(self):
        """
        Returns the factory used to construct the formsets
        """
        return formset_factory

    def get_form_class(self):
        return self.form_class

    def get_formset_class(self):
        return self.formset_class

    def get_kwargs(self):
        return {'form': self.get_form_class(),
                'formset': self.get_formset_class(),
                'extra': self.extra,
                'can_order': self.can_order,
                'can_delete': self.can_delete,
                'max_num': self.max_num, }


class FormSetsMixin(object):
    """
    A mixin that provides a way to show and handle formsets
    """

    formsets = [] # must be a list of BaseGenericFormSet
    success_url = None

    def __init__(self, *args, **kwargs):
        self.instantiate_enhanced_formsets()

    def instantiate_enhanced_formsets(self):
        """
        Instantiates the enhanced formsets
        """
        self.enhanced_formsets_instances = []
        for formset in self.formsets:
            enhanced_formset_instance = formset()
            self.enhanced_formsets_instances.append(enhanced_formset_instance)

    def construct_formsets(self):
        """
        Constructs the formsets
        """
        kwargs = self.get_formsets_kwargs()

        self.formsets_instances = []

        prefixes = {}
        for enhanced_formset in self.enhanced_formsets_instances:
            prefix = enhanced_formset.get_formset_class().get_default_prefix()
            prefixes[prefix] = prefixes.get(prefix, 0) + 1
            if prefixes[prefix] != 1:
                prefix = "%s-%s" % (prefix, prefixes[prefix])
            self.formsets_instances.append(
                enhanced_formset.get_formset(prefix=prefix, **kwargs))

    def get_formsets_kwargs(self):
        """"
        Returns the keyword arguments for instanciating the formsets
        """

        # default kwargs
        kwargs = {}

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = {
            'formsets': [formset for formset in self.formsets_instances],
        }

        context_data.update(kwargs)
        return context_data

    def get_success_url(self):
        if self.success_url:
            url = self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url")
        return url

    def formsets_valid(self):
        return HttpResponseRedirect(self.get_success_url())

    def formsets_invalid(self):
        return self.render_to_response(self.get_context_data())


class ProcessFormSetsView(View):
    """
    A mixin that processes formsets on POST
    """
    def get(self, request, *args, **kwargs):
        self.construct_formsets()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.construct_formsets()
        if all_valid(self.formsets_instances):
            return self.formsets_valid()
        else:
            return self.formsets_invalid()

    def put(self, request, *args, **kwargs):
        return self.post(*args, **kwargs)


class BaseFormSetsView(FormSetsMixin, ProcessFormSetsView):
    """
    A base view for displaying formsets
    """


class FormSetsView(TemplateResponseMixin, BaseFormSetsView):
    """
    A view for displaying formsets, and rendering a template response
    """
