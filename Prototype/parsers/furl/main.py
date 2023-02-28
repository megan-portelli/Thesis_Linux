from furl import furl
import sys

#pip install furl

try:
    url = sys.argv[1]
    f = furl(url)
    print("Successful parse")
except Exception as e:
    print (e) + "Invalid URL"