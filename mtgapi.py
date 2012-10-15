import urllib2
import urllib

def image_url(multiverse_id):
  return ('http://gatherer.wizards.com/Handlers/Image.ashx?'
          'multiverseid=%d&type=card' % multiverse_id)

def search_url(query_string):
  form_fields = {
      'q': query_string,
      'printType': 'books',
      'key': key,
  }
  form_string = urllib.urlencode(form_fields)
  return 'https://www.googleapis.com/books/v1/volumes?%s' % form_string
