import re

from django.test import TestCase
from django.utils.html import linebreaks

from core.util import field_list_pattern, url_block_pattern
from .templatetags.core_tags import rst_to_table
    
def _re_match(pattern, s, flags=0):
    """
    Helper function for tests. Return either the full match via 
    re.MatchObject.group() or None if there was no match.
    
    'flags' is passed to re.search().
    """
    match = re.search(pattern, s, flags)
    
    if match is None:
        return None
    else:
        return match.group()

class FieldRegexTestCase(TestCase):
    """Test the field_list_pattern regular expression."""
    
    def test_almost(self):
        """Verify strings that are nearly matches fail to match."""
        p = field_list_pattern
        
        self.assertIsNone(_re_match(p, ':: text'))
        self.assertIsNone(_re_match(p, ':not a heading:'))
        self.assertIsNone(_re_match(p, 'Lorem :heading: text'))
        
    def test_basic(self):
        """Verify simple, properly formatted blocks are matched."""
        p = field_list_pattern
        
        self.assertEqual(_re_match(p, ':head: \ttext\n'), ':head: \ttext')
        self.assertEqual(_re_match(p, ':*: text\n'), ':*: text')
        self.assertEqual(_re_match(p, 'Lorem\n:head: text', re.M), 
            ':head: text')
        self.assertEqual(_re_match(p, 'Lorem\n\n:head: text', re.M), 
            ':head: text')
        self.assertEqual(_re_match(p, ':head: word 1@#<>. '), 
            ':head: word 1@#<>. ')
        self.assertEqual(_re_match(p, ':head: text\n'), ':head: text')
        self.assertEqual(_re_match(p, ':head: text\n'), ':head: text')
        
    def test_escaped_colon(self):
        """Verify an escaped colon within the heading is ignored."""
        p = field_list_pattern
        
        self.assertEqual(_re_match(p, r':A\: heading: text'), 
            r':A\: heading: text')
        
    def test_groups(self):
        """
        Verify re.MatchObject.group(x) returns correct values.
        group(1) should return the between-colons portion.
        group(2) should return the rest of the line (not including the
        closing colon.
        """
        p = field_list_pattern
        
        m = re.search(p, '\n\n:A heading: \tSome text\n\n', re.M)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), 'A heading')
        self.assertEqual(m.group(2), 'Some text')
        
        m = re.search(p, ':heading::text : with : colons')
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), 'heading')
        self.assertEqual(m.group(2), ':text : with : colons')
        
        m = re.search(p, ':*: text')
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), '*')
        self.assertEqual(m.group(2), 'text')
    
    def test_post_linebreaks(self):
        """
        Verify <p> and <br> tags are correctly detected. If linebreaks was 
        used prior to this filter, the block may be wrapped in <p> tags.
        """
        p = field_list_pattern
        
        postLB = linebreaks(':head: text')
        self.assertEqual(_re_match(p, postLB), '<p>:head: text</p>')
        
        postLB = linebreaks('Lorem ipsum.\n\n:head: text\n\nDolor sit.')
        self.assertEqual(_re_match(p, postLB, re.M), '<p>:head: text</p>')
        
class FiltersTestCase(TestCase):
    """Test this app's custom filters."""
    
    def test_rsttotable(self):
        long = ('This is a paragraph.\n\n' + 
            ':Heading: Some text \n' +
            ':Heading 2: More text\n\n' +
            'This is another paragraph.')

        long_tabled = ('This is a paragraph.\n\n' +
            '<table class="table"><tr><td>Heading:</td><td>Some text </td></tr>' + 
            '<tr><td>Heading 2:</td><td>More text</td></tr></table>\n' +
            'This is another paragraph.')
            
        long_tabled_linebreaks = ('<p>This is a paragraph</p>' +
            '<table class="table"><tr><td>Heading:</td><td>Some text </td></tr>' + 
            '<tr><td>Heading 2:</td><td>More text</td></tr></table>\n' +
            '<p>This is another paragraph.</p>')
            
        simple = ':h1: text\n:h2: text2'
        simple_tabled = ('<table class="table"><tr><td>h1:</td><td>text</td></tr>' +
            '<tr><td>h2:</td><td>text2</td></tr></table>')
        
        self.assertEqual(rst_to_table(simple), simple_tabled)
        self.assertEqual(rst_to_table(long), long_tabled)
    
class URLRegexTestCase(TestCase):
    """Test the url_block_pattern regular expression"""
    
    def test_description(self):
        """Test the between-brackets text."""
        p = url_block_pattern
        
        self.assertEqual(_re_match(p, '[one two](page)'), '[one two](page)')
        self.assertEqual(_re_match(p, r'[[text\]](page)'), r'[[text\]](page)')
        self.assertEqual(_re_match(p, r'[/.,\':\\+=-_<>](page)'), 
            r'[/.,\':\\+=-_<>](page)')
    
    def test_formats(self):
        """Verify reversable formats are all matches."""
        p = url_block_pattern
        
        self.assertEqual(_re_match(p, '[text](app:page)'),
            '[text](app:page)')
        self.assertEqual(_re_match(p, '[text](page pk)'), 
            '[text](page pk)')
        self.assertEqual(_re_match(p, '[text](page a1 a2)'), 
            '[text](page a1 a2)')
        self.assertEqual(_re_match(p, '[text](app:page pk)'), 
            '[text](app:page pk)')
        self.assertEqual(_re_match(p, '[text](app:page a1 a2)'), 
            '[text](app:page a1 a2)')
        
    def test_groups(self):
        """
        Verify match groups. group(1) should be description, group(2) should 
        be args to reverse.
        """
        p = url_block_pattern
        
        m = re.search(p, r'[[text\]](app:page a1 a2)')
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), r'[text\]')
        self.assertEqual(m.group(2), 'app:page a1 a2')
        
    
    def test_placement(self):
        """Test various placements of the url block within a string."""
        p = url_block_pattern
        
        self.assertEqual(_re_match(p, '[text](page)'), '[text](page)')
        self.assertEqual(_re_match(p, 'Lorem [text](page) ipsum.'),
            '[text](page)')
        self.assertEqual(_re_match(p, 'Lorem ipsum [text.](page)'), 
            '[text.](page)')
        self.assertEqual(_re_match(p, '[Text](page) lorem ipsum.'), 
            '[Text](page)')
            
        self.assertEqual(_re_match(p, 'Lorem\n[text](page)\nipsum'),
            '[text](page)')
            
    def test_almost(self):
        """
        Test that strings which nearly fit the block pattern are not matches.
        """
        p = url_block_pattern
        
        self.assertIsNone(_re_match(p, '[](page)'))
        self.assertIsNone(_re_match(p, 'Some text(text in parens)'))
        self.assertIsNone(_re_match(p, '[text in brackets]more text.'))
            
    def test_invalid_url(self):
        """
        Test that un-reversable patterns within the parens are not matched.
        """
        p = url_block_pattern
        
        self.assertIsNone(_re_match(p, '[text](app page:pk)'))
        self.assertIsNone(_re_match(p, '[text](usr@page)'))
        self.assertIsNone(_re_match(p, '[text](site.com)'))
        self.assertIsNone(_re_match(p, '[text](http://site.com)'))
        
    def test_multiple(self):
        """
        Test that the first of multiple URL blocks is correctly matched.
        """
        p = url_block_pattern
        
        self.assertEqual(_re_match(p, '[text](page)[text2](page2)'), 
            '[text](page)')
        self.assertEqual(
            _re_match(p, 'Lorem [text](page) ipsum [text2](page2) dolor.'),
            '[text](page)')
