from django.db import connection
from django.test import TestCase

class DetailViewTestCase(TestCase):
    fixtures = ['core_views_testdata.json']
    
    def test_landing_page(self):
        """Test redirect to /welcome/ from root url."""
        self.assertRedirects(self.client.get('/'), '/welcome/', 
            status_code=301)
        
        response = self.client.get('/', follow=True)
        self.assertIn('days_remaining', response.context)
        
    def test_db_hits(self):
        """
        Requesting the landing page should entail 3 DB queries:
          1) Get the Page object via pk
          2) Get each Section and its related Minigallery and Map objects.
          3) Get the SubheaderImage with a reference to the page's pk
        """
        connection.use_debug_cursor = True
        connection.queries = []
        
        with self.assertNumQueries(3):
            self.client.get('/', follow=True)
                
        connection.use_debug_cursor = False