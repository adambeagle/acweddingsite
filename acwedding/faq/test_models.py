from django.test import TestCase

from .models import Entry

class EntryTestCase(TestCase):
    def setUp(self):
        """
        Create entries with out-of-order ids to (attempt to) verify
        ordering not chronological by creation.
        """
        Entry.objects.create(
            id = 5,
            question = "Is this a test question?",
            answer = "Yes."
        )
        
        Entry.objects.create(
            id = 0,
            question = "Ever see a guy say goodbye to a shoe?",
            answer = "Yes, once."
        )
        
        Entry.objects.create(
            id = 3,
            question = "With what can you not win friends?",
            answer = "Salad."
        )
        
    def test_ordering(self):
        """Test that entries are returned in ascending order by id."""
        lastId = None
        
        for entry in Entry.objects.all():
            if lastId is None:
                lastId = entry.id
            else:
                self.assertTrue(entry.id > lastId)
    