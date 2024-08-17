from django.shortcuts import redirect, render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
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

    accounts = Account.objects.filter(active=True)
    return render(request, 'home.html', {'accounts': accounts})

# Profile view to see user information
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

# Select account view to see user information
def select_account(request):
    user = request.user
    try:
        user.is_authenticated
    except:
        return redirect('login')

    account_id = request.POST.get('account_id')
    account = Account.objects.get(id=account_id)
    request.session['selected_account'] = account
    user.accounts.add(account)
    return redirect('planted_trees')

# Get all planted trees from authenticated user
def get_planted_trees(request):
    user = request.user
    account = request.session.get('selected_account')
    try:
        user.is_authenticated
    except:
        return redirect('login')
    
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

# # Create a planted tree from authenticated user
# def plant_trees(request):
#     user = request.user
#     account = request.account
#     try:
#         user.is_authenticated
#     except:
#         return redirect('login')

#     plant_id = request.POST.get('plant_id')
#     plant = Plant.objects.get(id=plant_id)
#     planted_tree = PlantedTree.objects.create(user=user, account=account, plant=plant)
#     return JsonResponse({'id': planted_tree.id}, status=status.HTTP_201_CREATED)