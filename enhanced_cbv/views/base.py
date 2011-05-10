from django.views.generic.base import TemplateResponseMixin
from enhanced_cbv.response import PDFTemplateResponse

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
