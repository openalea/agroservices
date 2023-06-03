# run pytest with -rP option to see which service passes
import pytest
from agroservices.ipm.ipm import IPM
import agroservices.ipm.fakers as ipm_fakers


ipm = IPM()
link = ipm.get_dss('LINK')
onthefly = ipm.get_dss('ONTHEFLY')

link_dss_models = sum([[(d,m) for m in v['models']] for d,v in link.items()],[])
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


onthefly_dss_models = sum([[(d, m) for m in v['models']] for d, v in onthefly.items()], [])
@pytest.mark.parametrize('dss,model', onthefly_dss_models)
def test_faker_dss_onthefly(dss, model):
    m = onthefly[dss]['models'][model]
    assert m['execution']['type'] == 'ONTHEFLY'
    assert 'endpoint' in m['execution']
    assert len(m['execution']['endpoint']) > 0
    assert 'input_schema' in m ['execution']
    assert len(m['execution']['input_schema']) > 0
    fake = ipm_fakers.input_data(m)
    assert isinstance(fake, dict)
