import os
import json

datadir = os.path.dirname(__file__) + '/data/'

def postman_tests():
    """Undeclared options of weatheradapter services"""
    with open(datadir + 'IPM Decisions Weather API tests.postman_collection.json') as jsonfile:
        postman = json.load(jsonfile)
    adapters = {it['name']: it for it in
                [item for item in postman['item'] if item['name'] == 'WeatherAdapterService'][0]['item']
                }
    def _read(test):
        d = dict()
        d['name'] = test['name']
        url = test['request']['url']
        d['endpoint'] = '/'.join(url['host'] + url['path'])
        d['call'] = {it['key']: it['value'] for it in url['query']}
        return d
    mapping = {'FruitWeb/Davis': 'info.fruitweb',
               'MeteoBot': 'com.meteobot',
               'Metos (FieldClimate)': 'net.ipmdecisions.metos',
               'FMI (Finnish Meteorological Service)': 'fi.fmi.observation.station',
               'Yr.no (Norwegian Meteorological Service) forecasts': 'no.met.locationforecasts',
               'Met Ireland forecasts': 'ie.gov.data',
               'FMI (Finnish Meteorological Service) forecasts': 'fi.fmi.forecast.location',
               'DMI (Danish Meteorological Service) PointWeb GRID': 'dk.dmi.pointweather',
               'SLU Lantmet (Sweden) GRID': 'se.slu.lantmet'}
    return {mapping[k] : _read(v) for k,v in adapters.items()}

def country_mapping():
    """mapping of alpha3 to alpha 2 country codes
    generated using pycountry :
    {c.alpha_3: c.alpha_2 for c in pycountry.countries}
    """
    with open(datadir + 'countries.json') as input:
        mapping = json.load(input)
    return mapping