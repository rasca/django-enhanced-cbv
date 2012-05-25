from django.views.generic.base import TemplateResponseMixin
from enhanced_cbv.response import PDFTemplateResponse, CSVTemplateResponse

class PDFTemplateResponseMixin(TemplateResponseMixin):
    """
    Extends the TemplateResponseMixin with a filename for render_to_response
    """

    response_class = PDFTemplateResponse
    filename = None

    def get_filename(self):
        if self.filename is None:
            raise ImproperlyConfigured(
                "PDFTemplateResponseMixin requires either a definition of "
                "'filename' or an implementation of 'get_filename()'")
        else:
            return self.filename

    def render_to_response(self, *args, **kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        kwargs.update({'filename': self.get_filename()})
        return super(PDFTemplateResponseMixin, self).render_to_response(*args, **kwargs)


class CSVTemplateResponseMixin(TemplateResponseMixin):
    """
    Extends the TemplateResponseMixin with a filename for render_to_response
    """

    response_class = CSVTemplateResponse
    filename = None
    writer_kwargs = None

    def get_filename(self):
        if self.filename is None:
            raise ImproperlyConfigured(
                "PDFTemplateResponseMixin requires either a definition of "
                "'filename' or an implementation of 'get_filename()'")
        else:
            return self.filename

    def get_writer_kwargs(self):
        return self.writer_kwargs

    def render_to_response(self, *args, **kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        rows = [self.get_header()]
        for obj in self.get_queryset():
            rows.append(self.get_row(obj))
        kwargs.update({
            'rows': rows,
            'filename': self.get_filename(),
            'writer_kwargs': self.get_writer_kwargs(),
        })
        return super(CSVTemplateResponseMixin, self).render_to_response(*args, **kwargs)

    def get_header(self):
        """Must return a list of strings for the header"""
        return NotImplementedError

    def get_row(self, obj):
        """Must return a list of strings for a row"""
        return NotImplementedError
