# run pytest with -rP option to see which service passes
import pytest
from agroservices.ipm.ipm import IPM
import agroservices.ipm.fakers as ipm_fakers

ipm = IPM()
link = ipm.get_dss('LINK')
onthefly = ipm.get_dss('ONTHEFLY')

link_dss_models = sum([[(d, m) for m in v['models']] for d, v in link.items()], [])
onthefly_dss_models = sum([[(d, m) for m in v['models']] for d, v in onthefly.items()], [])


@pytest.mark.parametrize('dss,model', link_dss_models)
def test_dss_link(dss, model):
    m = link[dss]['models'][model]
    assert m['execution']['type'] == 'LINK'
    assert 'endpoint' in m['execution']
    if m['execution']['endpoint'] == '':
        assert 'description_URL' in m
    assert ipm_fakers.input_data(m) is None
    try:
        res = ipm.run_model(m)
        assert isinstance(res, str)
    except:
        raise
    else:
        print ('ok')


@pytest.mark.parametrize('dss,model', onthefly_dss_models)
def test_dss_onthefly(dss, model):
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
        raise
    else:
        'ok'
