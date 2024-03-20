# run pytest -rA --tb=no to see which service passes
import ujson

import pytest

from openalea.agroservices.ipm.datadir import datadir
from openalea.agroservices.ipm.ipm import IPM
import openalea.agroservices.ipm.fakers as ipm_fakers
from openalea.agroservices.services import Service


ipm = IPM()
link = ipm.get_dss('LINK')
onthefly = ipm.get_dss('ONTHEFLY')

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

timeout_exclude = ['adas.datamanipulation'] # server not reachable
# a memory of what was failing on 2023-06-06
failures = [('adas.datamanipulation', 'ALL', 'timeout'),
            ('adas.dss', 'CARPPO', 400),
            ('uk.Warwick', 'PSILRO', 404),
            ('no.nibio.vips', 'BREMIALACT', 404),
            ('no.nibio.vips', 'PSILAROBSE', 500),
            ('no.nibio.vips', 'DELIARFOBS', 500),
            ('no.nibio.vips', 'SEPAPIICOL', 500)]


@pytest.mark.parametrize('dss,model', noweather_nofield)
def test_dss_noweathernofield(dss, model):
    if dss not in timeout_exclude:
        m = onthefly[dss]['models'][model]
        assert m['execution']['type'] == 'ONTHEFLY'
        assert 'endpoint' in m['execution']
        assert len(m['execution']['endpoint']) > 0
        assert 'endpoint' in m['execution']
        fake = ipm_fakers.input_data(m)
        try:
            res = ipm.run_model(m, input_data=fake)
            assert isinstance(res, dict)
        except:
            raise ValueError(str(res) + Service.response_codes.get(res, ''))
        else:
            print('ok')
    else:
        raise NotImplementedError(dss + ' curently in timeout exclusion list')


@pytest.mark.parametrize('dss,model', weather_nofield)
def test_dss_weathernofield(dss, model):
    if dss not in timeout_exclude:
        m = onthefly[dss]['models'][model]
        assert m['execution']['type'] == 'ONTHEFLY'
        assert 'endpoint' in m['execution']
        assert len(m['execution']['endpoint']) > 0
        assert 'endpoint' in m['execution']
        fake = ipm_fakers.input_data(m)
        try:
            res = ipm.run_model(m, input_data=fake)
            assert isinstance(res, dict), res
        except:
            raise ValueError(str(res) + ' ' + Service.response_codes.get(res, ''))
        else:
            print('ok')
    else:
        raise NotImplementedError(dss + ' curently in timeout exclusion list')

@pytest.mark.parametrize('dss,model', field)
def test_dss_field(dss, model):
    if dss not in timeout_exclude:
        m = onthefly[dss]['models'][model]
        assert m['execution']['type'] == 'ONTHEFLY'
        assert 'endpoint' in m['execution']
        assert len(m['execution']['endpoint']) > 0
        assert 'endpoint' in m['execution']
        fake = ipm_fakers.input_data(m)
        try:
            res = ipm.run_model(m, input_data=fake)
            assert isinstance(res, dict), res
        except:
            raise ValueError(str(res) + ' ' + Service.response_codes.get(res, ''))
        else:
            print('ok')
    else:
        raise NotImplementedError(dss + ' curently in timeout exclusion list')


def test_run_model_field():
    #input with field observation
    model = ipm.get_model(DSSId='no.nibio.vips', ModelId='PSILAROBSE')
    path = datadir + 'model_input_psilarobse.json'
    with open(path) as json_file:
        model_input = ujson.load(json_file)
    res = ipm.run_model(model, model_input)
    assert isinstance(res, dict)
    assert 'locationResult' in res
