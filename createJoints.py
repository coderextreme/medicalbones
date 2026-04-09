import xml.etree.ElementTree
import os
import copy

class Rigidify:
    def __init__(self):
        self.root = None

    def readXML(self, INPUT_FILE):
        X3D = xml.etree.ElementTree.parse(INPUT_FILE)
        self.root = X3D.getroot()

    def writeXML(self, OUTPUT_FILE):
        header = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 4.1//EN" "https://www.web3d.org/specifications/x3d-4.1.dtd">'
        xmlstr = xml.etree.ElementTree.tostring(self.root, encoding='unicode')
        xmlString = f"{header}{xmlstr}"
        with open(OUTPUT_FILE, "w") as output_file:
            output_file.write(xmlString)

    def print_hierarchy(self, elem, scene, level=0):
        for child in elem:
            if child.tag == "HAnimJoint" and elem.tag == "HAnimJoint":
                print('  ' * level + f'{elem.get("DEF")}')
                joint = xml.etree.ElementTree.SubElement(scene, "BallJoint")
                joint.set("containerField", 'joints')
                joint.tail = "\n"

                body1 = xml.etree.ElementTree.SubElement(joint, "RigidBody")
                elemDEF = elem.get('DEF').replace("_joint", "_rb")
                body1.set('USE', "hanim_joint_"+elemDEF)
                body1.set("containerField", 'body1')

                body2 = xml.etree.ElementTree.SubElement(joint, "RigidBody")
                childDEF = child.get('DEF').replace("_joint", "_rb")
                body2.set('USE', "hanim_joint_"+childDEF)
                body2.set("containerField", 'body2')
            self.print_hierarchy(child, scene, level + 1)

    def rigidify(self, INPUT_FILE, OUTPUT_FILE):
        self.readXML(INPUT_FILE)
        parent_map = {c: p for p in self.root.iter() for c in p}

        scene = self.root.find('.//Scene')
        joint = self.root.find('.//HAnimJoint')
        self.print_hierarchy(joint, scene)

        self.writeXML(OUTPUT_FILE)

skeleton = Rigidify()

skeleton.rigidify("hanim/skeleton1base_hanim.x3d", "0scaled/0Joints.x3d")

