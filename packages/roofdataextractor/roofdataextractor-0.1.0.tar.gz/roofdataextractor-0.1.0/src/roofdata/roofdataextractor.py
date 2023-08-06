import xml_to_json as xtj
import extract_roof_data as erd

def main():
    #file = input("Input the path to the file: ")
    file="Area1\src\XMLFIles\stogas.xml"
    erd.extract_roof_data(xtj.xml_to_json(file))
    
if __name__ == '__main__':
    main()
