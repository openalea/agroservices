"""Smart fakers for generating credible json inputs of ipm services"""

import datetime
import random


def weather_adapter_params(weather_adapter,
                           parameters=None,
                           time_start=None,
                           time_end=None,
                           interval=None,
                           latitude=None,
                           longitude=None,
                           altitude=None,
                           station_id=None):
    # TODO use postman spec to add additional required parameters
    """Generate a weather_adapter parameter dict

    By default re-use parameters found in postman test suite

        Parameters
        ----------
         source : dict
            A meta_data dict of the source (see self.get_weatherdatasource)
         interval : int,
             The measuring interval in seconds. Please note that the only allowed interval in this version is 3600 (hourly), by default 3600
         parameters : list,
             list of the requested weather parameters, by default the one listed under 'common'
         altitude : Union[int,float],
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
            time_start = datetime.datetime.fromisoformat(start) + datetime.timedelta(days=1)
            time_start = time_start.astimezone().isoformat()
        else:
            start = datetime.datetime.fromisoformat(time_start)
        if time_end is None:
            if interval == 3600:
                end = start + datetime.timedelta(hours=1)
            else:
                end = start + datetime.timedelta(days=1)
            time_end = end.astimezone().isoformat()
        fake.update(dict(timeStart=time_start, timeEnd=time_end))

    if weather_adapter['access_type'] == 'location':
        fake['latitude'] = random.uniform(0, 90) if latitude is None else latitude
        fake['longitude'] = random.uniform(0, 180) if longitude is None else longitude
        if altitude is not None:
            fake['altitude'] = altitude
    elif weather_adapter['access_type'] == 'location':
        if station_id is None:
            features = weather_adapter["spatial"]["geoJSON"]['features']
            ids = random.uniform(1, 100)
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


def weather_data(parameters=(1001, 1002), interval=3600, length=3):
    """generate a dict complying IPMDecision weatherData schema"""
    fake = {}

    assert interval in [3600, 86400]
    time_start = datetime.datetime.today().astimezone()
    if interval == 3600:
        time_end = time_start + datetime.timedelta(hours=length)
    else:
        time_end = time_start + datetime.timedelta(days=length)
    fake['timeStart'] = time_start.isoformat()
    fake['timeEnd'] = time_end.isoformat()
    fake['interval'] = interval

    try:
        iter(parameters)
    except TypeError:
        parameters = list(parameters)
    fake['weatherParameters'] = [p for p in parameters]

    width = len(parameters)
    data = [[p / 10 for p in random.sample(range(100), width)] for _ in range(length)]
    fake['locationWeatherData'] = [
        {
            'longitude': random.uniform(0, 180),
            'latitude': random.uniform(0, 90),
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
    return weather_data(parameters, interval, length)

#TODO : fake fieldobs and fake model inputs

#TODO: add interpreters for weatherdat postman spec, model meta for wralea

#TODO: add fixes at instanciation for JSF pattern that fails