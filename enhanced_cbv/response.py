from django.template.response import TemplateResponse
from enhanced_cbv.utils import fetch_resources

class PDFTemplateResponse(TemplateResponse):

    # The following is needed due to an error un pisa (pdf generation)
    # It must be executed once at startup
    import logging
    class PisaNullHandler(logging.Handler):
        def emit(self, record):
            pass
    logging.getLogger("ho.pisa").addHandler(PisaNullHandler())

    def __init__(self, request, template, context=None,
                 mimetype='application/pdf', status=None, content_type=None,
                 current_app=None, filename=None):
        """Simple adds a default mimetype for PDFs and a filename"""

        self.filename = filename

        super(PDFTemplateResponse, self).__init__(request,
            template, context, mimetype, status, content_type)

    def render(self):
        """This is the tricky part, whith the rendered_content create a PDF"""

        # The following is required for PDF generation

        try:
            from cStringIO import StringIO
        except ImportError:
            from StringIO import StringIO
        import ho.pisa as pisa

        if not self._is_rendered:

            # File pointer needed to create the PDF in memory
            buffer = StringIO()

            # Create the PDF object, using the StringIO object as its "file."
            pisa.CreatePDF(self.rendered_content, buffer,
                           link_callback=fetch_resources)

            # Get the value of the StringIO buffer and write it to the response.
            pdf = buffer.getvalue()
            buffer.close()
            self.write(pdf)

            # Sets the appropriate PDF headers.
            self['Content-Disposition'] = 'attachment; filename=%s' % (
                self.filename, )

            # The PDF has been rendered
            self._is_rendered = True

            for post_callback in self._post_render_callbacks:
                post_callback(self)
        return self
