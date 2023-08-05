from xmljson import badgerfish as bf
from defusedxml.ElementTree import fromstring
import json
import check_format as cf

def xml_to_json(file):
    if cf.check_format(file):
        with open(file, "r") as input:
            jsonOut = bf.data(fromstring(input.read()))
        return json.loads(json.dumps(jsonOut))