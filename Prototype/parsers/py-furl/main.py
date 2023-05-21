from furl import furl
import sys

url = sys.argv[1]
try:
    f = furl(url)
    if not url.isvalid:
        raise Exception()
except Exception as e:
    sys.stderr.write("Invalid URL")