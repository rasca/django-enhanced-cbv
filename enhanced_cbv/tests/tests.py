from django.test import TestCase
from enhanced_cbv.views.edit import FormSetsMixin

class FormSetsViewTests(TestCase):
    urls = 'enhanced_cbv.tests.urls'

    def setUp(self):
        self.data = {
            'form-TOTAL_FORMS': u'3',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-title': u'',
            'form-0-pub_date': u'',
            'form-1-title': u'',
            'form-1-pub_date': u'',
            'form-2-title': u'',
            'form-2-pub_date': u'',

            'form-2-TOTAL_FORMS': u'3',
            'form-2-INITIAL_FORMS': u'0',
            'form-2-MAX_NUM_FORMS': u'',
            'form-2-0-name': u'',
            'form-2-1-name': u'',
            'form-2-2-name': u'',
        }

    def test_get(self):
        response = self.client.get('/edit/formsets/')
        self.assertEqual(response.status_code, 200)

    def test_empty_post(self):
        response = self.client.post('/edit/formsets/', self.data)
        self.assertEqual(response.status_code, 302)

    def test_valid(self):
        self.data.update({
            'form-0-title': u'first title',
            'form-0-pub_date': u'2011-01-13',
            'form-1-title': u'second title',
            'form-1-pub_date': u'2011-01-13',
            'form-2-0-name': u'this is my name',
        })
        response = self.client.post('/edit/formsets/', self.data)
        self.assertEqual(response.status_code, 302)

    def test_invalid(self):
        self.data.update({
            'form-0-title': u'first title',
            'form-0-pub_date': u'',
        })
        response = self.client.post('/edit/formsets/', self.data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ERROR')

