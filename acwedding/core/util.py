from datetime import datetime

field_list_pattern = (
    r"^(?:<p>)?:((?:[^\n\r\f\v:]|\\:)+):[\t ]*(\S[^\n\r\v\f]+)" +
    r"(?:</p>|<br />)?\r?$"
)
ul_pattern = r"^[*][ \t](\S[^\r\n]*)[\r]?$"
url_block_pattern = r"\[(.+?|\\\])\]\((\w+(?:\:\w+)?(?: [\w-]+)*)\)"
wedding_date = datetime(2015, 5, 16, 13)

class NonDBImage:
    """
    May be used to simulate a BaseImage model object.
    
    Use with caution; there is no validation that the image referred to 
    exists.
    """
    def __init__(self, filename, alt_text, caption):
        self.filename = filename
        self.alt_text = alt_text
        self.caption = caption
        
def asterisks_to_ul(value):
    """
    """
    split = value.splitlines(keepends=1)
    inList = False
    
    for i, line in enumerate(split):
        m = re.match(ul_pattern, line)
        
        if m and not inList:
            split[i] = '<ul><li>{0}</li>'.format(m.group(1))
            inList = True
        elif m:
            split[i - 1] = ''
            split[i] = '<li>{0}</li>'.format(m.group(1))
        elif inList and line.strip():
            split[i - 2] += '</ul>'
            split[i - 1] = ''
            inList = False
            
    if inList:
        split[-1] += '</ul>'

    return ''.join(split)

def days_remaining_context_processor(request):
    """Context processor. Adds days_remaining to context of every view."""
    now = datetime.now()
    return {'days_remaining' : (wedding_date - now).days}
    
def reverse_urls(value):
    """
    Replace all occurences of text of format "[text](app:page pk)" with 
    HTML <a> tags, where the parentheses enclosed portions are reversed
    into an absolute URL (following standard django rules) and the 
    bracket-enclosed portion becomes the text between the tags.
    
    Example input: '[text](app:page pk)'
    Example output: '<a href="/app/page/pk">text</a>' 
    (the exact form of the output url would depend on the project's
    urlconfs).
    """
    return re.sub(url_block_pattern, _replace_url_tag, value)
    
def rst_to_table(value):
    """
    Replace all occurences of text of format ":heading: some text \n"
    with an HTML table, similar to the format and output of reStructured
    Text's "field lists" as seen at 
    docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#field-lists
    
    The block must occur at the beginning of a line (or immediately following
    a <p> tag if linebreaks was used -- see below).
    
    Multiple sequential lines of format ":heading: text" will become
    rows of a single table.
    
    If the 'linebreaks' filter is to be used, be sure to place the field
    list block within value in it's own "paragraph," i.e. TWO newlines should
    precede and follow the block. <p> tags surrounding the resulting table
    will be removed, but <br /> tags will not. Linebreaks should occur before
    this filter in a chain, otherwise the table will be wrapped in <p> tags.
    
    Example input: ':Heading: Some words \n'
    Example output: 
    '<table><tr><td>Heading</td><td>Some words</td></tr></table>'
    """
    split = value.splitlines(keepends=1)
    inTable = False
    
    for i, line in enumerate(split):
        m = re.match(field_list_pattern, line, re.M)
        
        if m:
            split[i] = '' if inTable else '<table class="table">'
            split[i] += _replace_field_list_block(m)
            inTable = True
            
        elif inTable:
            inTable = False
            split[i - 1] += '</table>'
            
    if inTable:
        split[-1] += '</table>'

    return ''.join(split)
    
def _replace_field_list_block(match):
    """
    Return an HTML <table> version of the reStructured Text-like field
    list found in the passed re.match object.
    
    See tableifyrst for more information.
    """
    heading, data = match.group(1), match.group(2)
    
    return '<tr><td>{0}:</td><td>{1}</td></tr>'.format(
        heading, data)

def _replace_url_tag(match):
    """
    Return an HTML <a>-tagged version of the reversed url using the
    parameters of the re.MatchObject as described in reverseurls.
    
    Raises NoReverseMatch if the url cannot be reversed.
    """
    text, url_desc = match.group(1), match.group(2)
    url_desc = url_desc.split(' ')
    
    reversed = reverse(url_desc[0], args=url_desc[1:])
    return '<a href="{0}">{1}</a>'.format(reversed, text)
