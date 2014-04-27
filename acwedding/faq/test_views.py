from django.test import TestCase

class ViewTestCase(TestCase):
    
    def test_index(self):
        response = self.client.get('/faq/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('days_remaining', response.context)