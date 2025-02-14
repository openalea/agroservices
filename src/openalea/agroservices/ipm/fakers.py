"""Smart fakers for generating credible json inputs of ipm services"""

import datetime
import random
import json
from copy import deepcopy
from faker import Faker
from jsf import JSF
from openalea.agroservices.ipm.datadir import country_mapping

Geojson_point = """{{
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


def weather_adapter_params(
    weather_adapter,
    parameters=None,
    time_start=None,
    time_end=None,
    interval=None,
    latitude=None,
    longitude=None,
    station_id=None,
):
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
         End of weather data period (ISO-8601 Timestamp, e.g. 2020-07-03T00:00:00+03:00), by default tomorrow (forecast) one day after first date (historical)
     weatherStationId : int,
         a location id
    """
    fake = {}

    if parameters is None:
        parameters = weather_adapter["parameters"]["common"]
    fake.update(dict(parameters=",".join(map(str, parameters))))

    if interval is None:
        interval = weather_adapter["temporal"]["intervals"][0]
    fake.update({"interval": interval})

    if weather_adapter["temporal"]["historic"]["start"] is not None:
        if time_start is None:
            start = weather_adapter["temporal"]["historic"]["start"]
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
        fake.update(dict(timeStart=time_start, timeEnd=time_end, ignoreErrors="true"))

    if weather_adapter["access_type"] == "location":
        if weather_adapter["spatial"]["countries"] is None:
            fake["latitude"] = random.uniform(0, 90) if latitude is None else latitude
            fake["longitude"] = (
                random.uniform(0, 180) if longitude is None else longitude
            )
        else:
            cmap = country_mapping()
            faker = Faker()
            lat, lng, _, _, _ = faker.local_latlng(
                cmap[weather_adapter["spatial"]["countries"][0]]
            )
            fake["longitude"] = float(lng)
            fake["latitude"] = float(lat)
    elif weather_adapter["access_type"] == "stations":
        if station_id is None:
            features = weather_adapter["spatial"]["geoJSON"]["features"]
            ids = [int(random.uniform(1, 100))]
            if len(features) > 0:
                if "id" in features[0]:
                    ids = [item["id"] for item in features]
                else:
                    ids = [item["properties"]["id"] for item in features]
            station_id = random.sample(ids, 1)[0]
        fake.update(dict(weatherStationId=station_id))
    else:
        raise ValueError("Unknown access type : " + weather_adapter["access_type"])

    return fake


def weather_data(
    parameters=(1001, 1002),
    time_start=None,
    time_end=None,
    interval=3600,
    length=3,
    longitude=None,
    latitude=None,
    altitude=None,
    data=None,
    valid_spatial=None,
):
    """generate a dict complying IPMDecision weatherData schema"""
    fake = {}

    try:
        iter(parameters)
    except TypeError:
        parameters = list(parameters)
    fake["weatherParameters"] = [int(p) for p in parameters]

    assert interval in [3600, 86400]
    if time_start is None:
        if time_end is not None:
            if interval == 3600:
                time_start = time_end - datetime.timedelta(hours=length - 1)
            else:
                time_start = time_end - datetime.timedelta(days=length - 1)
        else:
            time_start = datetime.datetime.today().astimezone()
    else:
        time_start = datetime.datetime.fromisoformat(time_start).astimezone()
    width = len(parameters)
    if data is None:
        if time_end is None:
            if interval == 3600:
                time_end = time_start + datetime.timedelta(hours=length - 1)
            else:
                time_end = time_start + datetime.timedelta(days=length - 1)
        else:
            time_end = datetime.datetime.fromisoformat(time_end).astimezone()
            delta = time_end - time_start
            assert delta.total_seconds() >= 0, "time_end should be after time_start"
            if interval == 3600:
                hours = delta.total_seconds() // 3600
                length = int(hours) + 1
            else:
                length = int(delta.days) + 1
        data = [
            [p / 10 for p in random.sample(range(100), width)] for _ in range(length)
        ]
    else:
        assert len(data) > 0
        assert len(data[0]) == width, (
            "data should be a list of tuples, each being as long as parameters"
        )
        length = len(data)
        if interval == 3600:
            time_end = time_start + datetime.timedelta(hours=length - 1)
        else:
            time_end = time_start + datetime.timedelta(days=length - 1)

    fake["timeStart"] = time_start.isoformat()
    fake["timeEnd"] = time_end.isoformat()
    fake["interval"] = interval

    if valid_spatial is None:
        lng = random.uniform(0, 180)
        lat = random.uniform(0, 90)
    else:
        cmap = country_mapping()
        faker = Faker()
        lat, lng, _, _, _ = faker.local_latlng(cmap[valid_spatial])
    if longitude is None:
        longitude = lng
    if latitude is None:
        latitude = lat
    if altitude is None:
        altitude = 0

    fake["locationWeatherData"] = [
        {
            "longitude": longitude,
            "latitude": latitude,
            "altitude": altitude,
            "data": data,
            "length": length,
            "width": width,
        }
    ]

    return fake


