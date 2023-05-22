import json
from urllib.request import urlopen
from agroservices.ipm.ipm import IPM
from agroservices.ipm.datadir import datadir

def test_url():
    ipm = IPM()
    assert ipm.url is not None
    try:
        urlopen(ipm.url)
    except Exception as err:
        assert False, err
    else:
        assert True

ipm_ok = False
if test_url():
    ipm = IPM()
    ipm_ok = True

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)
    

################# MetaDataService ################################# 



def test_get_parameter():
    if ipm_ok:
        res = ipm.get_parameter()
        assert type(res) is list
        assert keys_exists(res[0],('id','name','description','unit'))

def test_get_qc():
    if ipm_ok:
        res = ipm.get_qc()
        assert type(res) is list
        assert keys_exists(res[0],('id','name','description'))

def test_get_schema_weatherdata():
    if ipm_ok:
        res = ipm.get_schema_weatherdata()
        assert type(res) is dict

def test_post_schema_weatherdata_validate():
    if ipm_ok:
        res = ipm.post_schema_weatherdata_validate(jsonfile=datadir + 'weather_data.json')
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
    res = ipm.post_schema_modeloutput_validate(jsonfile=datadir + 'modeloutput.json')
    assert type(res) is dict
    assert res['isValid']==True

######################### WeatherAdaptaterService #######################


def test_get_weatheradapter():
    """Canonical test described in doc  https://github.com/H2020-IPM-Decisions/WeatherService/blob/develop/docs/weather_service.md"""
    ipm = IPM()
    params = dict(weatherStationId=5,
             parameters='1002,2001,3002,3101',
             interval=3600,
             timeStart='2020-05-01T00:00:00+02:00',
             timeEnd= '2020-05-02T00:00:00+02:00')

    source = ipm.get_weatherdatasource('no.nibio.lmt')
    res = ipm.get_weatheradapter(source, params)

    assert type(res) is dict
    assert all(key in res for key in ('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
    assert all(var in res['weatherParameters'] for var in [1002, 2001, 3002, 3101])
    assert res['timeStart'] == '2020-04-30T22:00:00Z'
    assert res['timeEnd'] == '2020-05-01T22:00:00Z'
    assert res['locationWeatherData'][0]['length'] == 25



#################### WeatherDataService #########################################

def test_get_weatherdatasource():
    ipm=IPM()
    res = ipm.get_weatherdatasource()
    assert type(res) is dict
    assert keys_exists(res[next(iter(res))],('name','description','public_URL','endpoint','needs_data_control','access_type','temporal','parameters','spatial'))

def test_get_weatherdatasource_location_point():
    ipm=IPM()
    res = ipm.get_weatherdatasource_location_point(latitude=59.678835236960765,longitude=12.01629638671875, tolerance=0)
    assert type(res) is list
    assert keys_exists(res[0],('id', 'name', 'description', 'public_URL', 'endpoint', 'authentication_type', 'needs_data_control', 'access_type', 'priority', 'temporal', 'parameters', 'spatial', 'organization', 'active'))

def test_post_weatherdatasource_location():
    ipm=IPM()
    res = ipm.post_weatherdatasource_location(  
        tolerance=0,
        geoJsonfile=datadir + "GeoJson.json"
        )
    assert type(res) is list
    assert keys_exists(res[0].keys(),('id', 'name', 'description', 'public_URL', 'endpoint', 'authentication_type', 'needs_data_control', 'access_type', 'priority', 'temporal', 'parameters', 'spatial', 'organization', 'active')
        )



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
    assert 'DAUCS' in res[0]['models'][0]['crops']

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

def test_get_dss_location():
    ipm=IPM()
    res = ipm.get_dss_location_point(latitude=59.67883523696076, longitude=12.01629638671875)
    assert type(res) is list
    assert keys_exists(res[0],('models','id','version','name','url','languages','organization'))

def test_post_dss_location():
    ipm = IPM()
    res= ipm.post_dss_location(geoJsonfile=datadir + "GeoJson.json")
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

def test_run_model():
    ipm = IPM()
    model = ipm.get_model(DSSId='no.nibio.vips',ModelId='PSILARTEMP')
    # run with predifined model input:
    path = datadir + 'model_input.json'
    with open(path) as json_file:
        model_input = json.load(json_file)
    res = ipm.run_model(model, model_input=model_input)
    assert isinstance(res, dict)
    assert 'locationResult' in res
    # run with live model input
    params = dict(weatherStationId=5,
             parameters='1002,2001,3002,3101',
             interval=86400,
             timeStart='2020-05-01T00:00:00+02:00',
             timeEnd= '2020-05-02T00:00:00+02:00')
    source = ipm.get_weatherdatasource('no.nibio.lmt')
    weather_data = ipm.get_weatheradapter(source, params)
    res = ipm.run_model(model, weather_data=weather_data)
    assert isinstance(res, dict)
    assert 'locationResult' in res
