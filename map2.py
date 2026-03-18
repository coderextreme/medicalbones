import pandas as pd
import xml.etree.ElementTree as ET

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
input_x3d = "skeleton1_hanim.x3d"
mapping_csv = "loa4_mapping_result.csv"
output_x3d = "skeleton1_hanim_LOA4.x3d"

# ------------------------------------------------------------
# Utility
# ------------------------------------------------------------
def local_tag(tag):
    return tag.split("}")[-1]

# ------------------------------------------------------------
# 1. Load Mapping CSV
# ------------------------------------------------------------
mapping_df = pd.read_csv(mapping_csv)

# Build dictionary: original_name -> loa4_name
name_map = {}

for _, row in mapping_df.iterrows():
    file_joint = str(row["file_joint"]).strip()
    mapped_name = str(row["mapped_name"]).strip()

    if mapped_name and mapped_name != "nan":
        name_map[file_joint] = mapped_name

print(f"Loaded {len(name_map)} mapping entries.")

# ------------------------------------------------------------
# 2. Parse X3D
# ------------------------------------------------------------
tree = ET.parse(input_x3d)
root = tree.getroot()

# Track DEF renaming for fixing USE later
def_map = {}   # old_DEF -> new_DEF

# ------------------------------------------------------------
# 3. Rename DEF and name attributes
# ------------------------------------------------------------
for elem in root.iter():
    tag = local_tag(elem.tag)

    if tag in ("HAnimJoint", "HAnimSegment"):

        old_name = elem.attrib.get("name")
        old_def = elem.attrib.get("DEF")

        if old_name in name_map:
            new_name = name_map[old_name]

            # Replace name attribute
            elem.set("name", new_name)

            # Replace DEF if present
            if old_def:
                elem.set("DEF", new_name)
                def_map[old_def] = new_name

# ------------------------------------------------------------
# 4. Fix all USE references
# ------------------------------------------------------------
for elem in root.iter():
    if "USE" in elem.attrib:
        old_use = elem.attrib["USE"]
        if old_use in def_map:
            elem.set("USE", def_map[old_use])

# ------------------------------------------------------------
# 5. Write Output
# ------------------------------------------------------------
tree.write(output_x3d, encoding="utf-8", xml_declaration=True)

print("LOA4 remapping complete.")
print(f"Output written to: {output_x3d}")
