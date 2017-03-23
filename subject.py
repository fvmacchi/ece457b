import os
import xml_parser
from dicom_to_numpy import DicomArray

class Subject:
    
    def __init__(self, id, path):
        self.id = id
        self.path = path
        self.study_instances = {}
    
    def load_study_instances(self):
        for study_instance_path in filter(lambda d: not d.startswith('.'), os.listdir(self.path)):
            study_instance_id = study_instance_path
            study_instance_path = os.path.join(self.path, study_instance_path)
            
            study_instance = StudyInstance(study_instance_id, study_instance_path)
            study_instance.subject = self
            study_instance.load()
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
        self.valid = True
        self.subject = None
        self.reading_sessions = []
        
    
    def load(self):
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
        
        self.reading_sessions = xml_data['readingSession']
        for reading_session in self.reading_sessions:
            reading_session.study_instance = self
        
        self.valid = True
    
    def is_valid(self):
        return self.valid
    
    def get_reading_sessions(self):
        return self.reading_sessions
    
    def get_dicom_array(self):
        return self.dicom_array
        

class ReadingSession:
    def __init__(self, id):
        self.id = str(id)
        self.nodules = []
    
    def get_nodules(self):
        return self.nodules
    
    def add_nodule(self, nodule):
        self.nodules.append(nodule)
            
                
class Nodule:
    def __init__(self, id):
        self.id = id
        self.images = []
        self.malignancy = None
        self.lobulation = None
        self.spiculation = None
        self.calcification = None
    
    def is_small(self):
        return self.images[0].is_small()
    
    def get_images(self):
        return self.images
    
    def add_image(self, image):
        self.images.append(image)
    
    def draw_nodule_edge_images(self, plt, image_numbers=None):
        if image_numbers == None:
            image_numbers = range(len(self.images))
        
        for num in image_numbers:
            if num >= len(self.images):
                continue
            self.images[num].draw_edges(plt)
        
class NoduleImage:
    def __init__(self, id):
        self.id = id
        self.nodule = None
        self.dicom_array = None
    
    def set_edge_map(self, edge_map):
        self.edge_map = edge_map
    
    def is_small(self):
        return len(self.edge_map['x']) == 1
    
    def get_rectangle_boundary(self):
        min_x = min(self.edge_map['x'])
        max_x = max(self.edge_map['x'])
        min_y = min(self.edge_map['y'])
        max_y = max(self.edge_map['y'])
        return {'x': min_x, 'y': min_y, 'width': max_x-min_x+1, 'height': max_y-min_y+1}
    
    def _get_dicom_array(self):
        if self.dicom_array == None:
            self.dicom_array = self.nodule.reading_session.study_instance.get_dicom_array()
        return self.dicom_array
    
    def get_file(self):
        return self._get_dicom_array().find_image_uid(self.id)
    
    def draw_edges(self, plt):
        d_file = self.get_file()
        figure = self._get_dicom_array().plot_dicom(plt, d_file)
        self._get_dicom_array().drawEdgeMap(plt, self.edge_map['x'], self.edge_map['y'])
        