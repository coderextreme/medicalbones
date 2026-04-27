# Author: John W Carlson yottzumm@gmail.com
# Date: 4/27/2026

# Scale Coordinate.point by the Transform.scale
# Usage: python ScaleMany.py
# Reads file in: 'C:/Users/jcarl/www.web3d.org/x3d/content/examples/HumanoidAnimation/Skeleton/'+file.name
# Writes files in: 'ScaledLaughingUpperSkeleton.x3d'

import xml.etree.ElementTree
import os
import re
from pathlib import Path

class ScaleMany:
    def __init__(self):
        self.root = None

    # readXML.py
    def readXML(self, INPUT_FILE):
        parser = xml.etree.ElementTree.XMLParser(target=xml.etree.ElementTree.TreeBuilder(insert_comments=True))
        X3D = xml.etree.ElementTree.parse(INPUT_FILE, parser=parser)
        self.root = X3D.getroot()

    def writeXML(self, OUTPUT_FILE, directory):
        header = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 3.3//EN" "https://www.web3d.org/specifications/x3d-3.3.dtd">'
        xmlstr = xml.etree.ElementTree.tostring(self.root, encoding='unicode')
        # xmlstr = re.sub(r'=(\"|&quot;)(.*?)(\"|&quot;)', r"='\2'", xmlstr)
        xmlstr = re.sub(r'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
        xmlstr = re.sub(r'xmlns:xsi="https://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
        xmlstr = re.sub(r'xsi:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-3.3.xsd"', r'xsd:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-3.3.xsd"', xmlstr)
        xmlstr = re.sub(r'xmlns:ns0="http://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
        xmlstr = re.sub(r'xmlns:ns0="https://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
        xmlstr = re.sub(r'ns0:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-3.3.xsd"', r'xsd:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-3.3.xsd"', xmlstr)
        xmlstr = re.sub(r'xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
        
        xmlString = f"{header}{xmlstr}"
        file_output = os.path.basename(OUTPUT_FILE)
        file_output = os.path.join(directory,os.path.basename(OUTPUT_FILE))
        with open(file_output, "w") as output_file:
            output_file.write(xmlString)

    def scale(self, INPUT_FILE, OUTPUT_FILE, directory):
        self.readXML(INPUT_FILE)
        print(INPUT_FILE)

        transforms = self.root.findall('.//Transform')
        for transform in transforms:
            scale = transform.get("scale", "1 1 1").split()
            shapes = transform.findall('.//Shape')
            for shape in shapes:
                for coordinate in shape.findall(".//Coordinate"):
                    numbers = coordinate.get("point").split()
                    for num_index, num in enumerate(numbers):
                        numbers[num_index] = float(numbers[num_index]) * float(scale[num_index % 3])
                    point = ['%.4f' % float(n) for n in numbers]
                    print(point)
                    coordinate.set("point", " ".join(point))
            transform.attrib.pop("scale", None)
        self.writeXML(OUTPUT_FILE, directory)

in_file = 'C:/Users/jcarl/www.web3d.org/x3d/content/examples/HumanoidAnimation/Medical/LaughingUpperSkeleton.x3d'
out_file = 'ScaledLaughingUpperSkeleton.x3d'
print(f"{in_file} > ./{out_file}")
skeleton = ScaleMany()
skeleton.scale(in_file, out_file, "./")
