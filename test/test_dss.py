# run pytest -rA --tb=no to see which service passes
import pytest
from agroservices.ipm.ipm import IPM
import agroservices.ipm.fakers as ipm_fakers
from agroservices.services import Service
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
exclude = ['adas.datamanipulation'] # server not reachable


@pytest.mark.parametrize('dss,model', noweather_nofield)
def test_dss_noweathernofield(dss, model):
    if dss not in exclude:
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
        raise NotImplementedError(dss + ' curently in exclude list (server is probably down)')


@pytest.mark.parametrize('dss,model', weather_nofield)
def test_dss_weathernofield(dss, model):
    if dss not in exclude:
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
        raise NotImplementedError(dss + ' curently in exclude list (server is probably down)')

@pytest.mark.parametrize('dss,model', field)
def test_dss_field(dss, model):
    if dss not in exclude:
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
        raise NotImplementedError(dss + ' curently in exclude list (server is probably down)')