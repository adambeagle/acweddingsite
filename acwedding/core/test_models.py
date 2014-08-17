import re

from django.test import TestCase

img_pattern = r"^images/(?:.*/)*(.+)$"

class ImgPatternTestCase(TestCase):
    def test_root(self):
        full = 'images/file.ext'
        match = re.match(img_pattern, full)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(), full)
        self.assertEqual(match.group(1), 'file.ext')
        
    def test_nested(self):
        full = 'images/dir/file.ext'
        match = re.match(img_pattern, full)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(), full)
        self.assertEqual(match.group(1), 'file.ext')
        
    def test_nested_twice(self):
        full = 'images/dir/dir2/file.ext'
        match = re.match(img_pattern, full)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(), full)
        self.assertEqual(match.group(1), 'file.ext')
        
    def test_nested_lots(self):
        full = 'images/dir/dir2/.something/more/another/file.ext'
        match = re.match(img_pattern, full)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(), full)
        self.assertEqual(match.group(1), 'file.ext')
        
    def test_no_ext(self):
        full = 'images/file'
        match = re.match(img_pattern, full)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(), full)
        self.assertEqual(match.group(1), 'file')
        
    def test_no_ext_nested(self):
        full = 'images/dir/.dir2/more/file'
        match = re.match(img_pattern, full)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(), full)
        self.assertEqual(match.group(1), 'file')
        
    def test_multidot(self):
        full = 'images/file.something.ext'
        match = re.match(img_pattern, full)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(), full)
        self.assertEqual(match.group(1), 'file.something.ext')
        
    def test_multidot_nested(self):
        full = 'images/dir/dir2/.dir3/file.something.ext'
        match = re.match(img_pattern, full)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(), full)
        self.assertEqual(match.group(1), 'file.something.ext')
        
        