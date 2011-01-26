from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.forms.formsets import formset_factory, BaseFormSet, all_valid
from django.forms.models import (modelformset_factory, inlineformset_factory,
                                 BaseModelFormSet, BaseInlineFormSet, ModelForm)

from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin


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

    def get_base_formset(self, **kwargs):
        """
        Returns the base formset
        """
        kwargs.update(self.get_kwargs())
        return self.get_factory()(**kwargs)

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


class EnhancedModelFormSet(EnhancedFormSet):
    """
    A base class for generic model formsets
    """
    # TODO: provide a hook for formfield_callback

    form_class = ModelForm
    formset_class = BaseModelFormSet
    model = None
    queryset = None
    fields = None
    exclude = None

    def get_factory(self):
        return modelformset_factory

    def get_model(self):
        if self.model:
            return self.model
        else:
            raise ImproperlyConfigured(
                "No model to create the modelformset. Provide one.")

    def get_queryset(self):
        return self.queryset

    def get_fields(self):
        return self.fields

    def get_exclude(self):
        return self.exclude

    def get_kwargs(self):
        kwargs = super(EnhancedModelFormSet, self).get_kwargs()
        kwargs.update({
            'model': self.get_model(),
            'fields': self.get_fields(),
            'exclude': self.get_exclude(),
        })
        return kwargs


class EnhancedInlineFormSet(EnhancedModelFormSet):
    """
    A base class for generic inline formsets
    """

    fk_name = None
    formset_class = BaseInlineFormSet

    def get_factory(self):
        return inlineformset_factory

    def get_fk_name(self):
        return self.fk_name

    def get_kwargs(self):
        kwargs = super(EnhancedInlineFormSet, self).get_kwargs()
        kwargs.update({
            'fk_name': self.get_fk_name(),
        })
        return kwargs


class FormSetsMixin(object):
    """
    A mixin that provides a way to show and handle formsets
    """

    formsets = []  # must be a list of BaseGenericFormSet
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
        self.formsets_instances = []

        prefixes = {}
        for enhanced_formset in self.enhanced_formsets_instances:
            base_formset = enhanced_formset.get_base_formset(
                **self.get_factory_kwargs())

            # calculate prefix
            prefix = base_formset.get_default_prefix()
            prefixes[prefix] = prefixes.get(prefix, 0) + 1
            if prefixes[prefix] != 1:
                prefix = "%s-%s" % (prefix, prefixes[prefix])

            self.formsets_instances.append(
                base_formset(prefix=prefix, **self.get_formsets_kwargs(
                    enhanced_formset))
            )

    def get_factory_kwargs(self):
        """
        Returns the keyword arguments for the formsets factory
        """
        return {}

    def get_formsets_kwargs(self, enhanced_formset):
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


class ModelFormSetsMixin(FormSetsMixin):
    """
    A mixin that provides a way to show and handle model formsets
    """

    def get_formsets_kwargs(self, enhanced_formset):
        """"
        Returns the keyword arguments for instanciating the model formsets
        """
        kwargs = super(ModelFormSetsMixin, self).get_formsets_kwargs(
                                                    enhanced_formset)
        kwargs.update({
            'queryset': enhanced_formset.get_queryset()
        })
        return kwargs

    def formsets_valid(self):
        # FIXME: beware of m2m
        for formset in self.formsets_instances:
            formset.save()
        return super(ModelFormSetsMixin, self).formsets_valid()


class InlineFormSetsMixin(ModelFormSetsMixin, ModelFormMixin):
    """ 
    A mixin that provides a way to show and handle a model with it's inline
    formsets
    """
    def get_formsets_kwargs(self, enhanced_formset):
        """"
        Returns the keyword arguments for instanciating the inline formsets
        """
        kwargs = super(InlineFormSetsMixin, self).get_formsets_kwargs(
                                                    enhanced_formset)
        kwargs.update({
            'instance': self.object
        })
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Adds the context data from both parents
        """
        context_data = ModelFormSetsMixin.get_context_data(self)
        context_data.update(ModelFormMixin.get_context_data(self, **kwargs))
        # print context_data['formsets'][0]
        return context_data

    def get_factory_kwargs(self):
        """
        Returns the keyword arguments for the formsets factory
        """
        return {
            'parent_model': self.object.__class__,
        }


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


class ProcessInlineFormSetsView(View):
    """
    A mixin that processes a model instance and it's inline formsets on POST
    """

    def get(self, request, *args, **kwargs):
        # Create or Update
        try:
            self.object = self.get_object()
        except AttributeError:
            self.object = self.model()

        # ProcessFormView
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # ProcessFormSetsView
        self.construct_formsets()

        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        # Create or Update
        try:
            self.object = self.get_object()
        except AttributeError:
            self.object = self.model()

        # ProcessFormView
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            self.object = form.save(commit=False)

            # ProcessFormSetsViewV
            self.construct_formsets()

            if all_valid(self.formsets_instances):
                self.object.save()
                form.save_m2m()
                for formset in self.formsets_instances:
                    formset.save()

                return HttpResponseRedirect(self.get_success_url())
        else:
            # ProcessFormSetsViewV
            self.construct_formsets()
        return self.render_to_response(self.get_context_data(form=form))


    def put(self, request, *args, **kwargs):
        return self.post(*args, **kwargs)


class BaseFormSetsView(FormSetsMixin, ProcessFormSetsView):
    """
    A base view for displaying formsets
    """


class BaseModelFormSetsView(ModelFormSetsMixin, ProcessFormSetsView):
    """
    A base view for displaying model formsets
    """


class BaseInlineFormSetsView(InlineFormSetsMixin, ProcessInlineFormSetsView):
    """
    A base view for displaying a model instance with it's inline formsets
    """


class FormSetsView(TemplateResponseMixin, BaseFormSetsView):
    """
    A view for displaying formsets, and rendering a template response
    """


class ModelFormSetsView(TemplateResponseMixin, BaseModelFormSetsView):
    """
    A view for displaying model formsets, and rendering a template response
    """



class InlineFormSetsView(SingleObjectTemplateResponseMixin,
                         BaseInlineFormSetsView):
    """
    A view for displaying a model instance with it's inline formsets, and
    rendering a template response
    """
    template_name_suffix = '_form'
