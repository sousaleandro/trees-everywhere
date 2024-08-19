from django.shortcuts import redirect, render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .serializer import PlantedTreeSerializer
from .models import Tree, PlantedTree, Account


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
    planted_trees = PlantedTree.objects.filter(user=user)
    return render(request, 'home.html',{
        'accounts': accounts,
        'planted_trees': planted_trees
        })

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
    planted_trees = PlantedTree.objects.filter(account=account)

    return render(request, 'planted_trees.html', {
        'planted_trees': planted_trees,
        'account': account,
        })

# Get details from a planted tree from authenticated user
@login_required(login_url='/auth/login/')
@api_view(['GET'])
def get_planted_tree_details(request, planted_tree_id):
    user = request.user
    try:
        planted_tree = PlantedTree.objects.get(id=planted_tree_id)
    except PlantedTree.DoesNotExist: 
        return Response({'error': 'Tree not found'}, status=status.HTTP_404_NOT_FOUND)

    if planted_tree.user != user:
        return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    return render(request, 'planted_tree_details.html', {'planted_tree': planted_tree})

# Create a planted tree from authenticated user
@login_required(login_url='/auth/login/')
@api_view(['GET', 'POST'])
def plant_tree(request):
    user = request.user
    account_id = request.session.get('selected_account')

    if request.method == 'POST':
        tree_id = request.POST.get('tree_id')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        tree = Tree.objects.get(id=tree_id)
        account = Account.objects.get(id=account_id)
        user.plant_tree(tree, (latitude, longitude), account)
        return redirect('planted_trees')
    else:
        trees = Tree.objects.all()
        return render(request, 'plant_tree.html', {'trees': trees})
    
# This view is used to return a json with all trees planted by the authenticated user in all accounts
@login_required(login_url='/auth/login/')
@api_view(['GET'])
def get_planted_trees_api(request):
    user = request.user
    planted_trees = PlantedTree.objects.filter(user=user)
    serializer = PlantedTreeSerializer(planted_trees, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