def default_weather_period(model, current_year=None):
    if current_year is None:
        current_year = datetime.datetime.now().year
    previous_year = current_year - 1
    period = {"start": None, "end": None}
    for w in period:
        items = model["input"]["weather_data_period_" + w]
        for item in items:
            if item["determined_by"] == "FIXED_DATE":
                period[w] = item["value"].format(
                    CURRENT_YEAR=current_year, PREVIOUS_YEAR=previous_year
                )
                break  # items is a priority list
            elif item["determined_by"] == "INPUT_SCHEMA_PROPERTY":
                d = model["execution"]["input_schema"]["properties"]
                path = item["value"].split(".")
                for p in path[:-1]:
                    d = d[p]["properties"]
                period[w] = d[path[-1]]["default"].format(
                    CURRENT_YEAR=current_year, PREVIOUS_YEAR=previous_year
                )
                break
    return period["start"], period["end"]


def model_weather_data(model, time_start=None, time_end=None, length=3):
    """Generate fake weather data along spec given in model"""
    if model["input"]["weather_parameters"] is None:
        return None
    parameters = [
        item["parameter_code"] for item in model["input"]["weather_parameters"]
    ]
    interval = model["input"]["weather_parameters"][0]["interval"]
    start, end = default_weather_period(model)
    if time_start is None:
        if time_end is not None:
            start = None  # let use length
    else:
        start = time_start
    if time_end is None:
        if time_start is not None:
            end = None
    else:
        end = time_end
    valid_spatial = None
    if "valid_spatial" in model:
        if "countries" in model["valid_spatial"]:
            if len(model["valid_spatial"]["countries"]) > 0:
                valid_spatial = model["valid_spatial"]["countries"][0]
    return weather_data(
        parameters=parameters,
        time_start=start,
        time_end=end,
        interval=interval,
        length=length,
        valid_spatial=valid_spatial,
    )


def model_field_observations(
    model,
    quantifications,
    latitude=None,
    longitude=None,
    time=None,
    pest=None,
    crop=None,
):
    """generate common part of field observation

    quantification is a list of dict, each being a {k:value}"""
    length = len(quantifications)
    latitude = random.uniform(0, 90) if latitude is None else latitude
    longitude = random.uniform(0, 180) if longitude is None else longitude
    location = json.loads(Geojson_point.format(longitude=longitude, latitude=latitude))
    if time is None:
        start = datetime.datetime.today().astimezone()
        time = [(start + datetime.timedelta(days=i)).isoformat() for i in range(length)]
    if pest is None:
        pest = random.sample(model["pests"], 1)[0]
    if crop is None:
        crop = random.sample(model["crops"], 1)[0]
    field_obs = [
        {
            "fieldObservation": {
                "location": location,
                "time": time[i],
                "pestEPPOCode": pest,
                "cropEPPOCode": crop,
            },
            "quantification": quantifications[i],
        }
        for i in range(length)
    ]
    return field_obs


