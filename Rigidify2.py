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
        xmlString = xmlString[:1701] + xmlString[1702:]
        with open(OUTPUT_FILE, "w") as output_file:
            output_file.write(xmlString)

    def print_joints(self, elem, scene, level=0):
        for child in elem:
            if child.tag == "RigidBody" and elem.tag == "RigidBody":
                # print('  ' * level + f'{elem.get("DEF")}')
                joint = xml.etree.ElementTree.SubElement(scene, "SingleAxisHingeJoint")
                joint.set("containerField", 'joints')
                joint.set("anchorPoint", child.get('position'))
                joint.set("axis", '0 0 1')
                joint.set("minAngle", '1.5708')
                joint.set("maxAngle", '1.5708')
                joint.tail = "\n"

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
        head = self.root.find('.//head')
        component = xml.etree.ElementTree.Element("component")
        component.set('name', 'RigidBodyPhysics')
        component.set('level', '2')
        head.insert(0, component)

        scene = self.root.find('.//Scene')
        transform = xml.etree.ElementTree.SubElement(scene, "Transform")
        transform.set("translation", "0 -3 0")
        shape = xml.etree.ElementTree.SubElement(transform, "Shape")
        shape.set('USE', "box")
        humanoids = []

        for humanoid_index, humanoid in enumerate(self.root.findall('.//HAnimHumanoid')):
            humanoids.append(copy.deepcopy(humanoid))

        for humanoid_index, humanoid in enumerate(self.root.findall('.//HAnimHumanoid')):
            humanoid.tag = "RigidBodyCollection"
            humanoid.attrib.pop('name', None)
            humanoid.set('DEF', humanoid.get('DEF')+"_rbc")
            humanoid.set('gravity', "0 -9.8 0")
            humanoid.set('iterations', "3")
            humanoid.attrib.pop('loa', None)
            humanoid.attrib.pop('version', None)
            humanoid.attrib.pop('scale', None)
            collision_collection = xml.etree.ElementTree.SubElement(humanoid, "CollisionCollection")
            collision_collection.set('containerField', "collider")
            collision_collection.set('appliedParameters', '"FRICTION_COEFFICIENT_1" "SLIP_COEFFICIENTS"')
            rigidbody = xml.etree.ElementTree.SubElement(humanoid, "RigidBody")
            rigidbody.set('DEF', "sphere_rb")
            rigidbody.set('containerField', "bodies")
            rigidbody.set('mass', "0")
            collidable_shape = xml.etree.ElementTree.SubElement(rigidbody, "CollidableShape")
            collidable_shape.set('DEF', "sphere_cs")
            collidable_shape.set('containerField', "geometry")
            shape = xml.etree.ElementTree.SubElement(collidable_shape, "Shape")
            shape.set('DEF', "box")
            shape.set('containerField', "shape")
            appearance = xml.etree.ElementTree.SubElement(shape, "Appearance")
            material = xml.etree.ElementTree.SubElement(appearance, "Material")
            material.set('diffuseColor', "0.5 0.5 0.5")
            sphere = xml.etree.ElementTree.SubElement(shape, "Sphere")
            sphere.set('radius', "3")
            #<Cylinder height="10" radius="2"/>
            #<Cone height="10" bottomRadius="2"/>
            #<Box size="10 0.1 10"/>

        for joint_index, joint in enumerate(self.root.findall('.//HAnimJoint')):
            if joint.get('containerField') == 'joints':
                parent_map[joint].remove(joint)
            else:
                jointDEF = joint.get('DEF')
                joint.set('DEF', jointDEF+"_rb")

                #routepos = xml.etree.ElementTree.SubElement(scene, "ROUTE")
                #routepos.set('fromNode', jointDEF+"_rb")
                #routepos.set('toNode', jointDEF)
                #routepos.set('fromField', "position")
                #routepos.set('toField', "translation")
                #routepos.tail = '\n'

                routerot = xml.etree.ElementTree.SubElement(scene, "ROUTE")
                routerot.set('fromNode', jointDEF+"_rb")
                routerot.set('toNode', jointDEF)
                routerot.set('fromField', "orientation")
                routerot.set('toField', "rotation")
                routerot.tail = '\n'

            joint.tag = "RigidBody"
            joint.attrib.pop('name', None)
            joint.set('position', joint.get('center'))
            joint.attrib.pop('center', None)
            joint.set('containerField', "bodies")
            joint.set('mass', "0.5")

        for segment_index, segment in enumerate(self.root.findall('.//HAnimSegment')):
            if segment.get('containerField') == 'segments':
                parent_map[segment].remove(segment)
            else:
                if segment.find('.//Shape') is not None:
                    shapes = []
                    for shape_index, shape in enumerate(segment.findall('.//Shape')):
                        shapes.append(copy.deepcopy(shape))
                    segmentDEF = segment.get('DEF')
                    segment.clear()
                    segment.tag = "CollidableShape"
                    segment.set('DEF', segmentDEF+"_cs")
                    segment.set('containerField', "geometry")

                    for shape_index, shape in enumerate(shapes):
                        shapeDEF = shape.get('DEF')
                        if shapeDEF is None:
                            shape.set('DEF', "Shape"+str(segment_index))
                            shape.attrib.clear()
                        shape.set('containerField', "shape")
                        segment.append(shape)

        for humanoid_index, humanoid in enumerate(self.root.findall('.//RigidBodyCollection')):
            self.print_joints(humanoid, humanoid)
            for body_index, body in enumerate(humanoid.findall('.//RigidBody')):
                for subbody_index, subbody in enumerate(body.findall('RigidBody')):
                    if parent_map[subbody] != humanoid:
                        humanoid.insert(0, subbody)
                        parent_map[subbody].remove(subbody)

        for humanoid_index, humanoid in enumerate(humanoids):
            scene.insert(0, humanoid)

        textureFound = False
        for texture_index, texture in enumerate(self.root.findall('.//ImageTexture')):
            textureDEF = texture.get('DEF')
            if textureDEF is not None:
                if textureFound:
                    texture.attrib.clear()
                    texture.set('USE', textureDEF)
                textureFound = True

        self.writeXML(OUTPUT_FILE)

skeleton = Rigidify()

skeleton.rigidify("C:/Users/jcarl/www.web3d.org/x3d/content/examples/HumanoidAnimation/Characters/JinLOA1.x3d", "Jin/JinLOA1RigidBody.x3d")

# skeleton.rigidify("C:/Users/jcarl/www.web3d.org/x3d/content/examples/HumanoidAnimation/Bones/AllBonesLOA5Skeletons.x3d", "Don/2RigidBody.x3d")
# Bones/AllBonesCollection.x3d
