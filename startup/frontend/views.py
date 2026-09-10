from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

class home(APIView):
    def get(self, request):
        #return HttpResponse("<h1>Hello! This is my frontend.</h1>")
        return Response({
            "name": "onyo",
        })