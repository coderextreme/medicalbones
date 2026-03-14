# Author: John W Carlson yottzumm@gmail.com
# Date: 3/10/2026
# Use with Medical bone shapes in HumanoidAnimation/Medical (processed by unknown) to overwrite HumanoidAnimation/Skeleton

# Usage: bash canonicalize.sh (runs the following)
# Alternate Usage: python CenterCoordinatePoints.py
# Reads fils in: C:/Users/jcarl/www.web3d.org/x3d/content/examples/HumanoidAnimation/Skeleton/*.x3d
# Writes files in: Skeleton/
# Processing done:
#    * Subtracts center of Coordinate.point coordinates with the center of the bounding box
#    * Sets Transform.translation with the center of the bounding box

# Use with X3D Canoncalization to correct spacing and quotes

import xml.etree.ElementTree
import os
import re
from pathlib import Path

class Center:
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

    def center(self, INPUT_FILE, OUTPUT_FILE, directory):
        self.readXML(INPUT_FILE)

        transform = self.root.find('.//Transform')
        shape = self.root.find('.//Shape')
        if shape is not None:
            for coordinate in shape.findall(".//Coordinate"):
                minimum  = [ 1000000, 1000000, 1000000 ]
                maximum  = [ -1000000, -1000000, -1000000 ]
                average  = [ 0, 0, 0 ]
                numbers = coordinate.get("point").split()
                # Get max and min array
                for num_index, num in enumerate(numbers):
                    minmaxindex = num_index % 3
                    value = float(numbers[num_index])
                    # print(f"{value}[{minmaxindex}] = {minimum}, {maximum}")
                    if value < minimum[minmaxindex]:
                        minimum[minmaxindex] = value
                        # print(f"Setting minimum to {value}")
                    if value > maximum[minmaxindex]:
                        # print(f"Setting maximum to {value}")
                        maximum[minmaxindex] = value
                    # print(f"{value}[{minmaxindex}] = {minimum}, {maximum}")
                # get center/average of minimum and maximum arrays
                average[0] = (minimum[0] + maximum[0]) * 0.5
                average[1] = (minimum[1] + maximum[1]) * 0.5
                average[2] = (minimum[2] + maximum[2]) * 0.5
                # print(f"{average} = {minimum} + {maximum}")
                # subtract the center from each number 
                for num_index, num in enumerate(numbers):
                    numbers[num_index] = float(numbers[num_index]) - average[num_index % 3]
                    # print(f"{numbers[num_index]} = {float(numbers[num_index])} - {average[num_index % 3]}")
                point = ['%.4f' % float(n) for n in numbers]
                coordinate.set("point", " ".join(point))
                # set the translation to the average
                if transform is not None:
                    transform.set("translation", " ".join(['%.4f' % ave for ave in average]))
        self.writeXML(OUTPUT_FILE, directory)

for file in Path('C:/Users/jcarl/www.web3d.org/x3d/content/examples/HumanoidAnimation/Skeleton').iterdir():
    if file.is_file() and file.name.endswith(".x3d"):
        in_file = 'C:/Users/jcarl/www.web3d.org/x3d/content/examples/HumanoidAnimation/Skeleton/'+file.name
        out_file = file.name
        print(f"{in_file} > Skeleton/{out_file}")
        skeleton = Center()
        skeleton.center(in_file, out_file, "Skeleton/")
