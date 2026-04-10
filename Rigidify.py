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

    def print_joints(self, elem, scene, level=0):
        for child in elem:
            if child.tag == "RigidBody" and elem.tag == "RigidBody":
                print('  ' * level + f'{elem.get("DEF")}')
                joint = xml.etree.ElementTree.SubElement(scene, "SingleAxisHingeJoint")
                joint.set("containerField", 'joints')
                joint.tail = "\n"
                joint.set("anchorPoint", child.get('position'))
                joint.set("axis", '1 0 0')

                body1 = xml.etree.ElementTree.SubElement(joint, "RigidBody")
                elemDEF = elem.get('DEF')
                body1.set('USE', elemDEF)
                body1.set("containerField", 'body1')
                body1.tail = "\n"

                body2 = xml.etree.ElementTree.SubElement(joint, "RigidBody")
                childDEF = child.get('DEF')
                body2.set('USE', childDEF)
                body2.set("containerField", 'body2')
                body2.tail = "\n"
            self.print_joints(child, scene, level + 1)

    def rigidify(self, INPUT_FILE, OUTPUT_FILE):
        self.readXML(INPUT_FILE)
        parent_map = {c: p for p in self.root.iter() for c in p}

        scene = self.root.find('.//Scene')
        transform = xml.etree.ElementTree.SubElement(scene, "Transform")
        transform.set("translation", "0 -3 0")
        transform.tail = "\n"
        shape = xml.etree.ElementTree.SubElement(transform, "Shape")
        shape.set('USE', "box")
        humanoids = []

        for humanoid_index, humanoid in enumerate(self.root.findall('.//HAnimHumanoid')):
            humanoids.append(copy.deepcopy(humanoid))

        for humanoid_index, humanoid in enumerate(self.root.findall('.//HAnimHumanoid')):
            humanoid.tag = "RigidBodyCollection"
            humanoid.attrib.pop('name', None)
            # humanoid.set('DEF', humanoid.get('DEF')+"_rbc")
            humanoid.set('gravity', "0 -9.8 0")
            humanoid.set('iterations', "3")
            humanoid.attrib.pop('loa', None)
            humanoid.attrib.pop('version', None)
            collision_collection = xml.etree.ElementTree.SubElement(humanoid, "CollisionCollection")
            collision_collection.set('containerField', "collider")
            collision_collection.set('appliedParameters', '"FRICTION_COEFFICIENT_1" "SLIP_COEFFICIENTS"')
            collision_collection.tail = '\n'

            rigidbody = xml.etree.ElementTree.SubElement(humanoid, "RigidBody")
            rigidbody.set('DEF', "box_rb")
            rigidbody.set('containerField', "bodies")
            rigidbody.set('mass', "0")
            rigidbody.tail = '\n'
            collidable_shape = xml.etree.ElementTree.SubElement(rigidbody, "CollidableShape")
            collidable_shape.set('DEF', "box_cs")
            collidable_shape.set('containerField', "geometry")
            collidable_shape.tail = '\n'
            shape = xml.etree.ElementTree.SubElement(collidable_shape, "Shape")
            shape.set('DEF', "box")
            shape.set('containerField', "shape")
            shape.tail = '\n'
            appearance = xml.etree.ElementTree.SubElement(shape, "Appearance")
            appearance.tail = '\n'
            material = xml.etree.ElementTree.SubElement(appearance, "Material")
            material.set('diffuseColor', "0.5 0.5 0.5")
            material.tail = '\n'
            sphere = xml.etree.ElementTree.SubElement(shape, "Sphere")
            sphere.set('radius', "3")
            sphere.tail = '\n'
            #<Cylinder height="10" radius="2"/>
            #<Cone height="10" bottomRadius="2"/>
            #<Box size="10 0.1 10"/>

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
            self.print_joints(humanoid, humanoid)
            for body_index, body in enumerate(humanoid.findall('.//RigidBody')):
                for subbody_index, subbody in enumerate(body.findall('RigidBody')):
                    if parent_map[subbody] != humanoid:
                        humanoid.append(subbody)
                        parent_map[subbody].remove(subbody)

        for humanoid_index, humanoid in enumerate(humanoids):
            scene.insert(0, humanoid)

        background = xml.etree.ElementTree.Element("Background")
        background.set('skyColor', "0.3 0.5 0.9")
        background.tail = "\n"
        scene.insert(0, background)

        viewpoint = xml.etree.ElementTree.Element("Viewpoint")
        viewpoint.set('centerOfRotation', "0 0 0")
        viewpoint.set('description', "Humanoid LOA 3 Far")
        viewpoint.set('position', "0 20.0 100")
        viewpoint.tail = "\n"
        scene.insert(0, viewpoint)

        self.writeXML(OUTPUT_FILE)

skeleton = Rigidify()

skeleton.rigidify("0scaled/0skeleton1scaled.x3d", "0scaled/0RigidBody.x3d")
