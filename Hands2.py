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

# Mapping for the Right Hand to HAnim 2.0 Joint Names
SHAPE_TO_JOINT_MAP = {
    0:  'r_distal_interphalangeal_4',   1:  'r_distal_interphalangeal_3',   2:  'r_proximal_interphalangeal_4', 
    3:  'r_distal_interphalangeal_4',   4:  'r_distal_interphalangeal_4',   5:  'r_distal_interphalangeal_3', 
    6:  'r_proximal_interphalangeal_3', 7:  'r_distal_interphalangeal_5',   8:  'r_distal_interphalangeal_2', 
    9:  'r_proximal_interphalangeal_2', 10: 'r_metacarpophalangeal_3',      11: 'r_metacarpophalangeal_4', 
    12: 'r_proximal_interphalangeal_5', 13: 'r_interphalangeal_1',          14: 'r_metacarpophalangeal_2', 
    15: 'r_carpometacarpal_3',          16: 'r_carpometacarpal_4',          17: 'r_carpometacarpal_5', 
    18: 'r_metacarpophalangeal_2',      19: 'r_carpometacarpal_2',          20: 'r_carpometacarpal_2', 
    21: 'r_carpometacarpal_3',          22: 'r_metacarpophalangeal_1',      23: 'r_carpometacarpal_1', 
    24: 'r_carpometacarpal_1',          25: 'r_carpometacarpal_1',          26: 'r_carpometacarpal_2',
}

# Mapping for the Left Hand
SHAPE_TO_JOINT_MAP_LEFT = {k: v.replace('r_', 'l_') for k, v in SHAPE_TO_JOINT_MAP.items()}

# HAnim 2.0 standard mapping to properly name Segment tags based on the Joint
HANIM_JOINT_TO_SEGMENT = {
    'carpometacarpal_1': 'metacarpal_1',            'metacarpophalangeal_1': 'proximal_phalanx_1',      'interphalangeal_1': 'distal_phalanx_1',
    'carpometacarpal_2': 'metacarpal_2',            'metacarpophalangeal_2': 'proximal_phalanx_2',      'proximal_interphalangeal_2': 'middle_phalanx_2',      'distal_interphalangeal_2': 'distal_phalanx_2',
    'carpometacarpal_3': 'metacarpal_3',            'metacarpophalangeal_3': 'proximal_phalanx_3',      'proximal_interphalangeal_3': 'middle_phalanx_3',      'distal_interphalangeal_3': 'distal_phalanx_3',
    'carpometacarpal_4': 'metacarpal_4',            'metacarpophalangeal_4': 'proximal_phalanx_4',      'proximal_interphalangeal_4': 'middle_phalanx_4',      'distal_interphalangeal_4': 'distal_phalanx_4',
    'carpometacarpal_5': 'metacarpal_5',            'metacarpophalangeal_5': 'proximal_phalanx_5',      'proximal_interphalangeal_5': 'middle_phalanx_5',      'distal_interphalangeal_5': 'distal_phalanx_5',
}

# H-Anim 2.0 standard joint centers for both hands (approximate, in meters)
HANIM_HAND_JOINTS = {
    # RIGHT HAND
    'r_carpometacarpal_1':          (-0.19,  0.93,  0.02),
    'r_metacarpophalangeal_1':      (-0.21,  0.94,  0.03),
    'r_interphalangeal_1':          (-0.22,  0.95,  0.03),
    'r_carpometacarpal_2':          (-0.20,  0.95,  0.01),
    'r_metacarpophalangeal_2':      (-0.20,  0.97,  0.01),
    'r_proximal_interphalangeal_2': (-0.20,  0.99,  0.01),
    'r_distal_interphalangeal_2':   (-0.20,  1.01,  0.01),
    'r_carpometacarpal_3':          (-0.18,  0.95,  0.00),
    'r_metacarpophalangeal_3':      (-0.18,  0.97,  0.00),
    'r_proximal_interphalangeal_3': (-0.18,  0.99,  0.00),
    'r_distal_interphalangeal_3':   (-0.18,  1.01,  0.00),
    'r_carpometacarpal_4':          (-0.16,  0.95, -0.01),
    'r_metacarpophalangeal_4':      (-0.16,  0.97, -0.01),
    'r_proximal_interphalangeal_4': (-0.16,  0.99, -0.01),
    'r_distal_interphalangeal_4':   (-0.16,  1.01, -0.01),
    'r_carpometacarpal_5':          (-0.14,  0.95, -0.02),
    'r_metacarpophalangeal_5':      (-0.14,  0.97, -0.02),
    'r_proximal_interphalangeal_5': (-0.14,  0.99, -0.02),
    'r_distal_interphalangeal_5':   (-0.14,  1.01, -0.02),

    # LEFT HAND (X-axis mirrored)
    'l_carpometacarpal_1':          ( 0.19,  0.93,  0.02),
    'l_metacarpophalangeal_1':      ( 0.21,  0.94,  0.03),
    'l_interphalangeal_1':          ( 0.22,  0.95,  0.03),
    'l_carpometacarpal_2':          ( 0.20,  0.95,  0.01),
    'l_metacarpophalangeal_2':      ( 0.20,  0.97,  0.01),
    'l_proximal_interphalangeal_2': ( 0.20,  0.99,  0.01),
    'l_distal_interphalangeal_2':   ( 0.20,  1.01,  0.01),
    'l_carpometacarpal_3':          ( 0.18,  0.95,  0.00),
    'l_metacarpophalangeal_3':      ( 0.18,  0.97,  0.00),
    'l_proximal_interphalangeal_3': ( 0.18,  0.99,  0.00),
    'l_distal_interphalangeal_3':   ( 0.18,  1.01,  0.00),
    'l_carpometacarpal_4':          ( 0.16,  0.95, -0.01),
    'l_metacarpophalangeal_4':      ( 0.16,  0.97, -0.01),
    'l_proximal_interphalangeal_4': ( 0.16,  0.99, -0.01),
    'l_distal_interphalangeal_4':   ( 0.16,  1.01, -0.01),
    'l_carpometacarpal_5':          ( 0.14,  0.95, -0.02),
    'l_metacarpophalangeal_5':      ( 0.14,  0.97, -0.02),
    'l_proximal_interphalangeal_5': ( 0.14,  0.99, -0.02),
    'l_distal_interphalangeal_5':   ( 0.14,  1.01, -0.02),
}

def get_standard_segment_name(joint_name):
    """Derive standard HAnim 2.0 segment name from joint name."""
    prefix = joint_name[:2]  # e.g., 'r_' or 'l_'
    base_joint = joint_name[2:]
    if base_joint in HANIM_JOINT_TO_SEGMENT:
        return prefix + HANIM_JOINT_TO_SEGMENT[base_joint]
    return f"{joint_name}_segment" # Fallback

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
            # Create Joint tag
            new_joint = xml.etree.ElementTree.SubElement(bone['joint'], "HAnimJoint")
            new_joint_name = name
            new_joint.set('DEF', 'Joe_'+new_joint_name)
            new_joint.set('name', new_joint_name)
            new_joint.tail = "\n"
            new_joint.text = "\n"

            # Create standard Segment tag (e.g. 'r_proximal_phalanx_2' instead of 'r_metacarpophalangeal_2_segment')
            new_segment = xml.etree.ElementTree.SubElement(new_joint, "HAnimSegment")
            new_segment_name = get_standard_segment_name(new_joint_name)
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
        f"-> {b['inferred_bone']:28s} std loc {HANIM_HAND_JOINTS.get(b['inferred_bone'], 'N/A')} (dist: {b['match_distance_cm']} cm)"
    )
