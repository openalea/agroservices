"""Smart fakers for generating credible json inputs of ipm services"""

import datetime
import random
from faker import Faker
from jsf import JSF
from agroservices.ipm.datadir import country_mapping
import json

Geojson_point ="""{{
    "type": "FeatureCollection",
    "features": [
        {{
            "type": "Feature",
            "properties": {{}},
            "geometry": {{
                "type": "Point",
                "coordinates": [
                    {longitude},
                    {latitude}
                ]
            }}
        }}
    ]
}}"""

def weather_adapter_params(weather_adapter,
                           parameters=None,
                           time_start=None,
                           time_end=None,
                           interval=None,
                           latitude=None,
                           longitude=None,
                           station_id=None):
    """Generate a weather_adapter parameter dict


        Parameters
        ----------
         source : dict
            A meta_data dict of the source (see self.get_weatherdatasource)
         interval : int,
             The measuring interval in seconds. Please note that the only allowed interval in this version is 3600 (hourly), by default 3600
         parameters : list,
             list of the requested weather parameters, by default the one listed under 'common'
         latitude : Union[int,float],
            WGS84 Decimal degrees
         longitude : Union[int,float],
            WGS84 Decimal degrees
        timeStart : str,
             Start of weather data period (ISO-8601 Timestamp, e.g. 2020-06-12T00:00:00+03:00), by default to day (forecast) or first date available (historical)'
         timeEnd : str, optional
             End of weather data period (ISO-8601 Timestamp, e.g. 2020-07-03T00:00:00+03:00), by default tommorow (forecast) one day after first date (historical)
         weatherStationId : int,
             a location id
    """
    fake = {}

    if parameters is None:
        parameters = weather_adapter['parameters']['common']
    fake.update(dict(parameters=','.join(map(str, parameters))))

    if interval is None:
        interval = weather_adapter['temporal']['intervals'][0]
    fake.update({'interval': interval})

    if weather_adapter['temporal']['historic']['start'] is not None:
        if time_start is None:
            start = weather_adapter['temporal']['historic']['start']
            # use next day to avoid timezone problems
            start = datetime.datetime.fromisoformat(start) + datetime.timedelta(days=1)
        else:
            start = datetime.datetime.fromisoformat(time_start)
        time_start = start.astimezone().isoformat()
        if time_end is None:
            if interval == 3600:
                end = start + datetime.timedelta(hours=1)
            else:
                end = start + datetime.timedelta(days=1)
            time_end = end.astimezone().isoformat()
        fake.update(dict(timeStart=time_start, timeEnd=time_end, ignoreErrors='true'))

    if weather_adapter['access_type'] == 'location':
        if weather_adapter['spatial']['countries'] is None:
            fake['latitude'] = random.uniform(0, 90) if latitude is None else latitude
            fake['longitude'] = random.uniform(0, 180) if longitude is None else longitude
        else:
            cmap = country_mapping()
            faker = Faker()
            lat, lng, _, _, _ = faker.local_latlng(cmap[weather_adapter['spatial']['countries'][0]])
            fake['longitude'] = float(lng)
            fake['latitude'] = float(lat)
    elif weather_adapter['access_type'] == 'stations':
        if station_id is None:
            features = weather_adapter["spatial"]["geoJSON"]['features']
            ids = [int(random.uniform(1, 100))]
            if len(features) > 0:
                if 'id' in features[0]:
                    ids = [item['id'] for item in features]
                else:
                    ids = [item['properties']['id'] for item in features]
            station_id = random.sample(ids, 1)[0]
        fake.update(dict(weatherStationId=station_id))
    else:
        raise ValueError("Unknown access type : " + weather_adapter['access_type'])

    return fake


def weather_data(parameters=(1001, 1002), interval=3600, length=3, longitude =None, latitude=None, altitude=None, data=None):
    """generate a dict complying IPMDecision weatherData schema"""
    fake = {}

    assert interval in [3600, 86400]
    time_start = datetime.datetime.today().astimezone()
    if interval == 3600:
        time_end = time_start + datetime.timedelta(hours=length - 1)
    else:
        time_end = time_start + datetime.timedelta(days=length - 1)
    fake['timeStart'] = time_start.isoformat()
    fake['timeEnd'] = time_end.isoformat()
    fake['interval'] = interval

    try:
        iter(parameters)
    except TypeError:
        parameters = list(parameters)
    fake['weatherParameters'] = [p for p in parameters]

    width = len(parameters)
    if data is None:
        data = [[p / 10 for p in random.sample(range(100), width)] for _ in range(length)]
    else:
        assert len(data) > 0
        assert len(data)[0] == width, 'data should be a list of tuples, each being as long as parameters'
        length = len(data)

    if longitude is None:
        longitude = random.uniform(0, 180)
    if latitude is None:
        latitude = random.uniform(0, 90)
    if altitude is None:
        altitude = 0

    fake['locationWeatherData'] = [
        {
            'longitude': longitude,
            'latitude': latitude,
            'altitude': altitude,
            'data': data,
            'length': length,
            'width': width
        }
    ]

    return fake


