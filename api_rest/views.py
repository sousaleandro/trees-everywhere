from django.shortcuts import redirect, render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import Plant, PlantedTree


# Login view to authenticate user
def userLogin(request):
    if request.method == 'GET':
      return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            planted_trees = PlantedTree.objects.filter(user=user)
            return render(request, 'planted_trees.html', {'planted_trees': planted_trees})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Get all planted trees from authenticated user
def get_planted_trees(request):
    user = request.user
    try:
        user.is_authenticated
    except:
        return redirect('login')
    
    planted_trees = PlantedTree.objects.filter(user=user)
    return render(request, 'planted_trees.html', {'planted_trees': planted_trees})

# Get details from a planted tree from authenticated user
def get_planted_tree_details(request, planted_tree_id):
    user = request.user
    try:
        planted_tree = PlantedTree.objects.get(id=planted_tree_id, user=user)
    except PlantedTree.DoesNotExist: 
        return Response({'error': 'Plant not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return render(request, 'planted_tree_details.html', {'planted_tree': planted_tree})
