try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO  # noqa

import django
from django.template.response import TemplateResponse

from enhanced_cbv.utils import fetch_resources, UnicodeWriter


class PDFTemplateResponse(TemplateResponse):

    # The following is needed due to an error un pisa (pdf generation)
    # It must be executed once at startup
    #
    # TODO: Check if this still happends in xhtml2pdf (the most up-to-date
    # version of pisa was renamed). Otherwise, report it to
    # https://github.com/chrisglass/xhtml2pdf

    import logging

    class PisaNullHandler(logging.Handler):
        def emit(self, record):
            pass
    logging.getLogger("ho.pisa").addHandler(PisaNullHandler())

    def __init__(self, request, template, context=None,
                 content_type='application/pdf', status=None, current_app=None,
                 charset=None, using=None, filename=None):
        """Simple adds a default mimetype for PDFs and a filename"""

        self.filename = filename

        if django.VERSION < (1, 8):
            super(PDFTemplateResponse, self).__init__(request,
                template, context, content_type, status, using)
        else:
            super(PDFTemplateResponse, self).__init__(request,
                template, context, content_type, status, charset, using)

    def render(self):
        """This is the tricky part, whith the rendered_content create a PDF"""

        # The following is required for PDF generation

        import xhtml2pdf.pisa as pisa  # The import is changed to xhtml2pdf

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


class CSVTemplateResponse(TemplateResponse):

    def __init__(self, request, template, context=None,
                 content_type='text/csv', status=None,
                 current_app=None, charset=None, using=None, filename=None,
                 rows=None, writer_kwargs=None):
        """Simple adds a default mimetype for CSVs and a filename"""

        self.filename = filename
        self.rows = rows
        if writer_kwargs:
            self.writer_kwargs = writer_kwargs
        else:
            self.writer_kwargs = {}

        if django.VERSION < (1, 8):
            super(CSVTemplateResponse, self).__init__(request,
                template, context, content_type, status, using)
        else:
            super(CSVTemplateResponse, self).__init__(request,
                template, context, content_type, status, charset, using)

    def render(self):
        """This is the tricky part, whith the rendered_content create a CSV"""

        if not self._is_rendered:

            # File pointer needed to create the CSV in memory
            buffer = StringIO()
            writer = UnicodeWriter(buffer, **self.writer_kwargs)

            for row in self.rows:
                writer.writerow([unicode(value).encode('utf-8') for value
                                 in row])

            # Get the value of the StringIO buffer and write it to the response.
            csv = buffer.getvalue()
            buffer.close()
            self.write(csv)

            # Sets the appropriate CSV headers.
            self['Content-Disposition'] = 'attachment; filename=%s' % (
                self.filename, )

            # The CSV has been generated
            self._is_rendered = True

            for post_callback in self._post_render_callbacks:
                post_callback(self)
        return self