def set_default(fake_value, schema):
    if isinstance(fake_value, dict):
        for k, v in fake_value.items():
            fake_value[k] = set_default(v, schema["properties"][k])
    else:
        fake_value = schema.get("default", fake_value)
        if schema["type"] == "number":
            fake_value = float(fake_value)
        if schema["type"] == "integer":
            fake_value = int(fake_value)
    if isinstance(fake_value, str):
        current_year = datetime.datetime.now().year
        previous_year = current_year - 1
        fake_value = fake_value.format(
            CURRENT_YEAR=current_year, PREVIOUS_YEAR=previous_year
        )
    return fake_value


def set_all_required(schema):
    schema["required"] = list(schema["properties"].keys())
    for k, v in schema["properties"].items():
        if v["type"] == "object":
            schema["properties"][k] = set_all_required(v)
    return schema


def input_data(
    model,
    weather_data=None,
    field_observations=None,
    requires_all=True,
    check_default=True,
):
    if model["execution"]["type"] == "LINK":
        return None
    else:
        input_schema = deepcopy(model["execution"]["input_schema"])

    weather = False
    fieldobs = False
    fieldloc = input_schema
    fakeloc = []
    if model["input"] is None:
        pass
    else:
        if model["input"]["weather_parameters"] is not None:
            weather = True
            input_schema["properties"]["weatherData"] = {
                "type": "string",
                "pattern": "^WEATHER_DATA$",
            }
            if "weatherData" not in input_schema["required"]:
                input_schema["required"].append("weatherData")
        if model["input"]["field_observation"] is not None:
            if "fieldObservations" in fieldloc["properties"]:
                fieldobs = True
            else:
                for prop in fieldloc["properties"]:
                    if fieldloc["properties"][prop]["type"] == "object":
                        if (
                            "fieldObservations"
                            in fieldloc["properties"][prop]["properties"]
                        ):
                            fieldobs = True
                            fieldloc = fieldloc["properties"][prop]
                            fakeloc.append(prop)
                            break
            if fieldobs:
                fieldloc["properties"]["fieldObservations"]["minItems"] = 1
                if "fieldObservations" not in fieldloc["required"]:
                    fieldloc["required"].append("fieldObservations")
                fieldloc["properties"]["fieldObservations"]["items"]["properties"][
                    "fieldObservation"
                ] = {"type": "string", "pattern": "^FIELD_OBSERVATION$"}
                fieldloc["properties"]["fieldObservations"]["items"]["required"] = [
                    "fieldObservation",
                    "quantification",
                ]

    if requires_all:
        if input_schema["type"] == "object":
            input_schema = set_all_required(input_schema)

    jsf_faker = JSF(input_schema)
    fake = jsf_faker.generate()

    if check_default:
        for k, v in fake.items():
            fake[k] = set_default(v, input_schema["properties"][k])

    if weather:
        if weather_data is None:
            weather_data = model_weather_data(model)
        fake["weatherData"] = weather_data
        for w in ("start", "end"):
            for bound in model["input"]["weather_data_period_" + w]:
                if bound["determined_by"] == "INPUT_SCHEMA_PROPERTY":
                    d = fake
                    fields = bound["value"].split(".")
                    for field in fields[:-1]:
                        d = d[field]
                    assert fields[-1] in d, (
                        "weather_data_period_"
                        + w
                        + " not found in input_schema properties, but refered in model input to be there (use FIXED _DATE instead)"
                    )
                    d[fields[-1]] = weather_data["time" + w[0].upper() + w[1:]]
                    if model["input"]["weather_parameters"][0]["interval"] > 3600:
                        d[fields[-1]] = d[fields[-1]][:10]  # datetime -> date
                    break
    if fieldobs:
        d = fake
        for prop in fakeloc:
            d = d[prop]
        if field_observations is None:
            quantifications = [
                item["quantification"] for item in d["fieldObservations"]
            ]
            field_observations = model_field_observations(model, quantifications)
        d["fieldObservations"] = field_observations

    return fake


# TODO: add interpreters for model meta for wralea
