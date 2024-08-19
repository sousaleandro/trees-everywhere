from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# User model with profile informations such as about and joined
class User(AbstractUser):
    about = models.TextField(blank=True)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User: {self.first_name} {self.last_name}'

    # Method to plant a tree
    def plant_tree(self, tree, location, account):
        latitude, longitude = location
        PlantedTree.objects.create(
            user=self,
            tree=tree,
            planted_at=timezone.now(),
            age=0,
            account=account,
            latitude=latitude,
            longitude=longitude
        )

    # Method to plant multiple trees
    def plant_trees(self, trees_data, account):
        for tree_data in trees_data:
            tree, location = tree_data
            latitude, longitude = location
            PlantedTree.objects.create(
                user=self,
                tree=tree,
                planted_at=timezone.now(),
                age=0,
                account=account,
                latitude=latitude,
                longitude=longitude
            )


# Account model with name, created date,
# active status and relationship with users
class Account(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, related_name='accounts', blank=True)

    def __str__(self):
        return f'Account: {self.name} | Active: {self.active}'


# Tree model with name and scientific name
class Tree(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)

    def __str__(self):
        return f'Tree: {self.name} | Scientific name: {self.scientific_name}'


# PlantedTree model with user, tree, planted_at,
# age, account, latitude and longitude
class PlantedTree(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    age = models.IntegerField()
    planted_at = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    def __str__(self):
        return (
            f'Planted at: {self.planted_at} | Age: {self.age} | '
            f'Location: ({self.latitude}, {self.longitude}) | '
            f'User: {self.user.first_name} {self.user.last_name}'
        )
