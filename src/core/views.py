from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])  # This endpoint only supports GET requests
def ping(request):
    return Response({"message": "pong"})