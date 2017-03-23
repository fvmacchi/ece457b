import os
import dicom
from subject import Subject
import dicom_to_png
import uuid
import json

output_path = os.path.abspath("./PNG_IMAGES/")
metatdata_file = "metadata.json"
metatdata_file = os.path.join(output_path, metatdata_file)
path = os.path.abspath("./LIDC-IDRI/")

CROPPING_PADDING = 5

nodules = []
num_nodule_images = 0

# Construct list of nodules
for subject_folder in os.listdir(path):
    if not subject_folder.startswith("LIDC"):
        continue
    subject = Subject(subject_folder, os.path.join(path, subject_folder))
    subject.load_study_instances()
    for study_instance in subject.get_study_instances():
        for reading_session in study_instance.get_reading_sessions():
            # skip small nodules
            ns = filter(lambda x: not x.is_small(), reading_session.get_nodules())
            nodules.extend(ns)
            for nodule in ns:
                num_nodule_images += len(nodule.get_images())

print str(len(nodules)) + " nodules discovered."
print str(num_nodule_images) + " nodule images discovered."

if not os.path.exists(output_path):
    os.makedirs(output_path)
if not os.path.exists(metatdata_file):
    with open(metatdata_file, 'w') as f:
        f.write("{}")

with open(metatdata_file, 'r') as f:
    metadata = f.read()
    metadata = json.loads(metadata)

def save_metadata():
    with open(metatdata_file, 'w') as f:
        f.write(json.dumps(metadata, indent=4))

nodule_image_number = 0
for nodule_number, nodule in enumerate(nodules):
    
    identifier = nodule.id + "." + nodule.reading_session.id + "." + nodule.reading_session.study_instance.id + "." + nodule.reading_session.study_instance.subject.id
    if identifier in metadata:
        nodule_image_number += len(nodule.get_images())
        continue
    
    print "Extracting nodule " + str(nodule_number+1) + " of " + str(len(nodules))
    
    for nodule_image in nodule.get_images():
        png_file = None
        nodule_image_number += 1
        print "Extracting nodule image " + str(nodule_image_number) + " of " + str(num_nodule_images)
        try:
            # Add padding to boundary
            boundary = nodule_image.get_rectangle_boundary()
            boundary['x'] = max(0, boundary['x'] - CROPPING_PADDING)
            boundary['y'] = max(0, boundary['y'] - CROPPING_PADDING)
            boundary['width'] += CROPPING_PADDING + min(boundary['x'], CROPPING_PADDING)
            boundary['height'] += CROPPING_PADDING + min(boundary['y'], CROPPING_PADDING)
            
            while True:
                png_id = str(uuid.uuid4())
                output_file = os.path.join(output_path, png_id + ".png")
                if not os.path.exists(output_file):
                    break
            png_file = output_file
            
            if not identifier in metadata:
                metadata[identifier] = {'images':[]}
            metadata[identifier]['images'].append(png_id)
            metadata[identifier]['malignancy'] = nodule.malignancy
            metadata[identifier]['lobulation'] = nodule.lobulation
            metadata[identifier]['spiculation'] = nodule.spiculation
            metadata[identifier]['calcification'] = nodule.calcification
            
            dicom_to_png.convert_file(nodule_image.get_file(), png_file, x=boundary['x'], y=boundary['y'], width=boundary['width'], height=boundary['height'])
        
            
        except KeyboardInterrupt:
            if identifier in metadata:
                for image_id in metadata[identifier]['images']:
                    image_file = os.path.join(output_path, image_id + ".png")
                    if os.path.exists(image_file):
                        os.remove(image_file)
                del metadata[identifier]
            save_metadata()
            raise
save_metadata()
print "Done extracting images"
                
                