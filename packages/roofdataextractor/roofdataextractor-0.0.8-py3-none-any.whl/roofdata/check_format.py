import defusedxml.ElementTree as ET

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
