import re
#from sys import stderr

from .templatetags.core_tags import (field_list_pattern, rsttotable, 
    url_block_pattern)
    
def _re_match(pattern, s, flags=0):
    match = re.search(pattern, s, flags)
    
    if match is None:
        return None
    else:
        return match.group()

def test_field_list_regex():
    p = field_list_pattern
    
    # Success cases
    assert _re_match(p, ':head: text') == ':head: text'
    assert _re_match(p, ':head:text\n') == ':head:text'
    assert _re_match(p, 'This is a sentence.\n:head:text', re.M) == ':head:text'
    assert _re_match(p, ':head: word 1@#<>. ') == ':head: word 1@#<>. '
    assert _re_match(p, ':te\\:st:  \ttext ') == ':te\\:st:  \ttext '

    # Failure cases
    assert _re_match(p, ':: text') == None
    assert _re_match(p, ':head: ') == None
    
    # Groups
    m = re.search(p, ':Heading: Lorem ipsum dolor')
    assert m.group(1) == 'Heading'
    assert m.group(2) == 'Lorem ipsum dolor'
    
    m = re.search(p, ':h1: text : text2 \n')
    assert m.group(1) == 'h1'
    assert m.group(2) == 'text : text2 '
    
def test_rsttotable():
    long = ('This is a paragraph.\n\n' + 
        ':Heading: Some text \n' +
        ':Heading 2: More text\n\n' +
        'This is another paragraph.')

    long_tabled = ('This is a paragraph.\n\n' +
        '<table><tr><td>Heading</td><td>Some text </td></tr>' + 
        '<tr><td>Heading 2</td><td>More text</td></tr></table>\n\n' +
        'This is another paragraph.')
        
    simple = ':h1: text\n:h2: text2'
    simple_tabled = ('<table><tr><td>h1</td><td>text</td></tr>' +
        '<tr><td>h2</td><td>text2</td></tr></table>\n')
    
    assert rsttotable(simple) == simple_tabled
    assert rsttotable(long) == long_tabled
    
def test_url_block_regex():
    p = url_block_pattern
    
    # Success cases
    assert _re_match(p, '[text](page)') == '[text](page)'
    assert _re_match(p, 'Lorem [text](page) ipsum.') == '[text](page)'
    assert _re_match(p, 'Lorem ipsum [text.](page)') == '[text.](page)'
    assert _re_match(p, '[Text](page) lorem ipsum.') == '[Text](page)'
    assert _re_match(p, 'Lorem\nipsum [text](page)\ndolor.') == '[text](page)'
    assert _re_match(p, '[one two](app:page)') == '[one two](app:page)'
    assert _re_match(p, '[one two](page pk)') == '[one two](page pk)'
    assert _re_match(p, '[one two](page a1 a2)') == '[one two](page a1 a2)'
    assert _re_match(p, '[text](app:page pk)') == '[text](app:page pk)'
    assert _re_match(p, '[/.,\':\\+=-_<>](page)') == '[/.,\':\\+=-_<>](page)'
    
    # Failure cases
    assert _re_match(p, '[text](app page:pk)') == None
    assert _re_match(p, '[text](usr@page)') == None
    assert _re_match(p, '[text](http://site.com)') == None
    assert _re_match(p, '[text](site.com)') == None
    assert _re_match(p, '[](page)') == None
    assert _re_match(p, 'Some text(text in parens)') == None
    assert _re_match(p, '[text in brackets]more text.') == None
    
    # Groups
    m = re.search(p, 'Lorem [some text](app:page pk) ipsum.')
    assert m.group() == '[some text](app:page pk)'
    assert m.group(1) == 'some text'
    assert m.group(2) == 'app:page pk'
    