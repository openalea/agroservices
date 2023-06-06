import pytest
from agroservices.ipm.ipm import IPM
from agroservices.ipm import fakers as ipm_fakers

ipm = IPM()
onthefly = ipm.get_dss('ONTHEFLY')
link = ipm.get_dss('LINK')
link_dss_models = sum([[(d, m) for m in v['models']] for d, v in link.items()], [])
onthefly_dss_models = sum([[(d, m) for m in v['models']] for d, v in onthefly.items()], [])

noweather_nofield = [(d, m) for d, m in onthefly_dss_models if
                                         onthefly[d]['models'][m]['input'] is None]
input_not_none = [(d, m) for d, m in onthefly_dss_models if
                                         onthefly[d]['models'][m]['input'] is not None]
weather_nofield = [(d, m) for d, m in input_not_none if
                   (onthefly[d]['models'][m]['input']['weather_parameters'] is not None)
                   & (onthefly[d]['models'][m]['input']['field_observation'] is None)]
field = [(d, m) for d, m in input_not_none if
                   onthefly[d]['models'][m]['input']['field_observation'] is not None]

@pytest.mark.parametrize('dss,model', link_dss_models)
def test_dss_link(dss, model):
    m = link[dss]['models'][model]
    assert m['execution']['type'] == 'LINK'
    assert 'endpoint' in m['execution']
    if m['execution']['endpoint'] == '':
        assert 'description_URL' in m
    assert ipm_fakers.input_data(m) is None
    res = ipm.run_model(m)
    assert isinstance(res, str)


@pytest.mark.parametrize('dss,model', noweather_nofield)
def test_faker_dss_onthefly_noweather_nofield(dss, model):
    m = onthefly[dss]['models'][model]
    assert m['execution']['type'] == 'ONTHEFLY'
    assert 'endpoint' in m['execution']
    assert len(m['execution']['endpoint']) > 0
    assert 'input_schema' in m['execution']
    assert len(m['execution']['input_schema']) > 0
    fake = ipm_fakers.input_data(m)
    assert isinstance(fake, dict)


@pytest.mark.parametrize('dss,model', weather_nofield)
def test_faker_dss_onthefly_weather_nofield(dss, model):
    m = onthefly[dss]['models'][model]
    assert m['execution']['type'] == 'ONTHEFLY'
    assert 'endpoint' in m['execution']
    assert len(m['execution']['endpoint']) > 0
    assert 'input_schema' in m['execution']
    assert len(m['execution']['input_schema']) > 0
    assert 'weatherData' in m['execution']['input_schema']['properties']
    fake = ipm_fakers.input_data(m)
    assert isinstance(fake, dict)
    assert 'weatherData' in fake


@pytest.mark.parametrize('dss,model', field)
def test_faker_dss_onthefly_field(dss, model):
    m = onthefly[dss]['models'][model]
    assert m['execution']['type'] == 'ONTHEFLY'
    assert 'input_schema' in m['execution']
    assert len(m['execution']['input_schema']) > 0
    fake = ipm_fakers.input_data(m)
    assert isinstance(fake, dict)
