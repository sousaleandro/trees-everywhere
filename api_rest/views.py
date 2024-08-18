from django.shortcuts import redirect, render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

from .serializer import PlantedTreeSerializer
from .models import Plant, PlantedTree, Account


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
            accounts = Account.objects.filter(active=True)
            return render(request, 'home.html', {'accounts': accounts})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Home view to select an account and see user Profile
def home(request):
    user = request.user
    try:
        user.is_authenticated
    except:
        return redirect('login')
    
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        account = Account.objects.get(id=account_id)
        request.session['selected_account'] = account_id
        user.accounts.add(account)
        return redirect('planted_trees')

    accounts = Account.objects.filter(active=True)
    return render(request, 'home.html', {'accounts': accounts})

# Profile view to see user information
def get_profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

# Get all planted trees from authenticated user
def get_planted_trees(request):
    user = request.user
    account_id = request.session.get('selected_account')
    try:
        user.is_authenticated
    except:
        return redirect('login')
    
    account = Account.objects.get(id=account_id)
    planted_trees = PlantedTree.objects.filter(user=user, account=account)
    return render(request, 'planted_trees.html', {'planted_trees': planted_trees})

# Get details from a planted tree from authenticated user
def get_planted_tree_details(request, planted_tree_id):
    user = request.user
    try:
        planted_tree = PlantedTree.objects.get(id=planted_tree_id, user=user)
    except PlantedTree.DoesNotExist: 
        return Response({'error': 'Plant not found'}, status=status.HTTP_404_NOT_FOUND)

    return render(request, 'planted_tree_details.html', {'planted_tree': planted_tree})

# Create a planted tree from authenticated user
def plant_tree(request):
    user = request.user
    account_id = request.session.get('selected_account')
    try:
        user.is_authenticated
    except:
        return redirect('login')

    if request.method == 'POST':
        plant_name = request.POST.get('plant')
        location = request.POST.get('location')
        plant = Plant.objects.get(name=plant_name)
        account = Account.objects.get(id=account_id)
        user.plant_tree(account, (plant, location))
        return redirect('planted_trees')
    else:
        plants = Plant.objects.all()
        return render(request, 'plant_tree.html', {'plants': plants})
    
# This view is used to return a json with all trees planted by the authenticated user in all accounts
@api_view(['GET'])
def get_planted_trees_api(request):
    user = request.user
    try:
        user.is_authenticated
    except:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
    planted_trees = PlantedTree.objects.filter(user=user)
    serializer = PlantedTreeSerializer(planted_trees, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
