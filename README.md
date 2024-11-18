# alto-xml-parser

ALTO XML parser for Handwritten Text Recognition (HTR). Extract cropped line images with their corresponding text.

## Environment Setup (or venv etc.)

    conda create -n alto-xml python=3.9

## Dependencies

    conda activate alto-xml
    pip install -r requirements.txt

## Run

Place files inside `data` directory (eg. .xml and .tif files).

### Parse files to get cropped line images and the corresponding text in `output`

    python parse_alto_xml.py --input data --output output
