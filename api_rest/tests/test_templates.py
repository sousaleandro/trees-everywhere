import pytest
from api_rest.models import User, PlantedTree, Account
from pytest_django.asserts import assertTemplateUsed, assertContains



def test_if_response_is_200(client):
    leandroUser = User.objects.get(username='leandro')

    client.force_login(leandroUser)
    response = client.get('/auth/home/')

    assert response.status_code == 200
    
def test_if_correct_template_for_planted_trees_by_the_user_is_rendered(client):
    leandroUser = User.objects.get(username='leandro')

    client.force_login(leandroUser)
    plantedTree = PlantedTree.objects.filter(user=leandroUser).first()
    response = client.get('/auth/home/')

    assertTemplateUsed(response, 'home.html')
    assertContains(response, plantedTree.tree.name)

def test_if_user_is_forbidden_to_see_details_of_other_users_planted_trees(client):
    leandroUser = User.objects.get(username='leandro')
    louiseUser = User.objects.get(username='louise')

    client.force_login(leandroUser)
    planted_tree = PlantedTree.objects.filter(user=louiseUser).first()

    url = f'/auth/planted_trees/details/{planted_tree.id}/'
    response = client.get(url)

    assert response.status_code == 403

# This test is not working yet and must be finished
# def test_if_correct_template_for_the_selected_account_planted_trees_is_rendered(client):
#     leandroUser = User.objects.get(username='leandro')
#     louiseUser = User.objects.get(username='louise')
#     alphaAccount = Account.objects.get(name='alpha')
#     leandroPlantedTree = PlantedTree.objects.filter(account=alphaAccount, user=leandroUser).first()
#     louisePlantedTree = PlantedTree.objects.filter(account=alphaAccount, user=louiseUser).first()

#     client.force_login(leandroUser)
#     client.session['selected_account'] = alphaAccount.id
#     client.session.save()
#     url = f'/auth/planted_trees/'
#     response = client.get(url)

#     assertTemplateUsed(response, 'planted_trees.html')
#     assertContains(response, leandroPlantedTree.user.username)
#     assertContains(response, leandroPlantedTree.tree.name)
#     assertContains(response, louisePlantedTree.user.username)
#     assertContains(response, louisePlantedTree.tree.name)
    