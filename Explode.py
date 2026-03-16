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

    def putRootFromTree(self, root, OUTPUT_FILE, directory):
        header = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 4.1//EN" "https://www.web3d.org/specifications/x3d-4.1.dtd">'
        xmlstr = xml.etree.ElementTree.tostring(root, encoding='unicode')
        xmlString = f"{header}{xmlstr}"
        file_output = os.path.basename(OUTPUT_FILE)
        file_output = os.path.join(directory,os.path.basename(OUTPUT_FILE))
        with open(file_output, "w") as output_file:
            output_file.write(xmlString)

    def writeXML(self, OUTPUT_FILE, directory):
        self.putRootFromTree(self.root, OUTPUT_FILE, directory) 

    def explode(self, INPUT_FILE, OUTPUT_FILE, directory):
        self.readXML(INPUT_FILE)
        parent_map = {c: p for p in self.root.iter() for c in p}

        for shape_index, shape in enumerate(self.root.findall('.//Shape')):
            if shape is not None:
                #for coordinate in shape.findall(".//Coordinate"):
                #    numbers = coordinate.get("point").split()
                #    for num_index, num in enumerate(numbers):
                #        numbers[num_index] = float(num) * 0.029
                #    point = ['%.5f' % n for n in numbers]
                #    coordinate.set("point", " ".join(point))
                out_file = shape.get("DEF")
                shapeDEF = out_file
                if out_file is None:
                    out_file = "shape"+str(shape_index)
                out_file = out_file+".x3d"
                # shape.set("containerField", "children")
                root = xml.etree.ElementTree.Element("X3D")
                root.text = "\n"
                root.tail = "\n"
                root.set("version", "4.1")
                root.set("profile", "Full")
                root.set("xmlns:xsd","https://www.w3.org/2001/XMLSchema-instance")
                root.set("xsd:noNamespaceSchemaLocation", "https://www.web3d.org/specifications/x3d-4.1.xsd")
                head = xml.etree.ElementTree.SubElement(root, "head")
                head.text = "\n"
                head.tail = "\n"
                component = xml.etree.ElementTree.Element('component')
                component.set("name", "Networking")
                component.set("level", "4")
                component.text = ""
                component.tail = "\n"
                head.append(component)
                component = xml.etree.ElementTree.Element('component')
                component.set("name", "HAnim")
                component.set("level", "3")
                component.text = ""
                component.tail = "\n"
                head.append(component)
                meta = xml.etree.ElementTree.Element('meta')
                meta.text = ""
                meta.tail = "\n"
                meta.set("name", "title")
                meta.set("content", out_file)
                head.append(meta)
                meta = xml.etree.ElementTree.Element('meta')
                meta.text = ""
                meta.tail = "\n"
                meta.set("name", "identifier")
                meta.set("content", "https://coderextreme.net/X3DJSONLD/src/main/data/"+out_file)
                head.append(meta)
                meta = xml.etree.ElementTree.Element('meta')
                meta.text = ""
                meta.tail = "\n"
                meta.set("name", "description")
                meta.set("content", "Part of a skeleton: "+shapeDEF)
                meta = xml.etree.ElementTree.Element('meta')
                meta.text = ""
                meta.tail = "\n"
                meta.set("name", "generator")
                meta.set("content", "medicalbones/Explode.py")
                head.append(meta)
                scene = xml.etree.ElementTree.SubElement(root, "Scene")
                scene.text = "\n"
                scene.tail = "\n"
                scene.append(shape)
                self.putRootFromTree(root, out_file, directory) 
                humanoid = xml.etree.ElementTree.Element('HAnimHumanoid')
                humanoid.text = "\n"
                humanoid.tail = "\n"
                humanoid.set("version", "2.0")

                parent = parent_map[shape]
                index = list(parent).index(shape)
                parent.insert(index, humanoid)
                out_joint = xml.etree.ElementTree.Element('HAnimJoint')
                out_joint.text = "\n"
                out_joint.tail = "\n"
                # TODO only top-level Joint
                out_joint.set("containerField", "skeleton")
                out_joint.set("DEF", "hanim_joint_"+shapeDEF)
                out_joint.set("name", "joint_"+shapeDEF)
                humanoid.append(out_joint)

                use_joint = xml.etree.ElementTree.Element('HAnimJoint')
                use_joint.text = "\n"
                use_joint.tail = "\n"
                use_joint.set("containerField", "joints")
                use_joint.set("USE", "hanim_joint_"+shapeDEF)
                humanoid.append(use_joint)

                in_joint = xml.etree.ElementTree.Element('HAnimJoint')
                in_joint.text = "\n"
                in_joint.tail = "\n"
                in_joint.set("DEF", "hanim_joint_"+shapeDEF+"_center")
                in_joint.set("name", "joint_"+shapeDEF+"_center")
                out_joint.append(in_joint)

                use_joint_center = xml.etree.ElementTree.Element('HAnimJoint')
                use_joint_center.text = "\n"
                use_joint_center.tail = "\n"
                use_joint_center.set("containerField", "joints")
                use_joint_center.set("USE", "hanim_joint_"+shapeDEF+"_center")
                humanoid.append(use_joint_center)

                segment = xml.etree.ElementTree.Element('HAnimSegment')
                segment.text = "\n"
                segment.tail = "\n"
                segment.set("DEF", "hanim_segment_"+shapeDEF)
                segment.set("name", "segment_"+shapeDEF)
                in_joint.append(segment)

                inline = xml.etree.ElementTree.Element('Inline')
                inline.text = "\n"
                inline.tail = "\n"
                segment.append(inline)
                # inline.set("url", '"'+out_file+'#'+shape.get("DEF")+'_Geo"')
                inline.set("url", '"'+out_file+'"')
                parent.remove(shape)

        self.writeXML(OUTPUT_FILE, directory)

skeleton = Explode()

#skeleton.explode("skeleton1.x3d", "skeleton1base.x3d", "shapes/")
#skeleton.explode("skeleton1_hanim.x3d", "skeleton1base_hanim.x3d", "hanim/")
#skeleton.explode("skeleton1.x3d", "skeleton1scaled.x3d", "scaled/")
skeleton.explode("0skeleton1.x3d", "0skeleton1scaled.x3d", "0scaled/")
