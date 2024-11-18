import xml.etree.ElementTree as ET
from PIL import Image
import os
import argparse

class AltoParser:
    def __init__(self, xml_file_path):
        self.tree = ET.parse(xml_file_path)
        self.root = self.tree.getroot()
        # Extracting the namespace from the XML file
        namespace_uri = self.root.tag.split('}')[0].strip('{')
        self.ns = {'alto': namespace_uri}

    def parse_text_lines(self):
        for text_line in self.root.findall('.//alto:TextLine', self.ns):
            hpos = int(text_line.get('HPOS'))
            vpos = int(text_line.get('VPOS'))
            width = int(text_line.get('WIDTH'))
            height = int(text_line.get('HEIGHT'))
            # To concatenate all the strings in a line
            line_text = ' '.join([string.get('CONTENT') for string in text_line.findall('alto:String', self.ns)])
            yield hpos, vpos, width, height, line_text

class ImageCropper:
    def __init__(self, image_path, output_dir):
        self.image_path = image_path
        self.output_dir = output_dir

    def crop_and_save_text(self, text_line_data, sub_output_dir):
        os.makedirs(sub_output_dir, exist_ok=True)  # Create sub-directory if it doesn't exist
        for i, (hpos, vpos, width, height, line_text) in enumerate(text_line_data):
            # Open the original image
            with Image.open(self.image_path) as img:
                # Define the bounding box for cropping
                bbox = (hpos, vpos, hpos + width, vpos + height)
                # Crop the image
                cropped_img = img.crop(bbox)
                # Save the cropped image
                cropped_img.save(f'{sub_output_dir}/line_{i}.png')
                # Save the text
                with open(f'{sub_output_dir}/line_{i}.txt', 'w') as text_file:
                    text_file.write(line_text)

def process_pair(xml_file_path, image_file_path, output_dir):
    parser = AltoParser(xml_file_path)
    text_line_data = parser.parse_text_lines()

    cropper = ImageCropper(image_file_path, output_dir)
    sub_output_dir = os.path.join(output_dir, os.path.basename(image_file_path).split('.')[0])
    cropper.crop_and_save_text(text_line_data, sub_output_dir)

def main(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)  # Create output directory if it doesn't exist

    # Supported image extensions
    image_extensions = ['.tif', '.jpeg', '.jpg', '.png']

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.xml'):
            xml_file_path = os.path.join(input_directory, file_name)
            base_name = file_name.replace('.xml', '')
            
            # Check for any matching image file with supported extensions
            image_file_path = None
            for ext in image_extensions:
                potential_image_path = os.path.join(input_directory, base_name + ext)
                if os.path.exists(potential_image_path):
                    image_file_path = potential_image_path
                    break

            # If an image file is found, process the pair
            if image_file_path:
                process_pair(xml_file_path, image_file_path, output_directory)
            else:
                print(f"No matching image file found for {file_name}")

# python parse_alto_xml.py --input <input-directory> --output <output-directory>
# python parse_alto_xml.py --input data --output output
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process ALTO-XML files and images.')
    parser.add_argument('--input', dest='input_directory', default='data', help='Input directory containing ALTO-XML files and images.')
    parser.add_argument('--output', dest='output_directory', default='output', help='Output directory for cropped images and text.')
    args = parser.parse_args()
    
    main(args.input_directory, args.output_directory)
    print("Done.")