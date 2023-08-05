from xmljson import badgerfish as bf
from defusedxml.ElementTree import fromstring
from collections import OrderedDict
import defusedxml.ElementTree as ET
import json

# json.dumps does not make your string ready to be loaded with json.loads.
#  It will only encode it to JSON specs (by adding escapes pretty much everywhere) !
# json.loads will transform a correctly formatted JSON string to a python dictionary. 
# It will only work if the JSON follows the JSON specs (no single quotes, uppercase for boolean's first letter, etc).

def check_format(file):
    # check if the file is correctly formatted
    try:
        tree = ET.parse(file)
        tree.getroot() == "DATA_EXPORT"
        tree.getroot()[2].tag == "ADDRESS"
        # check if third child's child is named "ROOF"
        return True
    except ET.ParseError:
        # if the file is not well-formed, print that is not well-formed
        print(file + " is not well-formed")
        return False


# define a function to convert xml to json
def xml_to_json(file):
    if check_format(file):
        with open(file, "r") as input:
            jsonOut = bf.data(fromstring(input.read()))
        return json.loads(json.dumps(jsonOut))

def extract_roof_data(data):
    print("extracting roof data")
 
    faces = data['DATA_EXPORT']['STRUCTURES']['ROOF']['FACES']
    lines = data['DATA_EXPORT']['STRUCTURES']['ROOF']['LINES']
    points = data['DATA_EXPORT']['STRUCTURES']['ROOF']['POINTS']

    counter = 0
    final_string = ""
    for face in faces['FACE']:
        #Einam per kiekviena face'a
        for path_line in face['POLYGON']['@path'].split(","):
            #Splitinam "L44,L45,L46,L47" ir einam per kiekviena is ju
            for line in lines['LINE']:
                #einam per visus line'us ir ieskom sutampanciu            
                if line['@id'] == path_line:
                    #jei randam sutampanti
                    line_points = line['@path'].split(",")
                    #splitinam ta line'o patha "C25,C1" ir einam per kiekviena is ju
                    line_type = line['@type']
                    #pasiimam line'o tipa, kurio mum reikes
                    for point in points['POINT']:
                        #einam per visus pointus ir surandam sutampancius
                        if point['@id'] == line_points[0]:
                            point1 = point['@data'].split(",")
                            #pasiimam pointo koordinates, splitindami i tris dalis: x, y, z
                        if point['@id'] == line_points[1]:
                            point2 = point['@data'].split(",") 
                            #pasiimam pointo koordinates, splitindami i tris dalis: x, y, z  +line_type + "'," + 


                    path_line_str = (" '" + path_line + "' : {'Type' : '"+ line_type + "','" + line_points[0] + "' : { 'X' : " + point1[0] + ","  
                    + "'Y' : " + point1[1] + "," + "'Z' : " + point1[2] + "},'" + line_points[1] + "' : { 'X' : " + point2[0] + ","  
                    + "'Y' : " + point2[1] + "," + "'Z' : " + point2[2] + "}" +  "},")
                    final_string = "".join([ final_string, path_line_str]) 
                    #sujungiam visus stringus i viena, kad butu lengviau irasyti i json'a
                    break
        counter += 1
                            
                               
        final_string = "{" +final_string + "}"
         
        face['POLYGON']['@path'] = eval(final_string)
        final_string = ""
        #addinam i jsona su eval funkcija

    faces = data['DATA_EXPORT']['STRUCTURES']['ROOF']['FACES']
    with open("data" + ".json","w+") as newFile:
        json.dump(faces, newFile, ensure_ascii=True, indent=2, sort_keys=False)
   






def main():
    #file = input("Iveskite failo pavadinima arba kelia iki jo: ")
    file="stogas.xml"
    extract_roof_data(xml_to_json(file))
    


if __name__ == '__main__':
    main()
