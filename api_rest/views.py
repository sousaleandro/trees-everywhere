from django.shortcuts import redirect, render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .serializer import PlantedTreeSerializer
from .models import Plant, PlantedTree, Account


# Login view to authenticate user
@api_view(['GET', 'POST'])
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
@login_required(login_url='/auth/login/')
@api_view(['GET', 'POST'])
def home(request):
    user = request.user
    
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        account = Account.objects.get(id=account_id)
        request.session['selected_account'] = account_id
        user.accounts.add(account)
        return redirect('planted_trees')

    accounts = Account.objects.filter(active=True)
    return render(request, 'home.html', {'accounts': accounts})

# Profile view to see user information
@login_required(login_url='/auth/login/')
@api_view(['GET'])
def get_profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

# Get all planted trees from authenticated user
@login_required(login_url='/auth/login/')
@api_view(['GET'])
def get_planted_trees(request):
    user = request.user
    account_id = request.session.get('selected_account')
    
    account = Account.objects.get(id=account_id)
    planted_trees = PlantedTree.objects.filter(user=user, account=account)
    return render(request, 'planted_trees.html', {'planted_trees': planted_trees})

# Get details from a planted tree from authenticated user
@login_required(login_url='/auth/login/')
@api_view(['GET'])
def get_planted_tree_details(request, planted_tree_id):
    user = request.user
    try:
        planted_tree = PlantedTree.objects.get(id=planted_tree_id, user=user)
    except PlantedTree.DoesNotExist: 
        return Response({'error': 'Plant not found'}, status=status.HTTP_404_NOT_FOUND)

    return render(request, 'planted_tree_details.html', {'planted_tree': planted_tree})

# Create a planted tree from authenticated user
@login_required(login_url='/auth/login/')
@api_view(['POST'])
def plant_tree(request):
    user = request.user
    account_id = request.session.get('selected_account')

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
@login_required(login_url='/auth/login/')
@api_view(['GET'])
def get_planted_trees_api(request):
    user = request.user
    planted_trees = PlantedTree.objects.filter(user=user)
    serializer = PlantedTreeSerializer(planted_trees, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
