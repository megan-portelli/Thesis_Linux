from url_parser import parse_url
import sys

#pip install url-parser

try:
    url = parse_url(sys.argv[1])
except Exception as e:
    print (e) + "Invalid URL"