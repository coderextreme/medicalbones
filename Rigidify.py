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

    def rigidify(self, INPUT_FILE, OUTPUT_FILE):
        self.readXML(INPUT_FILE)
        parent_map = {c: p for p in self.root.iter() for c in p}

        for humanoid_index, humanoid in enumerate(self.root.findall('.//HAnimHumanoid')):
            humanoid.tag = "RigidBodyCollection"
            humanoid.attrib.pop('name', None)
            humanoid.attrib.pop('loa', None)
            humanoid.attrib.pop('version', None)

        for joint_index, joint in enumerate(self.root.findall('.//HAnimJoint')):
            if joint.get('USE') is not None:
                parent_map[joint].remove(joint)
            joint.tag = "RigidBody"
            joint.attrib.pop('name', None)
            joint.attrib.pop('containerField', None)

        for segment_index, segment in enumerate(self.root.findall('.//HAnimSegment')):
            segment.tag = "CollidableShape"
            segment.attrib.pop('name', None)
            for inline_index, inline in enumerate(segment.findall('Inline')):
                inline.tag = "InlineGeometry"
                inline.set('containerField', "shape")

        for humanoid_index, humanoid in enumerate(self.root.findall('.//RigidBodyCollection')):
            for body_index, body in enumerate(humanoid.findall('.//RigidBody')):
                for subbody_index, subbody in enumerate(body.findall('RigidBody')):
                    if parent_map[subbody] != humanoid:
                        print(f" remove {subbody.get('DEF')} from {parent_map[subbody].get('DEF')}")
                        humanoid.append(subbody)
                        parent_map[subbody].remove(subbody)

        self.writeXML(OUTPUT_FILE)

skeleton = Rigidify()

skeleton.rigidify("0scaled/0skeleton1AImapped.x3d", "0scaled/0RigidBody.x3d")
