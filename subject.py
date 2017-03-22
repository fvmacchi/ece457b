import os
import xml_parser
from dicom_to_numpy import DicomArray

class Subject:
    
    def __init__(self, id, path):
        self.id = id
        self.path = path
        self.study_instances = {}
        print self.path
        print self.id
    
    def load_study_instances(self):
        for study_instance_path in filter(lambda d: not d.startswith('.'), os.listdir(self.path)):
            study_instance_id = study_instance_path
            study_instance_path = os.path.join(self.path, study_instance_path)
            
            study_instance = StudyInstance(study_instance_id, study_instance_path)
            if not study_instance.is_valid():
                continue
            
            self.study_instances[study_instance.id] = study_instance
    
    def get_study_instances(self):
        return self.study_instances.values()
    
    def get_study_instance(self, study_instance_id):
        return self.study_instances[study_instance_id]

class StudyInstance:
    
    def __init__(self, id, path):
        self.id = id
        self.path = path
        self.valid = False
        # verify there is only 1 series under study_instance
        series_paths = filter(lambda d: not d.startswith('.'), os.listdir(self.path))
        if not len(series_paths) == 1:
            raise Exception('Number of series under study_instance is ' + str(len(series_paths)) + '. Change code to account for this case.')
        series_path = os.path.join(self.path, series_paths[0])
        xml_paths = filter(lambda d: (not d.startswith('.')) and d.endswith('.xml'), os.listdir(series_path))
        # verify there is only 1 xml in each series
        if not len(xml_paths) == 1:
            raise Exception('Number of xml files under series is ' + str(len(xml_paths)) + '. Change code to account for this case.')
        xml_path = os.path.join(series_path, xml_paths[0])
        xml_data = xml_parser.parse_xml(xml_path)
        if xml_data == False:
            self.valid = False
            return
        
        self.dicom_array = DicomArray()
        self.dicom_array.read_dicom(series_path)
        
        self.reading_sessions = []
        for reading_session in xml_data['readingSession']:
            self.reading_sessions.append(ReadingSession(self, reading_session))
        
        self.valid = True
    
    def is_valid(self):
        return self.valid
    
    def get_reading_sessions(self):
        return self.reading_sessions
    
    def get_dicom_array(self):
        return self.dicom_array
        

class ReadingSession:
    def __init__(self, study_instance, data):
        self.study_instance = study_instance
        self.nodules = []
        for nodule in data["nodules"]:
            nodule = Nodule(self, nodule)
            self.nodules.append(nodule)
    
    def get_nodules(self):
        return self.nodules
            
                
class Nodule:
    def __init__(self, reading_session, image_data):
        self.reading_session = reading_session
        self.images = []
        for image in image_data:
            image = NoduleImage(self, image)
            self.images.append(image)
    
    def draw_nodule_edge_images(self, plt, image_numbers=None):
        if image_numbers == None:
            image_numbers = range(len(self.images))
        
        for num in image_numbers:
            if num >= len(self.images):
                continue
            self.images[num].draw_edges(plt)
        
class NoduleImage:
    def __init__(self, nodule, data):
        self.nodule = nodule
        self.uid = data['image_uid']
        self.edge_map = data['edge_map']
        self.dicom_array = self.nodule.reading_session.study_instance.get_dicom_array()
    
    def draw_edges(self, plt):
        d_file = self.dicom_array.find_image_uid(self.uid)
        figure = self.dicom_array.plot_dicom(plt, d_file)
        self.dicom_array.drawEdgeMap(plt, self.edge_map['x'], self.edge_map['y'])
        