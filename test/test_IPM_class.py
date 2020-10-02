import pytest
from agroservice.ipm import IPM_weather, IPM_DSS


ws = IPM_weather()
dss = IPM_DSS()

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)
    

def test_url():
    assert ws.url == 'https://ipmdecisions.nibio.no/api/wx/rest', "IPM_weather url are not valid"
    assert dss.url == 'https://ipmdecisions.nibio.no/api/dss/rest',"IPM_DSS url are not valid"



################# MetaDataService ################################# 

def test_get_parameter():
    res = ws.get_parameter()
    assert res is not None
    assert type(res) is list or int
    assert keys_exists(res[0],('id','name','description','unit'))

def test_get_qc():
    res = ws.get_qc()
    assert res is not None
    assert type(res) is list or int 
    assert keys_exists(res[0],('id','name','description'))

def test_get_schema_weatherdata():
    res = ws.get_schema_weatherdata()
    assert res is not None
    assert type(res) is list or int

def test_post_schema_weatherdata_validate():
    """Todo"""
    #res = ws.post_schema_weatherdata_validate()
    pass    

def test_get_schema_fieldobservation():
    res = dss.get_schema_fieldobservation()
    assert res is not None 
    assert type(res) is dict or int
    assert res ==  {'$schema': 'http://json-schema.org/draft-04/schema#',
 'title': 'Field observation',
 'type': 'object',
 'additionalProperties': False,
 'description': 'Version 0.1. The schema describes the field observation format for the IPM Decisions platform. See an example here: TODO',
 '$id': 'https://ipmdecisions.nibio.no/dss/rest/schema/fieldobservation',
 'properties': {'location': {'title': 'Location  of the observation. In GeoJson format.',
   '$ref': 'https://ipmdecisions.nibio.no/schemas/geojson.json'},
  'time': {'type': 'string',
   'format': 'date-time',
   'description': 'The timestamp of the field observation. Format: "yyyy-MM-dd\'T\'HH:mm:ssXXX", e.g. 2020-04-09T18:00:00+02:00',
   'title': "Time (yyyy-MM-dd'T'HH:mm:ssXXX)"},
  'pestEPPOCode': {'type': 'string',
   'description': 'The EPPO code for the observed pest. See https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes',
   'title': 'Pest'},
  'cropEPPOCode': {'type': 'string',
   'description': 'The EPPO code for the crop in which the pest was observed. See https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes',
   'title': 'Pest'}},
 'required': ['location', 'time', 'pestEPPOCode', 'cropEPPOCode']}

def test_get_schema_modeloutput():
    res = dss.get_schema_modeloutput()
    assert res is not None 
    assert type(res) is dict or int
    assert res == {'$schema': 'http://json-schema.org/draft-04/schema#',
 'title': 'Model output',
 'type': 'object',
 'additionalProperties': False,
 'description': 'Version 0.1. The schema describes the model output format for the IPM Decisions platform. See an example here: TODO',
 '$id': 'https://ipmdecisions.nibio.no/dss/rest/schema/modeloutput',
 'properties': {'timeStart': {'type': 'string',
   'format': 'date-time',
   'description': 'The timestamp of the first result. Format: "yyyy-MM-dd\'T\'HH:mm:ssXXX", e.g. 2020-04-09T18:00:00+02:00',
   'title': "Time start (yyyy-MM-dd'T'HH:mm:ssXXX)"},
  'timeEnd': {'type': 'string',
   'format': 'date-time',
   'description': 'The timestamp of the last result. Format: "yyyy-MM-dd\'T\'HH:mm:ssXXX", e.g. 2020-04-09T18:00:00+02:00',
   'title': "Time end (yyyy-MM-dd'T'HH:mm:ssXXX)"},
  'interval': {'type': 'integer',
   'description': 'The sampling frequency in seconds. E.g. 3600 = hourly values',
   'title': 'Sampling frequency (seconds)'},
  'resultParameters': {'type': 'array',
   'minItems': 1,
   'maxItems': 2147483647,
   'items': {'type': 'string'},
   'description': 'The result parameters. Unique to each model',
   'title': 'Result parameters'},
  'locationResult': {'oneOf': [{'type': 'null', 'title': 'Not included'},
    {'type': 'array', 'items': {'$ref': '#/definitions/LocationResult'}}],
   'description': 'The result data per location.',
   'title': 'Result data'}},
 'required': ['timeStart', 'timeEnd', 'interval', 'resultParameters'],
 'definitions': {'LocationResult': {'type': 'object',
   'additionalProperties': False,
   'properties': {'longitude': {'oneOf': [{'type': 'null',
       'title': 'Not included'},
      {'type': 'number'}],
     'description': 'The longitude of the location. Decimal degrees (WGS84)',
     'title': 'Longitude (WGS84)'},
    'latitude': {'oneOf': [{'type': 'null', 'title': 'Not included'},
      {'type': 'number'}],
     'description': 'The latitude of the location. Decimal degrees (WGS84)',
     'title': 'Latitude (WGS84)'},
    'altitude': {'oneOf': [{'type': 'null', 'title': 'Not included'},
      {'type': 'number'}],
     'description': 'The altitude of the location. Measured in meters',
     'title': 'Altitude (Meters)'},
    'data': {'type': 'array',
     'items': {'type': 'array', 'items': {'type': 'number'}},
     'description': 'The data. In rows, ordered chronologically. Columns ordered as given in resultParameters.',
     'title': 'Result data per location'},
    'width': {'oneOf': [{'type': 'null', 'title': 'Not included'},
      {'type': 'integer'}]},
    'length': {'oneOf': [{'type': 'null', 'title': 'Not included'},
      {'type': 'integer'}]}},
   'required': ['data']}}}

