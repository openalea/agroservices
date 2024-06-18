


from agroservices.phis.phis import Phis
PAGE_SIZE_ALL = 10000

class Phis_UI(Phis):
    def __init__(self):
        super().__init__()
        self.token, _ =self.authenticate() 
        self.devices_all = None


    def get_device_details(self, device_name):
        if self.devices_all == None:
            self.devices_all = phis_ui.get_device(page_size=PAGE_SIZE_ALL)
        for item in self.devices_all['result']:
            if item['name'] == device_name:
                return item
        return None
    
    
phis_ui = Phis_UI()

#get all devices and print names
phis_ui.devices_all = phis_ui.get_device(page_size=PAGE_SIZE_ALL)
for item in phis_ui.devices_all['result']:
    print(item['name'])
print()

#show device details by name
emb7_details = phis_ui.get_device_details('Emb_7')
print(emb7_details)