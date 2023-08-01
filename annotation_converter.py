import os
import xml.etree.ElementTree as ET

def convert_coordinates(size, box):
    width, height = size
    x_min, y_min, x_max, y_max = box
    x_center = (x_min + x_max) / (2.0 * width)
    y_center = (y_min + y_max) / (2.0 * height)
    w = (x_max - x_min) / width
    h = (y_max - y_min) / height
    return x_center, y_center, w, h

def convert_annotation(xml_file_path, classes):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    size_element = root.find('size')
    width = int(size_element.find('width').text)
    height = int(size_element.find('height').text)
    size = (width, height)
    
    boxes = []

    for obj in root.findall('object'):
        class_name = obj.find('name').text
        if class_name not in classes:
            continue

        class_id = classes.index(class_name)
        box = obj.find('bndbox')
        bbox = [
            int(box.find('xmin').text),
            int(box.find('ymin').text),
            int(box.find('xmax').text),
            int(box.find('ymax').text)
        ]
        boxes.append((class_id, bbox))

    if not boxes:
        return None

    with open(xml_file_path.replace('.xml', '.txt'), 'w') as out_file:
        for class_id, bbox in boxes:
            x_center, y_center, w, h = convert_coordinates(size, bbox)
            out_file.write(f"{class_id} {x_center} {y_center} {w} {h}\n")

if __name__ == "__main__":
    # List of class names in the order of their IDs in the YOLO format
    classes_list = ["not_empty", "empty"]

    # Path to the directory containing the XML annotation files
    annotation_dir = "annotations"

    for xml_file in os.listdir(annotation_dir):
        if xml_file.endswith(".xml"):
            xml_path = os.path.join(annotation_dir, xml_file)
            convert_annotation(xml_path, classes_list)
