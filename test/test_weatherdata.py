# run pytest with -rP option to see which service passes
import pytest
from agroservices.ipm.ipm import IPM
from agroservices.ipm.fakers import weather_adapter_params
from agroservices.credentials import get_credentials


def keys_exists(dict_, keys, test=all):
    return test(key in dict_ for key in keys)


def is_weatherdata(res):
    if not isinstance(res, dict):
        return False
    return all(key in res for key in ('timeStart', 'timeEnd', 'interval', 'weatherParameters',
                                                              'locationWeatherData'))
ipm = IPM()
public_bylocation=ipm.get_weatherdatasource(access_type='location', authentication_type='NONE')
public_bystations=ipm.get_weatherdatasource(access_type='stations', authentication_type='NONE')
private_bystations=ipm.get_weatherdatasource(access_type='stations', authentication_type='CREDENTIALS')


######################### Public WeatherAdaptaterService #######################

@pytest.mark.parametrize('source_id', public_bylocation.keys())
def test_weatheradapter_public_bylocation(source_id):
    source = public_bylocation[source_id]
    params = weather_adapter_params(source)
    res = ipm.get_weatheradapter(source, params)
    if isinstance(res, dict):
        assert is_weatherdata(res)
        print(source_id + ' succesively pass')
    else:
        raise ValueError(res)

@pytest.mark.parametrize('source_id', public_bystations.keys())
def test_weatheradapter_public_bystations(source_id):
    source = public_bystations[source_id]
    params = weather_adapter_params(source)
    # adapt params to point to operating stations
    if source_id == 'no.nibio.lmt':
        params['weatherStationId'] = 5
    res = ipm.get_weatheradapter(source, params)
    if isinstance(res, dict):
        assert is_weatherdata(res)
        print(source_id + ' succesively pass')
    else:
        raise ValueError(res)

ipm_credentials = get_credentials('ipm')
private_bystations = {k:v for k,v in private_bystations.items() if k in ipm_credentials}
@pytest.mark.parametrize('source_id', private_bystations.keys())
def test_weatheradapter_private_bystations(source_id):
    source = private_bystations[source_id]
    credentials = ipm_credentials[source_id]
    params = weather_adapter_params(source)
    res = ipm.get_weatheradapter(source, params, credentials)
    if isinstance(res, dict):
        assert is_weatherdata(res)
        print(source_id + ' succesively pass')
    else:
        raise ValueError(res)