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

        scene = self.root.find('.//Scene')
        humanoids = []

        for humanoid_index, humanoid in enumerate(self.root.findall('.//HAnimHumanoid')):
            humanoids.append(copy.deepcopy(humanoid))

        for humanoid_index, humanoid in enumerate(self.root.findall('.//HAnimHumanoid')):
            humanoid.tag = "RigidBodyCollection"
            humanoid.attrib.pop('name', None)
            # humanoid.set('DEF', humanoid.get('DEF')+"_rbc")
            humanoid.set('gravity', "0 -9.8 0")
            humanoid.attrib.pop('loa', None)
            humanoid.attrib.pop('version', None)

        for joint_index, joint in enumerate(self.root.findall('.//HAnimJoint')):
            if joint.get('USE') is not None:
                parent_map[joint].remove(joint)
            else:
                jointDEF = joint.get('DEF')
                joint.set('DEF', jointDEF+"_rb")

                routepos = xml.etree.ElementTree.SubElement(scene, "ROUTE")
                routepos.set('fromNode', jointDEF+"_rb")
                routepos.set('toNode', jointDEF)
                routepos.set('fromField', "position")
                routepos.set('toField', "translation")
                routepos.tail = '\n'

                routerot = xml.etree.ElementTree.SubElement(scene, "ROUTE")
                routerot.set('fromNode', jointDEF+"_rb")
                routerot.set('toNode', jointDEF)
                routerot.set('fromField', "orientation")
                routerot.set('toField', "rotation")
                routerot.tail = '\n'

            joint.tag = "RigidBody"
            joint.attrib.pop('name', None)
            joint.set('containerField', "bodies")
            joint.set('mass', "0.5")

        for segment_index, segment in enumerate(self.root.findall('.//HAnimSegment')):
            segment.tag = "CollidableShape"
            segment.attrib.pop('name', None)
            segment.set('DEF', segment.get('DEF')+"_cs")
            segment.set('containerField', "geometry")
            for shape_index, shape in enumerate(segment.findall('Shape')):
                shapeDEF = shape.get('DEF')
                shape.attrib.clear()
                shape.clear()
                shape.set('containerField', "shape")
                shape.set('USE', shapeDEF)

        for humanoid_index, humanoid in enumerate(self.root.findall('.//RigidBodyCollection')):
            for body_index, body in enumerate(humanoid.findall('.//RigidBody')):
                for subbody_index, subbody in enumerate(body.findall('RigidBody')):
                    if parent_map[subbody] != humanoid:
                        humanoid.append(subbody)
                        parent_map[subbody].remove(subbody)

        for humanoid_index, humanoid in enumerate(humanoids):
            scene.insert(0, humanoid)

        self.writeXML(OUTPUT_FILE)

skeleton = Rigidify()

skeleton.rigidify("0scaled/0skeleton1scaled.x3d", "0scaled/0RigidBody.x3d")
