from furl import furl
import sys

url = sys.argv[1]
try:
    f = furl(url)
except Exception as e:
    print("Invalid URL")#+ url + "': "+ str(type(e)))