import pytest
from agroservice.ipm import IPM


ipm = IPM()

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)
    

def test_url():
    assert ipm.url == 'https://ipmdecisions.nibio.no/api/wx/rest', "IPM url are not valid"


################# MetaDataService ################################# 

def test_get_parameter():
    res = ipm.get_parameter()
    assert res is not None
    assert type(res) is list or int
    assert keys_exists(res[0],('id','name','description','unit'))

def test_get_qc():
    res = ipm.get_qc()
    assert res is not None
    assert type(res) is list or int 
    assert keys_exists(res[0],('id','name','description'))

def test_get_schema_weatherdata():
    res = ipm.get_schema_weatherdata()
    assert res is not None
    assert type(res) is list or int

def test_post_schema_weatherdata_validate():
    """Todo"""
    #res = ipm.post_schema_weatherdata_validate()
    pass       

######################### WeatherAdaptaterService #######################

def test_get_weatheradapter_fmi():
    res = ipm.get_weatheradapter_fmi(ignoreErrors=False,interval=3600,parameters="1001",timeStart='2020-06-12T00:00:00+03:00',timeEnd='2020-07-03T00:00:00+03:0',weatherStationId=101533)
    assert res is not None
    assert type(res) is list or int

def test_post_weatheradapter_fmi():
    """todo"""
    #res = ipm.post_weatheradapter_fmi()
    pass

def test_get_weatheradapter_fmi_forecasts():
    res = ipm.get_weatheradapter_fmi_forecasts(latitude= 43.56, longitude=3.52)
    assert res is not None 
    assert type(res) is dict or int
    assert keys_exists(res.keys(),('timeStart','timeEnd','interval','weatherParameters','locationWeatherData'))
    assert keys_exists(res['locationWeatherData'][0],('longitude','latitude','altitude','data','width','length'))
    assert len(res['locationWeatherData'][0]['data'])==res['locationWeatherData'][0]['length']

def test_post_weatheradapter_fmi_forecasts():
    """Todo"""
    res = ipm.post_weatheradapter_fmi_forecasts(latitude=43.56, longitude=3.52)

def test_get_weatheradapter_yr():
    res = ipm.get_weatheradapter_yr(altitude=56,longitude=3.52,latitude=43.36)
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
    res = ipm.get_weatherdatasource()
    assert res is not None
    assert type(res) is list or int
    assert keys_exists(res[0],('name','description','public_URL','endpoint','needs_data_control','access_type','temporal','parameters','spatial'))

def test_get_weatherdatasource_location_point():
    res = ipm.get_weatherdatasource_location_point(latitude=43.36 ,longitude=3.52, tolerance=0)
    assert res is not None
    assert type(res) is list or int