def model_weather_data(model, length=3):
    """Generate fake weather data along spec given in model"""
    if model['input']['weather_parameters'] is None:
        return weather_data(length=length)
    parameters = [item['parameter_code'] for item in model['input']['weather_parameters']]
    interval = model['input']['weather_parameters'][0]['interval']
    return weather_data(parameters=parameters, interval=interval, length=length)

def model_field_observations(model, quantifications, latitude=None, longitude=None, time=None, pest=None, crop=None):
    """generate common part of field observation

        quantification is a list of dict, each being a {k:value} """
    length = len(quantifications)
    latitude = random.uniform(0, 90) if latitude is None else latitude
    longitude = random.uniform(0, 180) if longitude is None else longitude
    location = json.loads(Geojson_point.format(longitude=longitude, latitude=latitude))
    if time is None:
        start = datetime.datetime.today().astimezone()
        time = [(start + datetime.timedelta(days=i)).isoformat() for i in range(length)]
    if pest is None:
        pest = random.sample(model['pests'], 1)[0]
    if crop is None:
        crop = random.sample(model['crops'], 1)[0]
    field_obs =  [{'location': location,
                   'time': time[i],
                   'pestEPPOCode': pest,
                   'cropEPPOCode': crop} for i in range(length)]
    fake={'fieldObservations': field_obs,
            'fieldObservationQuantifications': quantifications}
    return fake


def input_data(model, weather_data=None, field_observations=None):
    input_schema = model['execution']['input_schema'].copy()
    accept_fieldobservations = False
    where_fieldobservations = None
    #TODO when there are reference to input schema parameters in model[input'], parameters should be added to the input
    # fill externaly defined refs
    if 'weatherData' in input_schema['properties']:
        input_schema['properties']['weatherData'] = {'type': 'string',
                                               'default': 'WEATHER_DATA'}
    if 'fieldObservations' in input_schema['properties']:
        input_schema['properties']['fieldObservations'] = {'type': 'string',
                                               'default': 'FIELD_OBSERVATION'}
        if 'fieldObservations' in input_schema['properties']['required']:
            if 'fieldObservationQuantifications' not in input_schema['properties']['required']:
                input_schema['properties']['required'].append('fieldObservationQuantifications')
        accept_fieldobservations=True
        where_fieldobservations='root'
    else:
        for prop in input_schema['properties']:
            if 'properties' in input_schema['properties'][prop]:
                if 'fieldObservations' in input_schema['properties'][prop]['properties']:
                    input_schema['properties'][prop]['properties']['fieldObservations'] = {'type': 'string',
                                                                   'default': 'FIELD_OBSERVATION'}
                    if 'fieldObservations' in input_schema['properties'][prop]['required']:
                        if 'fieldObservationQuantifications' not in input_schema['properties'][prop]['required']:
                            input_schema['properties'][prop]['required'].append('fieldObservationQuantifications')
                    accept_fieldobservations = True
                    where_fieldobservations = prop

    jsf_faker = JSF(input_schema)
    fake = jsf_faker.generate()
    current_year = datetime.datetime.now().year
    for field in fake:
        if 'default' in input_schema['properties'][field]:
            fake[field] = input_schema['properties'][field]['default'].format(CURRENT_YEAR=current_year)
        elif isinstance(fake[field], dict):
            for sub_field in fake[field]:
                if 'default' in input_schema['properties'][field]['properties'][sub_field]:
                    fake[field][sub_field] = input_schema['properties'][field]['properties'][sub_field]['default'].format(CURRENT_YEAR=current_year)

    if 'weatherData' in input_schema['properties']:
        if weather_data is None:
            weather_data = model_weather_data(model)
        fake['weatherData'] = weather_data

    if accept_fieldobservations:
        if field_observations is None:
            if where_fieldobservations == 'root':
                quantifications = fake['fieldObservationQuantifications']
            else :
                quantifications = fake[prop]['fieldObservationQuantifications']
            field_observations = model_field_observations(model, quantifications)

        if where_fieldobservations == 'root':
            fake.update(field_observations)
        else:
            fake[prop].update(field_observations)

    return fake



#TODO: add interpreters for model meta for wralea

