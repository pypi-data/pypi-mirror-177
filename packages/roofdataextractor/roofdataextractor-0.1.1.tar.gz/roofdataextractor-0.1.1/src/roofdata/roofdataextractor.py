import check_format
import extract_roof_data
import xml_to_json


def main():
    #file = input("Iveskite failo pavadinima arba kelia iki jo: ")
    file="src\XMLFIles\stogas.xml"
    print(extract_roof_data.erd(xml_to_json.xtj(file)))
    #extract_roof_data.erd(xml_to_json.xtj(file))
    


if __name__ == '__main__':
    main()
