from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import User, Plant

def userLogin(request):
    if request.method == 'GET':
      return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return render(request, 'planted_trees.html')
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_plants(request):
    if request.method == 'GET':
        plants = Plant.objects.all()
        return Response([{'name': plant.name, 'scientific_name': plant.scientific_name} for plant in plants], status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




# @api_view(['POST'])
# def login(request):
#     if request.method == 'POST':
#         username = request.data.get('username')
#         password = request.data.get('password')
        
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         if user.check_password(password):
#             return Response({'message': 'User logged in'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
#     else:
#         return Response({'error': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    