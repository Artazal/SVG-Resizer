import xml.etree.ElementTree as ET
from pathlib import Path

def enlarge_svg(input_file: str, target_width: int = 7000) -> str:
    tree = ET.parse(input_file)
    root = tree.getroot()

    viewbox = root.get("viewBox")
    if not viewbox:
        raise ValueError("The .SVG doesn't have viewBox. Proportions cannot be calculated safely.")

    parts = viewbox.replace(",", " ").split()
    if len(parts) != 4:
        raise ValueError(f"Strange viewBox format: {viewbox}")

    min_x, min_y, vb_width, vb_height = map(float, parts)

    if vb_width == 0:
        raise ValueError("The width of viewBox = 0")
    aspect_ratio = vb_height / vb_width
    target_height = round(target_width * aspect_ratio)

    root.set("width", str(target_width))
    root.set("height", str(target_height))

    input_path = Path(input_file)
    output_file = input_path.with_name(input_path.stem + "_" + str(target_width) + ".svg")
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    return str(output_file)

def enlarge_multiple_svgs(file_paths: list[str], target_width: int = 7000):
    results = []
    for file_path in file_paths:
        try:
            output = enlarge_svg(file_path, target_width)
            results.append((file_path, "OK", output))
        except Exception as e:
            results.append((file_path, "ERROR", str(e)))
    return results