def test_post_schema_modeloutput_validate():
    #res = dss.post_schema_modeloutput_validate():
    pass

######################### WeatherAdaptaterService #######################

def test_get_weatheradapter_fmi():
    res = ws.get_weatheradapter_fmi(ignoreErrors=False,interval=3600,parameters="1001",timeStart='2020-06-12T00:00:00+03:00',timeEnd='2020-07-03T00:00:00+03:0',weatherStationId=101533)
    assert res is not None
    assert type(res) is list or int

def test_post_weatheradapter_fmi():
    """todo"""
    #res = ws.post_weatheradapter_fmi()
    pass

def test_get_weatheradapter_fmi_forecasts():
    res = ws.get_weatheradapter_fmi_forecasts(latitude= 43.56, longitude=3.52)
    assert res is not None 
    assert type(res) is dict or int
    assert keys_exists(res.keys(),('timeStart','timeEnd','interval','weatherParameters','locationWeatherData'))
    assert keys_exists(res['locationWeatherData'][0],('longitude','latitude','altitude','data','width','length'))
    assert len(res['locationWeatherData'][0]['data'])==res['locationWeatherData'][0]['length']

def test_post_weatheradapter_fmi_forecasts():
    """Todo"""
    res = ws.post_weatheradapter_fmi_forecasts(latitude=43.56, longitude=3.52)

def test_get_weatheradapter_yr():
    res = ws.get_weatheradapter_yr(altitude=56,longitude=3.52,latitude=43.36)
    assert res is not None
    assert type(res) is dict or int
    assert keys_exists(res.keys(),('timeStart','timeEnd','interval','weatherParameters','locationWeatherData','qc'))
    assert keys_exists(res['locationWeatherData'][0],('longitude','latitude','altitude','data','width','length'))
    assert len(res['locationWeatherData'][0]['data'])==res['locationWeatherData'][0]['length']
    

def test_post_weatheradapter_yr():
    """todo"""
    pass

#################### WeatherDataService #########################################

def test_get_weatherdatasource():
    res = ws.get_weatherdatasource()
    assert res is not None
    assert type(res) is list or int
    assert keys_exists(res[0],('name','description','public_URL','endpoint','needs_data_control','access_type','temporal','parameters','spatial'))

def test_get_weatherdatasource_location_point():
    res = ws.get_weatherdatasource_location_point(latitude=43.36 ,longitude=3.52, tolerance=0)
    assert res is not None
    assert type(res) is list or int

#################### DSSService ####################################################

def test_get_crop():
    res = dss.get_crop()
    assert res is not None
    assert type(res) is list or int

def test_get_cropCode():
    res = dss.get_cropCode(cropCode="DAUCS")
    assert res is not None
    assert res is list or int
    assert keys_exists(res[0],('models','id','version','name','url','languages','organization'))
    assert res[0]['models'][0]['crops']==['DAUCS']

def test_get_dss():
    res = dss.get_dss()
    assert res is not None
    assert res is list or int
    assert keys_exists(res[0],('models','id','version','name','url','languages','organization'))

def test_get_dss_location():
    res = dss.get_dss_location_point(latitude=59.67883523696076, longitude=12.01629638671875)
    assert res is not None 
    assert res is list or int
    assert keys_exists(res[0],('models','id','version','name','url','languages','organization'))

def test_get_dssId():
    res = dss.get_dssId(DSSId='no.nibio.vips')
    assert res is not None 
    assert res is dict or int
    assert keys_exists(res.keys(),('models','id','version','name','url','languages','organization'))
    assert res['id']=='no.nibio.vips'

def test_get_model():
    res = dss.get_model(DSSId='no.nibio.vips',ModelId='PSILARTEMP')
    assert res is not None 
    assert res is dict or int
    assert keys_exists(res.keys(),('name', 'id', 'version', 'type_of_decision', 'type_of_output', 'description_URL', 'description', 'citation', 'keywords', 'pests', 'crops', 'authors', 'execution', 'input', 'valid_spatial', 'output'))
    assert res['id']== 'PSILARTEMP'

def test_get_pest():
    res = dss.get_pest()
    assert res is not None 
    assert res is list or int

def test_get_pestCode():
    res = dss.get_pestCode(pestCode='PSILRO')
    assert res is not None 
    assert res is list or int
    assert keys_exists(res[0],('models','id','version','name','url','languages','organization'))
    assert res[0]['models'][0]['pests'] == ['PSILRO'] 

