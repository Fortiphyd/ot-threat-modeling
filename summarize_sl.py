
import zipfile
from lxml import etree
from collections import defaultdict
import argparse

def summarize_security_levels(tm7_path):
    sl_selected_counts = defaultdict(int)

    # Try to open the file as a plain XML file
    try:
        with open(tm7_path, "rb") as f:
            xml_root = etree.parse(f).getroot()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    for elem in xml_root.iter():
        if (
            etree.QName(elem).localname == "DisplayName"
            and elem.text
            and elem.text.endswith("Security Level")
        ):
            parent = elem.getparent()
            selected_index = parent.find(".//{http://schemas.datacontract.org/2004/07/ThreatModeling.KnowledgeBase}SelectedIndex")
            value_block = parent.find(".//{http://schemas.datacontract.org/2004/07/ThreatModeling.KnowledgeBase}Value")

            if selected_index is not None and value_block is not None:
                strings = value_block.findall(".//{http://schemas.microsoft.com/2003/10/Serialization/Arrays}string")
                try:
                    selected = int(selected_index.text)
                    if 0 <= selected < len(strings):
                        selected_value = strings[selected].text
                        sl_selected_counts[selected_value] += 1
                except (ValueError, TypeError):
                    continue

    if not sl_selected_counts:
        print("No Security Level selections found.")
    else:
        print("Security Level Summary:")
        for level, count in sorted(sl_selected_counts.items()):
            print(f"  {level}: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize Security Levels from a Threat Modeling Tool .tm7 file.")
    parser.add_argument("tm7_file", help="Path to the .tm7 or XML file")

    args = parser.parse_args()
    summarize_security_levels(args.tm7_file)
