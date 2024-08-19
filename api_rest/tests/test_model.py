import pytest
from api_rest.models import User, PlantedTree, Account, Tree

def test_user_method_plant_tree():
    leandroUser = User.objects.get(username='leandro')
    alphaAccount = Account.objects.get(name='alpha')
    pineTree = Tree.objects.get(name='scotch pine')
    location = (32.123456, -50.123456)

    leandroUser.plant_tree(pineTree, location, alphaAccount)
    
    plantedTree = PlantedTree.objects.filter(user=leandroUser).last()

    assert plantedTree.user == leandroUser
    assert plantedTree.tree == pineTree
    assert plantedTree.account == alphaAccount

def test_user_method_to_plant_multiple_trees():
    leandroUser = User.objects.get(username='leandro')
    betaAccount = Account.objects.get(name='beta')
    guavaTree = Tree.objects.get(name='apple guava')
    cherryTree = Tree.objects.get(name='wild cherry')
    guavaLocation = (31.123456, -59.123456)
    cherryLocation = (62.123456, -40.123456)
    trees_data = [(guavaTree, guavaLocation), (cherryTree, cherryLocation)]

    leandroUser.plant_trees(trees_data, betaAccount)
    
    plantedTrees = PlantedTree.objects.filter(user=leandroUser)

    assert plantedTrees.count() == 6
    assert plantedTrees.filter(tree=guavaTree).count() == 2
    assert plantedTrees.filter(tree=cherryTree).count() == 2
    assert plantedTrees.filter(account=betaAccount).count() == 4
    assert plantedTrees.filter(user=leandroUser).count() == 6
    assert plantedTrees.filter(planted_at__isnull=False).count() == 6


