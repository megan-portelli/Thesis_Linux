from urltools.urltools import parse
import sys

url = sys.argv[1]
try:
    parse(url=url)
except Exception as e :
        print("Invalid URL")#+ url + "': "+ str(type(e)))print("Exception occurred for url '"+ url + "': "+ str(type(e)))