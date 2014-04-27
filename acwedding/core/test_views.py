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
        
    def test_db_hits_simple(self):
        """
        Requesting the landing page should entail 3 DB queries:
          1) Get the Page object via pk
          2) Get each Section and its related Minigallery and Map objects.
          3) Get the SubheaderImage with a reference to the page's pk
        """
        with self.assertNumQueries(3):
            self.client.get('/', follow=True)
                
    
    def test_db_hits_with_minigallery(self):
        """
        Pages with a MiniGallery should entail the 'simple' DB queries plus
        one for each iteration through the images (thumbnails and full-size).
        """
        with self.assertNumQueries(5):
            self.client.get('/engagement/')
