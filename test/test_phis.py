import requests
from agroservices.phis.phis import Phis


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

    # Connexion test
    token, status_code = phis.authenticate()
    assert status_code == 200
    
    # Wrong password test
    try:
        token, status_code = phis.authenticate(password='wrong')
    except ValueError as e:
        assert str(e) == "User does not exists, is disabled or password is invalid"

    # Wrong identifier test
    try:
        token, status_code = phis.authenticate(identifier='wrong')
    except ValueError as e:
        assert str(e) == "User does not exists, is disabled or password is invalid"


def test_get_experiment():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_experiment(token=token)
    assert data['result'] != [], "Request failed"

    # Filtered search test 
    data = phis.get_experiment(token=token, year=2022, is_ended=True, is_public=True)
    assert data['result'] != [], "Request failed"

    # Filtered search test without results
    data = phis.get_experiment(token=token, year=200)
    assert data['result'] == [], "Expected no results, got data: " + data['result']

    # Test with a valid URI
    try:
        data = phis.get_experiment(uri='m3p:id/experiment/g2was2022', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)

    # Test with an invalid URI
    try:
        data = phis.get_experiment(uri='m3p:id/experiment/wrong', token=token)
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"


def test_get_variable():
    phis = Phis()
    token, _ = phis.authenticate()
    
    # Search test
    data = phis.get_variable(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_variable(uri='http://phenome.inrae.fr/m3p/id/variable/ev000020', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)

    # Test with an invalid URI
    try:
        data = phis.get_variable(uri='http://phenome.inrae.fr/m3p/id/variable/wrong', token=token)
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"


def test_get_project():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_project(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"
    
    # Test with a valid URI
    try:
        data = phis.get_project(uri='m3p:id/project/vitsec', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)

    # Test with an invalid URI
    try:
        data = phis.get_project(uri='m3p:id/project/wrong', token=token)
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"


def test_get_facility():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_facility(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_facility(uri='m3p:id/organization/facility.phenoarch', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)

    # Test with an invalid URI
    try:
        data = phis.get_facility(uri='m3p:id/organization/wrong', token=token)
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"
    

def test_get_germplasm():
    phis = Phis()
    token, _ = phis.authenticate()
    
    # Search test
    data = phis.get_germplasm(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_germplasm(uri='http://aims.fao.org/aos/agrovoc/c_1066', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)

    # Test with an invalid URI
    try:
        data = phis.get_germplasm(uri='http://aims.fao.org/aos/agrovoc/wrong', token=token)
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"


def test_get_device():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_device(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"
    
    # Test with a valid URI
    try:
        data = phis.get_device(uri='http://www.phenome-fppn.fr/m3p/ec1/2016/sa1600064', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)

    # Test with an invalid URI
    try:
        data = phis.get_device(uri='http://www.phenome-fppn.fr/m3p/ec1/2016/wrong', token=token)
    except Exception as err:
        assert True  # Exception is expected
    else:
        assert False, "Expected an exception, but none was raised"

    
def test_get_annotation():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_annotation(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    # No URIs
    # try:
    #     data = phis.get_annotation(uri='', token=token)
    # except Exception as err:
    #     assert False, "Unexpected error: " + str(err)


def test_get_document():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_document(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_document(uri='m3p:id/document/test_dataset', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_factor():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_factor(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    # No URIs
    # try:
    #     data = phis.get_factor(uri='', token=token)
    # except Exception as err:
    #     assert False, "Unexpected error: " + str(err)


def test_get_organization():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_organization(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_organization(uri='m3p:id/organization/phenoarch', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_site():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_site(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    # No URIs
    # try:
    #     data = phis.get_site(uri='', token=token)
    # except Exception as err:
    #     assert False, "Unexpected error: " + str(err)


def test_get_scientific_object():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_scientific_object(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_scientific_object(uri='m3p:id/scientific-object/za20/so-0001zm4531eppn7_lwd1eppn_rep_101_01arch2020-02-03',
                                           token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_species():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_species(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"


def test_get_system_info():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_system_info(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"


def test_get_characteristic():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_characteristic(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_characteristic(uri='http://phenome.inrae.fr/m3p/id/variable/characteristic.humidity', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_entity():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_entity(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_entity(uri='http://phenome.inrae.fr/m3p/id/variable/entity.solar', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_entity_of_interest():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_entity_of_interest(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    # No URIs
    # try:
    #     data = phis.get_entity_of_interest(uri='', token=token)
    # except Exception as err:
    #     assert False, "Unexpected error: " + err


def test_get_method():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_method(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"
    
    # Test with a valid URI
    try:
        data = phis.get_method(uri='http://phenome.inrae.fr/m3p/id/variable/method.measurement', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_unit():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_unit(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_unit(uri='http://qudt.org/vocab/unit/J', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_provenance():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_provenance(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_provenance(uri='http://www.phenome-fppn.fr/m3p/Prov_watering_WateringStation05_6l', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)


def test_get_datafile():
    phis = Phis()
    token, _ = phis.authenticate()

    # Search test
    data = phis.get_datafile(token=token)
    if data['metadata']['pagination']['totalCount'] != 0:
        assert data['result'] != [], "Request failed"

    # Test with a valid URI
    try:
        data = phis.get_datafile(uri='m3p:id/file/1597964400.af46ac07f735ced228cf181aa85ebced', token=token)
    except Exception as err:
        assert False, "Unexpected error: " + str(err)