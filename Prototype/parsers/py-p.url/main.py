from purl import Purl, exceptions
import sys

#noticing that there are differences when parsing backslashes in this parser and in other parsers
#could be interesting to use it when discussing results since this is whatwg compliant and browsers
#are compliant with that standard
url = sys.argv[1]
try:
    parsedURL = Purl(url)
    print(parsedURL)
except exceptions.InvalidUrlError as e :
        print("Invalid URL")#+ url + "': "+ str(type(e)))print("Exception occurred for url '"+ url + "': "+ str(type(e)))
except Exception as ex:
        print("Invalid URL")#+ url + "': "+ str(type(e)))print("Exception occurred for url '"+ url + "': "+ str(type(ex)))
