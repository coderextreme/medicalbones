import xml.etree.ElementTree as ET
import numpy as np

def parse_x3d_hand(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    parent_map = {c: p for p in root.iter() for c in p}

    bones = []

    for joint in root.iter('HAnimJoint'):
        joint_name   = joint.get('name') or joint.get('DEF', 'unnamed')
        joint_center = joint.get('center', '0 0 0')
        center_xyz   = tuple(float(v) for v in joint_center.split())

        for segment in joint.findall('HAnimSegment'):
            seg_name = segment.get('name') or segment.get('DEF', 'unnamed')

            # Collect all IFS meshes within this segment
            shapes = list(segment.iter('IndexedFaceSet'))
            print(f"\nJoint: {joint_name}  |  Segment: {seg_name}")
            print(f"  Joint center: {center_xyz}")
            print(f"  IFS mesh count: {len(shapes)}")

            for i, ifs in enumerate(shapes):
                coord_node = ifs.find('Coordinate')
                if coord_node is None:
                    continue

                pts = [float(v) for v in coord_node.get('point', '').split()]
                verts = np.array(pts).reshape(-1, 3)
                centroid = verts.mean(axis=0)

                bones.append({
                    'joint_name':   joint_name,
                    'segment_name': seg_name,
                    'shape_index':  i,
                    'centroid':     centroid,
                    'num_verts':    len(verts),
                    'vertices':     verts,
                })

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

bones = assign_bone_names(bones)

for b in bones:
    print(
        f"Shape {b['shape_index']:2d} | "
        f"Centroid: ({b['centroid'][0]:6.2f}, {b['centroid'][1]:6.2f}, {b['centroid'][2]:6.2f}) | "
        f"-> {b['inferred_bone']:15s} std loc {HANIM_HAND_JOINTS[b['inferred_bone']]} (dist: {b['match_distance_cm']} cm)"
    )

