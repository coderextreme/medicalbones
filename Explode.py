import xml.etree.ElementTree
import os

class Explode:
    def __init__(self):
        self.root = None

    # readXML.py
    def readXML(self, INPUT_FILE):
        X3D = xml.etree.ElementTree.parse(INPUT_FILE)
        self.root = X3D.getroot()

    def getRootFromXML(self, INPUT_FILE):
        eX3D = xml.etree.ElementTree.parse(INPUT_FILE)
        return eX3D.getroot()

    def putRootFromTree(self, root, OUTPUT_FILE):
        header = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 4.1//EN" "https://www.web3d.org/specifications/x3d-4.1.dtd">'
        xmlstr = xml.etree.ElementTree.tostring(root, encoding='unicode')
        xmlString = f"{header}{xmlstr}"
        file_output = os.path.basename(OUTPUT_FILE)
        file_output = os.path.join("shapes/",os.path.basename(OUTPUT_FILE))
        with open(file_output, "w") as output_file:
            output_file.write(xmlString)

    def writeXML(self, OUTPUT_FILE):
        self.putRootFromTree(self.root, OUTPUT_FILE) 

    def explode(self, INPUT_FILE, OUTPUT_FILE):
        self.readXML(INPUT_FILE)
        parent_map = {c: p for p in self.root.iter() for c in p}

        for shape_index, shape in enumerate(self.root.findall('.//Shape')):
            if shape is not None:
                out_file = shape.get("DEF")
                if out_file is None:
                    out_file = "shape"+str(shape_index)
                out_file = out_file+".x3d"
                root = xml.etree.ElementTree.Element("X3D")
                root.set("version", "4.1")
                scene = xml.etree.ElementTree.SubElement(root, "Scene")
                scene.append(shape)
                self.putRootFromTree(root, out_file) 

                parent = parent_map[shape]
                index = list(parent).index(shape)
                inline = xml.etree.ElementTree.Element('Inline')
                inline.set("url", '"'+out_file+'"')
                parent.insert(index, inline)
                parent.remove(shape)

        self.writeXML(OUTPUT_FILE)

skeleton = Explode()

skeleton.explode("skeleton1.x3d", "skeleton1base.x3d")
