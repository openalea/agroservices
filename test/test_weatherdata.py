import pytest
from urllib.request import urlopen
from agroservices.ipm import IPM


def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)
    


######################### WeatherAdaptaterService #######################
def test_weatheradapter_service():
    ipm=IPM()

    ws= ipm.weatheradapter_service(forecast=None)
    assert type(ws) is dict
    assert len(ws)==7
    assert keys_exists(ws.keys(),(
        'Met Norway Locationforecast',
        'FMI weather forecasts',
        'Finnish Meteorological Institute measured data',
        'Landbruksmeteorologisk tjeneste', 
        'MeteoBot API', 
        'Fruitweb', 
        'Metos')
        )

    ws_forcast= ipm.weatheradapter_service(forecast=True)
    assert type(ws_forcast) is dict
    assert len(ws_forcast)==2
    assert keys_exists(ws_forcast,(
        'Met Norway Locationforecast',
        'FMI weather forecasts'))

def test_get_weatheradapter_fmi():
    ipm=IPM()
    res = ipm.get_weatheradapter(endpoint='/weatheradapter/fmi/',
        ignoreErrors=True,
        credentials=None,
        interval=3600,
        parameters=[1002,3002],
        timeStart='2020-06-12T00:00:00+03:00',
        timeEnd='2020-07-03T00:00:00+03:00',
        weatherStationId=101104)
    assert type(res) is dict
    assert keys_exists(res.keys(),('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
    assert res['weatherParameters']==[1002,3002]
    assert res['timeStart']== "2020-06-11T21:00:00Z"
    assert res['timeEnd']== "2020-07-02T21:00:00Z"
    assert res['locationWeatherData'][0]['length']== 505
    

def test_get_weatheradapter_fmi_forecasts():
    ipm=IPM()
    res = ipm.get_weatheradapter_forecast(
        endpoint='/weatheradapter/fmi/forecasts',
        latitude=67.2828, 
        longitude=14.3711)
        
    assert type(res) is dict 
    assert keys_exists(res.keys(),('timeStart','timeEnd','interval','weatherParameters','locationWeatherData'))
    assert res['locationWeatherData'][0]['latitude']==67.2828
    assert res['locationWeatherData'][0]['longitude']==14.3711
    assert res['locationWeatherData'][0]['altitude']==0
    assert res['weatherParameters']==[2001, 4002, 5001, 1002, 3002, 1901]
    

def test_get_weatheradapter_yr():
    ipm=IPM()
    res = ipm.get_weatheradapter_forecast(
        endpoint= '/weatheradapter/yr/',
        altitude=70,
        longitude=14.3711,
        latitude=67.2828)
    assert type(res) is dict
    assert keys_exists(res.keys(),('timeStart','timeEnd','interval','weatherParameters','locationWeatherData'))
    assert res['locationWeatherData'][0]['altitude']==70
    assert res['locationWeatherData'][0]['longitude']==14.3711
    assert res['locationWeatherData'][0]['latitude']==67.2828
    assert res['weatherParameters']==[1001, 3001, 2001, 4002]
    

def test_weatheradapter_Landbrukmeterologisk():
    """todo"""
    pass

def test_weatheradapter_MeteoBot():
    ipm = IPM()
    res= ipm.get_weatheradapter(
        endpoint='/weatheradapter/meteobot/',
        weatherStationId=732,
        interval=3600,
        ignoreErrors=True,
        timeStart='2020-06-12',
        timeEnd='2020-07-03',
        parameters=[1001],
        credentials={"username":"3138313530303239","password":"Y3Nw_48aNe4y1Z0Wj"})
    
    assert type(res) is dict, res
    assert keys_exists(res.keys(),('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
    #assert res['weatherParameters']==[1002,3002]
    #assert res['timeStart']== "2020-06-11T21:00:00Z"
    #assert res['timeEnd']== "2020-07-02T21:00:00Z"
    #assert res['locationWeatherData'][0]['length']== 505
    

def test_weatheradapter_metos():
    ipm = IPM()
    res= ipm.get_weatheradapter(
        endpoint='/weatheradapter/metos/',
        weatherStationId=732,
        ignoreErrors=True,
        interval=3600,
        timeStart='2020-06-12',
        timeEnd='2020-07-03',
        parameters=[1001],
        credentials={"username":"3138313530303239","password":"Y3Nw_48aNe4y1Z0Wj"})

    assert type(res) is dict, res
    assert keys_exists(res.keys(),('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
    #assert res['weatherParameters']==[1002,3002]
    #assert res['timeStart']== "2020-06-11T21:00:00Z"
    #assert res['timeEnd']== "2020-07-02T21:00:00Z"
    #assert res['locationWeatherData'][0]['length']== 505

def test_weatheradapter_Fruitdevis():
    ipm = IPM()
    res= ipm.get_weatheradapter(
        endpoint='/weatheradapter/davisfruitweb/',
        weatherStationId=18150029,
        ignoreErrors=True,
        timeStart='2021-02-01',
        timeEnd='2021-03-01',
        parameters=[1001],
        credentials={"username":"536","password":"GF90esoleo"})
    
    assert type(res) is dict, res
    assert keys_exists(res.keys(),('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
    #assert res['weatherParameters']==[1002,3002]
    #assert res['timeStart']== "2020-06-11T21:00:00Z"
    #assert res['timeEnd']== "2020-07-02T21:00:00Z"
    #assert res['locationWeatherData'][0]['length']== 505

#################### WeatherDataService #########################################

def test_get_weatherdatasource():
    ipm=IPM()
    res = ipm.get_weatherdatasource()
    assert type(res) is list 
    assert keys_exists(res[0],('name','description','public_URL','endpoint','needs_data_control','access_type','temporal','parameters','spatial'))

def test_get_weatherdatasource_location_point():
    ipm=IPM()
    res = ipm.get_weatherdatasource_location_point(latitude=59.678835236960765,longitude=12.01629638671875, tolerance=0)
    assert type(res) is list
    assert keys_exists(res[0],('access_type','authentication_required','description', 'endpoint', 'name', 'needs_data_control', 'organization', 'parameters', 'public_URL', 'spatial', 'temporal'))

def test_post_weatherdatasource_location():
    ipm=IPM()
    res = ipm.post_weatherdatasource_location(  
        tolerance=0,
        geoJsonfile="GeoJson.json"
        )
    assert type(res) is list
    assert keys_exists(res[0].keys(),(
        'name', 
        'description', 
        'public_URL', 
        'endpoint', 
        'authentication_required', 
        'needs_data_control', 
        'access_type', 
        'temporal', 
        'parameters', 
        'spatial', 
        'organization')
        )

#################### DSSService ####################################################


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
