from xmljson import badgerfish as bf
from defusedxml.ElementTree import fromstring
import json
import check_format

def xtj(file):
    if check_format.cf(file):
        with open(file, "r") as input:
            jsonOut = bf.data(fromstring(input.read()))
        return json.loads(json.dumps(jsonOut))