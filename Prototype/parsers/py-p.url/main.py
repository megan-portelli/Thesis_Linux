from purl import *
import sys

# #noticing that there are differences when parsing backslashes in this parser and in other parsers
# #could be interesting to use it when discussing results since this is whatwg compliant and browsers
# #are compliant with that standard
url = sys.argv[1]
try:
    parsedURL = url(url)
    if parsedURL.is_valid == False:
        raise exceptions.InvalidUrlError()
except exceptions.InvalidUrlError as e :
    sys.stderr.write("Invalid URL")
except Exception as ex:
     sys.stderr.write("Invalid URL")
