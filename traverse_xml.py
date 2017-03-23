import os
import xml_parser

path = os.path.abspath("./LIDC-XML/")

max_width = 0
max_height = 0
num_xmls = 0
num_nodules = 0
num_images = 0

def process_xml(xml_file):
    global max_width, max_height, num_xmls, num_nodules, num_images
    data = xml_parser.parse_xml(xml_file)
    if data == False:
        return
    num_xmls += 1
    reading_sessions = data["readingSession"]
    for reading_session in [reading_sessions[0]]:
        num_nodules += len(reading_session.get_nodules())
        for nodule in reading_session.get_nodules():
            num_images += len(nodule.get_images())
            for nodule_image in nodule.get_images():
                boundary = nodule_image.get_rectangle_boundary()
                if boundary['width'] > max_width:
                    max_width = boundary['width']
                if boundary['height'] > max_height:
                    max_height = boundary['height']


# Recursively traverse all sub-folders in the path
for sub_folder, subdirs, files in os.walk(path):
    for f in os.listdir(sub_folder):
        file_path = os.path.join(sub_folder, f)

        # Make sure path is an actual file
        if os.path.isfile(file_path) and file_path.endswith(".xml"):

            process_xml(file_path)

print "Number of XMLs: " + str(num_xmls)
print "Number of Nodules: " + str(num_nodules)
print "Number of Images: " + str(num_images)
print "Maximum image width: " + str(max_width)
print "Maximum image height: " + str(max_height)
