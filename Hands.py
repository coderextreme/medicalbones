import xml.etree.ElementTree
import numpy as np
import re
import os

def writeXML(root, OUTPUT_FILE, directory):
    header = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 4.1//EN" "https://www.web3d.org/specifications/x3d-3.3.dtd">'
    xmlstr = xml.etree.ElementTree.tostring(root, encoding='unicode')

    xmlstr = re.sub(r'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
    xmlstr = re.sub(r'xmlns:xsi="https://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
    xmlstr = re.sub(r'xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
    xmlstr = re.sub(r'xmlns:ns0="http://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
    xmlstr = re.sub(r'xmlns:ns0="https://www.w3.org/2001/XMLSchema-instance"', r'xmlns:xsd="https://www.w3.org/2001/XMLSchema-instance"', xmlstr)
    xmlstr = re.sub(r'xsi:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-3.3.xsd"', r'xsd:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-3.3.xsd"', xmlstr)
    xmlstr = re.sub(r'xsi:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-4.1.xsd"', r'xsd:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-4.1.xsd"', xmlstr)
    xmlstr = re.sub(r'ns0:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-3.3.xsd"', r'xsd:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-3.3.xsd"', xmlstr)
    xmlstr = re.sub(r'ns0:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-4.1.xsd"', r'xsd:noNamespaceSchemaLocation="https://www.web3d.org/specifications/x3d-4.1.xsd"', xmlstr)

    xmlString = f"{header}\n{xmlstr}"
    file_output = os.path.join(directory, os.path.basename(OUTPUT_FILE))
    with open(file_output, "w") as output_file:
        output_file.write(xmlString)

# Mapping for the Right Hand
SHAPE_TO_JOINT_MAP = {
    0:  'r_ring3',   1:  'r_middle3', 2:  'r_ring2',   3:  'r_ring3',
    4:  'r_ring3',   5:  'r_middle3', 6:  'r_middle2', 7:  'r_pinky3',
    8:  'r_index3',  9:  'r_index2',  10: 'r_middle1', 11: 'r_ring1',
    12: 'r_pinky2',  13: 'r_thumb3',  14: 'r_index1',  15: 'r_middle0',
    16: 'r_ring0',   17: 'r_pinky0',  18: 'r_index1',  19: 'r_index0',
    20: 'r_index0',  21: 'r_middle0', 22: 'r_thumb2',  23: 'r_thumb1',
    24: 'r_thumb1',  25: 'r_thumb1',  26: 'r_index0',
}

# Mapping for the Left Hand (Assumes identical mirrored shape order in X3D)
SHAPE_TO_JOINT_MAP_LEFT = {k: v.replace('r_', 'l_') for k, v in SHAPE_TO_JOINT_MAP.items()}


# H-Anim standard joint centers for both hands (approximate, in meters)
HANIM_HAND_JOINTS = {
    # RIGHT HAND
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

    # LEFT HAND (X-axis mirrored)
    'l_thumb1':       ( 0.19,  0.93,  0.02),
    'l_thumb2':       ( 0.21,  0.94,  0.03),
    'l_thumb3':       ( 0.22,  0.95,  0.03),
    'l_index0':       ( 0.20,  0.95,  0.01),
    'l_index1':       ( 0.20,  0.97,  0.01),
    'l_index2':       ( 0.20,  0.99,  0.01),
    'l_index3':       ( 0.20,  1.01,  0.01),
    'l_middle0':      ( 0.18,  0.95,  0.00),
    'l_middle1':      ( 0.18,  0.97,  0.00),
    'l_middle2':      ( 0.18,  0.99,  0.00),
    'l_middle3':      ( 0.18,  1.01,  0.00),
    'l_ring0':        ( 0.16,  0.95, -0.01),
    'l_ring1':        ( 0.16,  0.97, -0.01),
    'l_ring2':        ( 0.16,  0.99, -0.01),
    'l_ring3':        ( 0.16,  1.01, -0.01),
    'l_pinky0':       ( 0.14,  0.95, -0.02),
    'l_pinky1':       ( 0.14,  0.97, -0.02),
    'l_pinky2':       ( 0.14,  0.99, -0.02),
    'l_pinky3':       ( 0.14,  1.01, -0.02),
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

def parse_x3d_hand(filepath):
    tree = xml.etree.ElementTree.parse(filepath)
    root = tree.getroot()
    parent_map = {c: p for p in root.iter() for c in p}

    bones = []

    # Track shape indexes separately for right and left hands
    shape_index_r = 0
    shape_index_l = 0

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
                        coord_node = ifs.find('Coordinate')
                        if coord_node is None:
                            continue

                        pts = [float(v) for v in coord_node.get('point', '').split()]
                        verts = np.array(pts).reshape(-1, 3)
                        centroid = verts.mean(axis=0)

                        is_right = seg_name.endswith("r_hand") and joint_name.endswith("r_wrist")
                        is_left  = seg_name.endswith("l_hand") and joint_name.endswith("l_wrist")

                        if is_right or is_left:
                            print(f"\nJoint: {joint_name}  |  Segment: {seg_name}")
                            print(f"  Joint center: {center_xyz}")
                            print(f"  IFS mesh count: {len(ifses)}")

                            side = 'r' if is_right else 'l'
                            current_shape_index = shape_index_r if is_right else shape_index_l

                            bones.append({
                                'joint':        joint,
                                'segment':      segment,
                                'shape':        shape,
                                'joint_name':   joint_name,
                                'segment_name': seg_name,
                                'shape_index':  current_shape_index,
                                'side':         side,
                                'centroid':     centroid,
                                'num_verts':    len(verts),
                                'vertices':     verts,
                            })

                            if is_right:
                                shape_index_r += 1
                            else:
                                shape_index_l += 1

    segment_map = {}

    for bone in bones:
        # 1. Infer distance to closest joint
        name, dist = nearest_joint(bone['centroid'], HANIM_HAND_JOINTS)

        # 2. Try looking it up in the explicit manual maps
        mapped_name = None
        if bone['side'] == 'r':
            mapped_name = SHAPE_TO_JOINT_MAP.get(bone['shape_index'])
        elif bone['side'] == 'l':
            mapped_name = SHAPE_TO_JOINT_MAP_LEFT.get(bone['shape_index'])

        if mapped_name is not None:
            name = mapped_name
        else:
            name = f"{name}_{bone['shape_index']}"

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
            touch_sensor.set('description', new_segment_name)
            touch_sensor.tail = "\n"
            touch_sensor.text = "\n"

            segment_map[name] = new_segment

        new_segment.append(bone['shape'])
        parent_map[bone['shape']].remove(bone['shape'])

    writeXML(root, "LaughingUpperSkeletonHands.x3d", ".")

    return bones


bones = parse_x3d_hand('ScaledLaughingUpperSkeleton.x3d')

print("\n--- Processing Results ---")
for b in bones:
    print(
        f"Hand: {b['side'].upper()} | Shape {b['shape_index']:2d} | "
        f"Centroid: ({b['centroid'][0]:6.2f}, {b['centroid'][1]:6.2f}, {b['centroid'][2]:6.2f}) | "
        f"-> {b['inferred_bone']:15s} std loc {HANIM_HAND_JOINTS.get(b['inferred_bone'], 'N/A')} (dist: {b['match_distance_cm']} cm)"
    )
