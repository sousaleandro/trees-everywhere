from api_rest.models import User, PlantedTree, Account, Tree


def test_user_method_plant_tree():
    leandro_user = User.objects.get(username='leandro')
    alpha_account = Account.objects.get(name='alpha')
    pine_tree = Tree.objects.get(name='scotch pine')
    location = (32.123456, -50.123456)

    leandro_user.plant_tree(pine_tree, location, alpha_account)

    planted_tree = PlantedTree.objects.filter(user=leandro_user).last()

    assert planted_tree.user == leandro_user
    assert planted_tree.tree == pine_tree
    assert planted_tree.account == alpha_account


def test_user_method_to_plant_multiple_trees():
    leandro_user = User.objects.get(username='leandro')
    beta_account = Account.objects.get(name='beta')
    guava_tree = Tree.objects.get(name='apple guava')
    cherry_tree = Tree.objects.get(name='wild cherry')
    guava_location = (31.123456, -59.123456)
    cherry_location = (62.123456, -40.123456)
    trees_data = [(guava_tree, guava_location), (cherry_tree, cherry_location)]

    leandro_user.plant_trees(trees_data, beta_account)

    planted_trees = PlantedTree.objects.filter(user=leandro_user)

    assert planted_trees.count() == 6
    assert planted_trees.filter(tree=guava_tree).count() == 2
    assert planted_trees.filter(tree=cherry_tree).count() == 2
    assert planted_trees.filter(account=beta_account).count() == 4
    assert planted_trees.filter(user=leandro_user).count() == 6
    assert planted_trees.filter(planted_at__isnull=False).count() == 6
