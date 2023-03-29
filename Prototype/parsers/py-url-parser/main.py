from url_parser import parse_url
import sys

#pip install url-parser

url = sys.argv[1]
try:
    parsedURL = parse_url(url)
except Exception as e:
    print("Exception occurred for url '"+ url + "': "+ str(type(e)))
