import requests
from agroservices.phis.phis import Phis
from urllib.parse import quote_plus


def test_url():
    phis = Phis()
    assert phis.url is not None
    try:
        requests.get(phis.url)
    except Exception as err:
        assert False, err
    else:
        assert True


def test_authenticate():
    phis = Phis()
    token, status_code = phis.authenticate()
    assert status_code == 200
    
    try:
        token, status_code = phis.authenticate(password='wrong')
    except ValueError as e:
        assert str(e) == "User does not exists, is disabled or password is invalid"

    try:
        token, status_code = phis.authenticate(identifier='wrong')
    except ValueError as e:
        assert str(e) == "User does not exists, is disabled or password is invalid"


def test_get_list_experiment():
    phis = Phis()
    token, _ = phis.authenticate()
    
    data, received = phis.get_list_experiment(token=token, year=2022, is_ended=True, is_public=True)
    assert received, f"Request failed: {data}"

    data, received = phis.get_list_experiment(token=token, year=200)
    assert not received, f"Expected request failure, got data: {data}"


def test_get_experiment():
    phis = Phis()
    token, _ = phis.authenticate()

    # Test with a valid URI
    try:
        data = phis.get_experiment(uri='m3p:id/experiment/g2was2022', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + err

    # Test with an invalid URI
    try:
        data = phis.get_experiment(uri='m3p:id/experiment/wrong', token=token)
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"


def test_get_list_variable():
    phis = Phis()
    token, _ = phis.authenticate()
    
    data = phis.get_list_variable(token=token)
    print(data)
    assert True


def test_get_variable():
    phis = Phis()
    token, _ = phis.authenticate()
    
    # Test with a valid URI
    try:
        data = phis.get_variable(uri='http://phenome.inrae.fr/m3p/id/variable/ev000020', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + err

    # Test with an invalid URI
    try:
        data = phis.get_variable(uri='http://phenome.inrae.fr/m3p/id/variable/wrong', token=token)
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"


def test_get_list_project():
    phis = Phis()
    token, _ = phis.authenticate()
    
    data = phis.get_list_project(token=token)
    print(data)
    assert True

def test_get_project():
    phis = Phis()
    token, _ = phis.authenticate()
    
    # Test with a valid URI
    try:
        data = phis.get_project(uri='m3p:id/project/vitsec', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + err

    # Test with an invalid URI
    try:
        data = phis.get_project(uri='m3p:id/project/wrong', token=token)
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"


def test_get_list_facility():
    phis = Phis()
    token, _ = phis.authenticate()
    
    data = phis.get_list_facility(token=token)
    print(data)
    assert True


def test_get_facility():
    phis = Phis()
    token, _ = phis.authenticate()

    # Test with a valid URI
    try:
        data = phis.get_facility(uri='m3p:id/organization/facility.phenoarch', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + err

    # Test with an invalid URI
    try:
        data = phis.get_facility(uri='m3p:id/organization/wrong', token=token)
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"
    

def test_get_list_germplasm():
    phis = Phis()
    token, _ = phis.authenticate()
    
    data = phis.get_list_germplasm(token=token)
    print(data)
    assert True


def test_get_germplasm():
    phis = Phis()
    token, _ = phis.authenticate()
    
    # Test with a valid URI
    try:
        data = phis.get_germplasm(uri='http://aims.fao.org/aos/agrovoc/c_1066', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + err

    # Test with an invalid URI
    try:
        data = phis.get_germplasm(uri='http://aims.fao.org/aos/agrovoc/wrong', token=token)
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"


def test_get_list_device():
    phis = Phis()
    token, _ = phis.authenticate()
    
    data = phis.get_list_device(token=token)
    print(data)
    assert True


def test_get_device():
    phis = Phis()
    token, _ = phis.authenticate()

    data = phis.get_device(uri='http://www.phenome-fppn.fr/m3p/ec1/2016/sa1600064', token=token)
    
    # Test with a valid URI
    try:
        data = phis.get_device(uri='http://www.phenome-fppn.fr/m3p/ec1/2016/sa1600064', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + err

    # Test with an invalid URI
    try:
        data = phis.get_device(uri='http://www.phenome-fppn.fr/m3p/ec1/2016/wrong', token=token)
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"