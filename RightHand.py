import xml.etree.ElementTree
import numpy as np
import re
import os

def writeXML(root, OUTPUT_FILE, directory):
    header = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 4.1//EN" "https://www.web3d.org/specifications/x3d-3.3.dtd">'
    xmlstr = xml.etree.ElementTree.tostring(root, encoding='unicode')
    # xmlstr = re.sub(r'=(\"|&quot;)(.*?)(\"|&quot;)', r"='\2'", xmlstr)
    xmlstr = re.sub(r'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
    xmlstr = re.sub(r'xmlns:xsi="https://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
    xmlstr = re.sub(r'xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
    xmlstr = re.sub(r'xmlns:ns0="http://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
    xmlstr = re.sub(r'xmlns:ns0="https://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
    xmlstr = re.sub(r'xsi:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-3.3.xsd"', r'xsd:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-3.3.xsd"', xmlstr)
    xmlstr = re.sub(r'xsi:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-4.1.xsd"', r'xsd:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-4.1.xsd"', xmlstr)
    xmlstr = re.sub(r'ns0:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-3.3.xsd"', r'xsd:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-3.3.xsd"', xmlstr)
    xmlstr = re.sub(r'ns0:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-4.1.xsd"', r'xsd:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-4.1.xsd"', xmlstr)
    
    xmlString = f"{header}{xmlstr}"
    file_output = os.path.basename(OUTPUT_FILE)
    file_output = os.path.join(directory,os.path.basename(OUTPUT_FILE))
    with open(file_output, "w") as output_file:
        output_file.write(xmlString)

"""
SHAPE_TO_JOINT_MAP = {
    0:  'r_index3',
    1:  'r_middle3',
    2:  'r_index2',
    3:  'r_index3',
    4:  'r_index3',
    5:  'r_middle3',
    6:  'r_middle2',
    7:  'r_thumb3',
    8:  'r_ring3',
    9:  'r_middle1',
    10: 'r_index1',
    11: 'r_thumb2',
    12: 'r_thumb1',
    13: 'r_pinky3',
    14: 'r_middle0',
    15: 'r_middle0',
    16: 'r_index0',
    17: 'r_index0',
    18: 'r_ring2',
    19: 'r_ring1',
    20: 'r_ring0',
    21: 'r_middle0',
    22: 'r_pinky2',
    23: 'r_pinky1',
    24: 'r_pinky0',
    25: 'r_pinky0',
    26: 'r_ring0',
}
"""

"""
SHAPE_TO_JOINT_MAP = {
    0:  'r_ring3',
    1:  'r_middle3',
    2:  'r_ring2',
    3:  'r_ring3',
    4:  'r_ring3',
    5:  'r_middle3',
    6:  'r_middle2',
    7:  'r_pinky3',
    8:  'r_index3',
    9:  'r_middle1',
    10: 'r_ring1',
    11: 'r_pinky2',
    12: 'r_pinky1',
    13: 'r_thumb3',
    14: 'r_middle0',
    15: 'r_middle0',
    16: 'r_ring0',
    17: 'r_ring0',
    18: 'r_index1',
    19: 'r_index0',
    20: 'r_index0',
    21: 'r_middle0',
    22: 'r_thumb2',
    23: 'r_thumb1',
    24: 'r_thumb1',
    25: 'r_thumb1',
    26: 'r_index0',
}
"""

SHAPE_TO_JOINT_MAP = {
    0:  'r_ring3',
    1:  'r_middle3',
    2:  'r_ring2',
    3:  'r_ring3',
    4:  'r_ring3',
    5:  'r_middle3',
    6:  'r_middle2',
    7:  'r_pinky3',
    8:  'r_index3',
    9:  'r_index2',
    10: 'r_middle1',
    11: 'r_ring1',
    12: 'r_pinky2',
    13: 'r_thumb3',
    14: 'r_index1',
    15: 'r_middle0',
    16: 'r_ring0',
    17: 'r_pinky0',
    18: 'r_index1',
    19: 'r_index0',
    20: 'r_index0',
    21: 'r_middle0',
    22: 'r_thumb2',
    23: 'r_thumb1',
    24: 'r_thumb1',
    25: 'r_thumb1',
    26: 'r_index0',
}

def parse_x3d_hand(filepath):
    tree = xml.etree.ElementTree.parse(filepath)
    root = tree.getroot()
    parent_map = {c: p for p in root.iter() for c in p}

    bones = []

    shape_index = 0

    for joint in root.iter('HAnimJoint'):
        joint_name   = joint.get('name') or joint.get('DEF', 'unnamed')
        joint_center = joint.get('center', '0 0 0')
        center_xyz   = tuple(float(v) for v in joint_center.split())

        for segment in joint.findall('HAnimSegment'):
            seg_name = segment.get('name') or segment.get('DEF', 'unnamed')

            for transform in segment.findall('Transform'):
                for shape in transform.findall('Shape'):
                    ifses = shape.findall('IndexedFaceSet')
                    for mesh_index, ifs in enumerate(ifses):
                        print(f"\nJoint: {joint_name}  |  Segment: {seg_name}")
                        print(f"  Joint center: {center_xyz}")
                        print(f"  IFS mesh count: {len(ifses)}")

                        coord_node = ifs.find('Coordinate')
                        if coord_node is None:
                            continue

                        pts = [float(v) for v in coord_node.get('point', '').split()]
                        verts = np.array(pts).reshape(-1, 3)
                        centroid = verts.mean(axis=0)

                        if seg_name.endswith("r_hand") and joint_name.endswith("r_wrist"):
                            bones.append({
                                'joint':   joint,
                                'segment': segment,
                                'shape': shape,
                                'joint_name':   joint_name,
                                'segment_name': seg_name,
                                'shape_index':  shape_index,
                                'centroid':     centroid,
                                'num_verts':    len(verts),
                                'vertices':     verts,
                            })
                            shape_index += 1

    segment_map = {}

    for bone in bones:
        name, dist = nearest_joint(bone['centroid'], HANIM_HAND_JOINTS)
        if SHAPE_TO_JOINT_MAP[bone['shape_index']] is not None:
            name = SHAPE_TO_JOINT_MAP[bone['shape_index']]
        else:
            name = name+"_"+bone['shape_index']
        bone['inferred_bone'] = name
        bone['match_distance_cm'] = round(dist, 2)
        if name in segment_map:
            new_segment = segment_map[name]
        else:
            new_joint = xml.etree.ElementTree.SubElement(bone['joint'], "HAnimJoint")
            new_joint_name = name
            new_joint.set('DEF', 'Joe_'+new_joint_name)
            new_joint.set('name', new_joint_name)
            new_joint.tail = "\n"
            new_joint.text = "\n"

            new_segment = xml.etree.ElementTree.SubElement(new_joint, "HAnimSegment")
            new_segment_name = name+"_segment"
            new_segment.set('DEF', 'Joe_'+new_segment_name)
            new_segment.set('name', new_segment_name)
            new_segment.tail = "\n"
            new_segment.text = "\n"

            touch_sensor = xml.etree.ElementTree.SubElement(new_segment, "TouchSensor")
            touch_sensor .set('description', new_segment_name)
            touch_sensor.tail = "\n"
            touch_sensor.text = "\n"

            segment_map[name] = new_segment

        new_segment.append(bone['shape'])
        parent_map[bone['shape']].remove(bone['shape'])

    writeXML(root, "LaughingUpperSkeletonRightHand.x3d", ".")

    return bones

# H-Anim standard joint centers for right hand (approximate, in meters)
HANIM_HAND_JOINTS = {
    'r_thumb1':       (-0.19,  0.93,  0.02),
    'r_thumb2':       (-0.21,  0.94,  0.03),
    'r_thumb3':       (-0.22,  0.95,  0.03),
    'r_index0':       (-0.20,  0.95,  0.01),
    'r_index1':       (-0.20,  0.97,  0.01),
    'r_index2':       (-0.20,  0.99,  0.01),
    'r_index3':       (-0.20,  1.01,  0.01),
    'r_middle0':      (-0.18,  0.95,  0.00),
    'r_middle1':      (-0.18,  0.97,  0.00),
    'r_middle2':      (-0.18,  0.99,  0.00),
    'r_middle3':      (-0.18,  1.01,  0.00),
    'r_ring0':        (-0.16,  0.95, -0.01),
    'r_ring1':        (-0.16,  0.97, -0.01),
    'r_ring2':        (-0.16,  0.99, -0.01),
    'r_ring3':        (-0.16,  1.01, -0.01),
    'r_pinky0':       (-0.14,  0.95, -0.02),
    'r_pinky1':       (-0.14,  0.97, -0.02),
    'r_pinky2':       (-0.14,  0.99, -0.02),
    'r_pinky3':       (-0.14,  1.01, -0.02),
}

def nearest_joint(centroid_cm, joint_table_m, scale=1.0):
    """Find the H-Anim joint name closest to the mesh centroid."""
    best_name, best_dist = None, float('inf')
    for name, pos_m in joint_table_m.items():
        pos_cm = np.array(pos_m) * scale
        dist = np.linalg.norm(centroid_cm - pos_cm)
        if dist < best_dist:
            best_dist, best_name = dist, name
    return best_name, best_dist

def assign_bone_names(bones):
    for bone in bones:
        name, dist = nearest_joint(bone['centroid'], HANIM_HAND_JOINTS)
        bone['inferred_bone'] = name
        bone['match_distance_cm'] = round(dist, 2)
    return bones

bones = parse_x3d_hand('ScaledLaughingUpperSkeleton.x3d')

# bones = assign_bone_names(bones)

for b in bones:
    print(
        f"Shape {b['shape_index']:2d} | "
        f"Centroid: ({b['centroid'][0]:6.2f}, {b['centroid'][1]:6.2f}, {b['centroid'][2]:6.2f}) | "
        f"-> {b['inferred_bone']:15s} std loc {HANIM_HAND_JOINTS[b['inferred_bone']]} (dist: {b['match_distance_cm']} cm)"
    )

