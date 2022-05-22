import pytest
from urllib.request import urlopen
from agroservices.ipm import IPM


def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)
    
######################### WeatherAdaptaterService #######################
 
    
def test_weatheradapter_MeteoBot():
    ipm = IPM()
    meteobot = 'MeteoBot API'
    ws= ipm.weatheradapter_service(forecast=None)
    res= ipm.get_weatheradapter(
        endpoint=ws[meteobot]['endpoint'],
        weatherStationId=732,
        interval=3600,
        ignoreErrors=True,
        timeStart='2020-06-12',
        timeEnd='2020-07-03',
        parameters=[1001],
        credentials={"username":"3138313530303239","password":"Y3Nw_48aNe4y1Z0Wj"})
    
    assert type(res) is dict, res
    assert keys_exists(res.keys(),('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
    assert res['weatherParameters']==[1002,3002]
    assert res['timeStart']== "2020-06-11T21:00:00Z"
    assert res['timeEnd']== "2020-07-02T21:00:00Z"
    assert res['locationWeatherData'][0]['length']== 505
    

def test_weatheradapter_metos():
    ipm = IPM()
    metos = 'Metos'
    ws= ipm.weatheradapter_service(forecast=None)

    res= ipm.get_weatheradapter(
        endpoint=ws[metos]['endpoint'],
        weatherStationId=732,
        ignoreErrors=True,
        interval=3600,
        timeStart='2020-06-12',
        timeEnd='2020-07-03',
        parameters=[1001],
        credentials={"username":"3138313530303239","password":"Y3Nw_48aNe4y1Z0Wj"})

    assert type(res) is dict, res
    assert keys_exists(res.keys(),('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
    assert res['weatherParameters']==[1002,3002]
    assert res['timeStart']== "2020-06-11T21:00:00Z"
    assert res['timeEnd']== "2020-07-02T21:00:00Z"
    assert res['locationWeatherData'][0]['length']== 505

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
    assert res['weatherParameters']==[1002,3002]
    assert res['timeStart']== "2020-06-11T21:00:00Z"
    assert res['timeEnd']== "2020-07-02T21:00:00Z"
    assert res['locationWeatherData'][0]['length']== 505


def test_dw_eu():
    ipm = IPM()
    ws= ipm.weatheradapter_service(forecast=None)
    dw_eu = 'Deutsche Wetterdienst EU Area location forecast by IPM Decisions'

    res= ipm.get_weatheradapter_forecast(
        endpoint=ws[dw_eu]['endpoint'],
        latitude=50.109,
        longitude=10.961
        )
    
    assert type(res) is dict, res
    assert keys_exists(res.keys(),('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))




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
