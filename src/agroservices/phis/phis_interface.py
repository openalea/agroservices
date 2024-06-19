


from agroservices.phis.phis import Phis
PAGE_SIZE_ALL = 10000

class Phis_UI(Phis):
    def __init__(self):
        super().__init__()
        self.device_all = None
        self.scientific_object_all = None
        self.experiment_all = None
        self.variable_all = None
        self.project_all = None
        self.facility_all = None
        self.germplasm_all = None
        self.annotation_all = None
        self.document_all = None
        self.factor_all = None


    def get_device_user(self, device_name=None):
        if self.device_all == None:
            self.device_all = self.get_device(page_size=PAGE_SIZE_ALL)
        
        if device_name == None:
            list = []
            for item in self.device_all['result']:
                list.append(item['name'])
            return list
        
        else:
            for item in self.device_all['result']:
                if item['name'] == device_name:
                    return item
        return None
    

    def get_scientific_object_user(self, scientific_object_name=None):
        if self.scientific_object_all == None:
            self.scientific_object_all = self.get_scientific_object(page_size=PAGE_SIZE_ALL)
        
        if scientific_object_name == None:
            list = []
            for item in self.scientific_object_all['result']:
                list.append(item['name'])
            return list
        
        else:
            for item in self.scientific_object_all['result']:
                if item['name'] == scientific_object_name:
                    return item
        return None
    

    def get_experiment_user(self, experiment_name=None):
        if self.experiment_all == None:
            self.experiment_all = self.get_experiment(page_size=PAGE_SIZE_ALL)
        
        if experiment_name == None:
            list = []
            for item in self.experiment_all['result']:
                list.append(item['name'])
            return list
        
        else:
            for item in self.experiment_all['result']:
                if item['name'] == experiment_name:
                    return item
        return None
    

    def get_variable_user(self, variable_name=None):
        if self.variable_all == None:
            self.variable_all = self.get_variable(page_size=PAGE_SIZE_ALL)
        
        if variable_name == None:
            list = []
            for item in self.variable_all['result']:
                list.append(item['name'])
            return list
        
        else:
            for item in self.variable_all['result']:
                if item['name'] == variable_name:
                    return item
        return None
    

    def get_project_user(self, project_name=None):
        if self.project_all == None:
            self.project_all = self.get_project(page_size=PAGE_SIZE_ALL)
        
        if project_name == None:
            list = []
            for item in self.project_all['result']:
                list.append(item['name'])
            return list
        
        else:
            for item in self.project_all['result']:
                if item['name'] == project_name:
                    return item
        return None
    

    def get_facility_user(self, facility_name=None):
        if self.facility_all == None:
            self.facility_all = self.get_facility(page_size=PAGE_SIZE_ALL)
        
        if facility_name == None:
            list = []
            for item in self.facility_all['result']:
                list.append(item['name'])
            return list
        
        else:
            for item in self.facility_all['result']:
                if item['name'] == facility_name:
                    return item
        return None
    

    def get_germplasm_user(self, germplasm_name=None):
        if self.germplasm_all == None:
            self.germplasm_all = self.get_germplasm(page_size=PAGE_SIZE_ALL)
        
        if germplasm_name == None:
            list = []
            for item in self.germplasm_all['result']:
                list.append(item['name'])
            return list
        
        else:
            for item in self.germplasm_all['result']:
                if item['name'] == germplasm_name:
                    return item
        return None
    

    def get_annotation_user(self, annotation_name=None):
        if self.annotation_all == None:
            self.annotation_all = self.get_annotation(page_size=PAGE_SIZE_ALL)
        
        if annotation_name == None:
            list = []
            for item in self.annotation_all['result']:
                list.append(item['name'])
            return list
        
        else:
            for item in self.annotation_all['result']:
                if item['name'] == annotation_name:
                    return item
        return None
    

    def get_document_user(self, document_name=None):
        if self.document_all == None:
            self.document_all = self.get_document(page_size=PAGE_SIZE_ALL)
        
        if document_name == None:
            list = []
            for item in self.document_all['result']:
                list.append(item['name'])
            return list
        
        else:
            for item in self.document_all['result']:
                if item['name'] == document_name:
                    return item
        return None
    

    def get_factor_user(self, factor_name=None):
        if self.factor_all == None:
            self.factor_all = self.get_factor(page_size=PAGE_SIZE_ALL)
        
        if factor_name == None:
            list = []
            for item in self.factor_all['result']:
                list.append(item['name'])
            return list
        
        else:
            for item in self.factor_all['result']:
                if item['name'] == factor_name:
                    return item
        return None


    
phis_ui = Phis_UI()

#get all devices and print names
for item in phis_ui.get_device_user():
    print(item)

print()
#show device details by name
emb7_details = phis_ui.get_device_user('Emb_7')
print(emb7_details)

print()
#get all scientific objects and print names
for item in phis_ui.get_scientific_object_user():
    print(item)

print()
#show scientific object details by name
object_details = phis_ui.get_scientific_object_user('0587/ZM4523/DZ_PG_74/WW/PGe_Rep_2/10_47/ARCH2020-02-03')
print(object_details)