import pytest
from rest_framework.test import APIClient
from api_rest.models import User, Tree, Account, PlantedTree

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        userLeandro = User.objects.create_user(username='leandro', password='1234')
        userAyla = User.objects.create_user(username='ayla', password='1234')
        userLouise = User.objects.create_user(username='louise', password='1234')

        alphaAcc = Account.objects.create(name='alpha')
        betaAcc = Account.objects.create(name='beta')

        pineTree = Tree.objects.create(name='scotch pine', scientific_name='Pinus sylvestris')
        guavaTree = Tree.objects.create(name='apple guava', scientific_name='Psidium guajava')
        cherryTree = Tree.objects.create(name='wild cherry', scientific_name='Prunus avium')

        alphaAcc.users.add(userLeandro, userLouise)
        betaAcc.users.add(userLeandro, userAyla)

        userLeandro.plant_tree(pineTree, (49.123456, -83.123456), alphaAcc)
        userLeandro.plant_tree(guavaTree, (10.123456, 90.123456), alphaAcc)
        userLeandro.plant_tree(pineTree, (89.123456, 180.123456), betaAcc)
        userLeandro.plant_tree(cherryTree, (12.123456, -20.123456), betaAcc)

        userAyla.plant_tree(guavaTree, (49.123456, -83.123456), betaAcc)
        userAyla.plant_tree(cherryTree, (10.123456, 90.123456), betaAcc)

        userLouise.plant_tree(cherryTree, (49.123456, -83.123456), alphaAcc)
        userLouise.plant_tree(guavaTree, (12.123456, -20.123456), alphaAcc)

        