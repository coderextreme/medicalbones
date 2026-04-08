import pandas as pd
import xml.etree.ElementTree as ET

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------
excel_path = "hanim_loa4_mapping.xlsx"
x3d_path = "0scaled/0skeleton1scaled.x3d"

# ---------------------------------------------------------------------
# 1. Load Spreadsheet (row 1 contains actual headers)
# ---------------------------------------------------------------------
df = pd.read_excel(excel_path, header=1)

df = df.rename(columns={
    "File Joint Name": "file_joint",
    "X3D HAnim LOA4 Joint": "loa4_joint",
    "Suggested LOA4 Segment Name": "loa4_segment",
    "Mapping Status": "status"
})

df = df[["file_joint", "loa4_joint", "loa4_segment", "status"]]

# Clean whitespace
df["file_joint"] = df["file_joint"].astype(str).str.strip()
df["loa4_joint"] = df["loa4_joint"].astype(str).str.strip()
df["loa4_segment"] = df["loa4_segment"].astype(str).str.strip()

# ---------------------------------------------------------------------
# 2. Parse X3D File
# ---------------------------------------------------------------------
tree = ET.parse(x3d_path)
root = tree.getroot()

hanim_joints = set()
hanim_segments = set()

for elem in root.iter():
    tag = elem.tag.split("}")[-1]
    if tag == "HAnimJoint" and "name" in elem.attrib:
        hanim_joints.add(elem.attrib["name"])
    if tag == "HAnimSegment" and "name" in elem.attrib:
        hanim_segments.add(elem.attrib["name"])

# ---------------------------------------------------------------------
# 3. Build Mapping
# ---------------------------------------------------------------------
mapping_results = []

for _, row in df.iterrows():
    file_joint = row["file_joint"]
    loa4_joint = row["loa4_joint"]
    loa4_segment = row["loa4_segment"]

    mapped_name = None
    mapped_type = None
    exists_in_x3d = False

    # Prefer LOA4 joint if defined
    if loa4_joint and loa4_joint.lower() != "none – extension" and loa4_joint.lower() != "none":
        mapped_name = loa4_joint
        mapped_type = "HAnimJoint"
        exists_in_x3d = mapped_name in hanim_joints

    # Otherwise use segment mapping
    elif loa4_segment and loa4_segment.lower() != "none":
        mapped_name = loa4_segment
        mapped_type = "HAnimSegment"
        # account for common "_seg" suffix in file
        exists_in_x3d = (
            mapped_name in hanim_segments or
            f"hanim_segment_{mapped_name}" in hanim_segments
        )

    mapping_results.append({
        "file_joint": file_joint,
        "mapped_name": mapped_name,
        "mapped_type": mapped_type,
        "exists_in_skeleton1_hanim": exists_in_x3d
    })

mapping_df = pd.DataFrame(mapping_results)

# ---------------------------------------------------------------------
# 4. Output Results
# ---------------------------------------------------------------------
print("\n=== Mapping Summary ===")
print(mapping_df.head(20))

# Optional: Save result
mapping_df.to_csv("0loa4_mapping_result.csv", index=False)

# Optional: dictionary form
mapping_dict = {
    row["file_joint"]: row["mapped_name"]
    for _, row in mapping_df.iterrows()
    if row["mapped_name"] is not None
}

print("\nTotal mapped joints:", len(mapping_dict))
