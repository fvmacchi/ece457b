import pprint as pp
import os

from dicom_to_numpy import DicomArray
from xml_parser import *
from subject import Subject
import matplotlib.pyplot as plt

### LIDC Dataset
subject_id = "LIDC-IDRI-0003"
path = os.path.abspath(os.path.join("./LIDC-IDRI/", subject_id))
subject = Subject(subject_id, path)
subject.load_study_instances()
study_instance = subject.get_study_instance("1.3.6.1.4.1.14519.5.2.1.6279.6001.101370605276577556143013894866")
for nodule in study_instance.get_reading_sessions()[0].get_nodules():
    nodule.draw_nodule_edge_images(plt, image_numbers=None)
plt.show()

