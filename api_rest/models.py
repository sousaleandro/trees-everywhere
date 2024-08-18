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
    def plant_tree(self, account, tree_data):
        plant, location = tree_data
        PlantedTree.objects.create(
            user=self,
            plant=plant,
            planted_at=timezone.now(),
            age=0,
            account=account,
            location=location
        )
    
    # Method to plant multiple trees
    def plant_trees(self, account, trees_data):
        for tree_data in trees_data:
            plant, location = tree_data
            PlantedTree.objects.create(
                user=self,
                plant=plant,
                planted_at=timezone.now(),
                age=0,
                account=account,
                location=location
            )
            

# Account model with name, created date, active status and relationship with users
class Account(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, related_name='accounts', blank=True)

    def __str__(self):
        return f'Account: {self.name} | Active: {self.active}'

# Plant model with name and scientific name
class Plant(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'Plant: {self.name} | Scientific name: {self.scientific_name}'

# PlantedTree model with user, plant, planted_at, age, account and location    
class PlantedTree(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    age = models.IntegerField()
    planted_at = models.DateTimeField()
    #location is a tuple of latitude and longitude(lat, long) TO BE IMPLEMENTED
    location = models.CharField(max_length=100)

    def __str__(self):
        return f'Planted at: {self.planted_at} | Age: {self.age} | Location: {self.location} | User: {self.user.first_name} {self.user.last_name}'