import pytest
from urllib.request import urlopen
from agroservices.ipm import IPM

def test_url():
    ipm = IPM()
    assert ipm.url is not None
    try:
        urlopen(ipm.url)
    except Exception as err:
        assert False, err
    else:
        assert True
    

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)
    

################# MetaDataService ################################# 

def test_get_parameter():
    ipm=IPM()
    res = ipm.get_parameter()
    assert type(res) is list
    assert keys_exists(res[0],('id','name','description','unit'))

def test_get_qc():
    ipm=IPM()
    res = ipm.get_qc()
    assert type(res) is list 
    assert keys_exists(res[0],('id','name','description'))

def test_get_schema_weatherdata():
    ipm=IPM()
    res = ipm.get_schema_weatherdata()
    assert type(res) is dict

def test_post_schema_weatherdata_validate():
    ipm = IPM()
    res = ipm.post_schema_weatherdata_validate(jsonfile='weather_data.json')
    assert type(res) is dict
    assert res["isValid"]==True   

def test_get_schema_fieldobservation():
    ipm=IPM()
    res = ipm.get_schema_fieldobservation()
    assert type(res) is dict
    

def test_get_schema_modeloutput():
    ipm=IPM()
    res = ipm.get_schema_modeloutput()
    assert res is not None 
    assert type(res) is dict

def test_post_schema_modeloutput_validate():
    ipm=IPM()
    res = ipm.post_schema_modeloutput_validate(jsonfile='modeloutput.json')
    assert type(res) is dict
    assert res['isValid']==True

######################### WeatherAdaptaterService #######################


#################### DSSService ####################################################

def test_get_crop():
    ipm=IPM()
    res = ipm.get_crop()
    assert type(res) is list

def test_get_cropCode():
    ipm=IPM()
    res = ipm.get_cropCode(cropCode="DAUCS")
    assert type(res) is list
    assert keys_exists(res[0],('models','id','version','name','url','languages','organization'))
    assert res[0]['models'][0]['crops']==['DAUCS']

def test_get_dss():
    ipm=IPM()
    res = ipm.get_dss()
    assert type(res) is list
    assert keys_exists(res[0],('models','id','version','name','url','languages','organization'))


def test_get_dssId():
    ipm=IPM()
    res = ipm.get_dssId(DSSId='no.nibio.vips')
    assert type(res) is dict
    assert keys_exists(res.keys(),('models','id','version','name','url','languages','organization'))
    assert res['id']=='no.nibio.vips'

def test_get_model():
    ipm=IPM()
    res = ipm.get_model(DSSId='no.nibio.vips',ModelId='PSILARTEMP')
    assert type(res) is dict
    assert keys_exists(res.keys(),('name', 'id', 'version', 'type_of_decision', 'type_of_output', 'description_URL', 'description', 'citation', 'keywords', 'pests', 'crops', 'authors', 'execution', 'input', 'valid_spatial', 'output'))
    assert res['id']== 'PSILARTEMP'

def test_get_pest():
    ipm=IPM()
    res = ipm.get_pest()
    assert type(res) is list

def test_get_pestCode():
    ipm=IPM()
    res = ipm.get_pestCode(pestCode='PSILRO')
    assert type(res) is list
    assert keys_exists(res[0],('models','id','version','name','url','languages','organization'))
    assert res[0]['models'][0]['pests'] == ['PSILRO'] 

""" Move to test_weatherdata: Need to be fixed
def test_get_dss_location():
    ipm=IPM()
    res = ipm.get_dss_location_point(latitude=59.67883523696076, longitude=12.01629638671875)
    assert type(res) is list
    assert keys_exists(res[0],('models','id','version','name','url','languages','organization'))

def test_post_dss_location():
    ipm = IPM()
    res= ipm.post_dss_location(geoJsonfile="GeoJson.json")
    assert type(res) is list
    assert keys_exists(res[0].keys(), (
        'models', 
        'id', 
        'version', 
        'name', 
        'url', 
        'languages', 
        'organization')
        )
"""