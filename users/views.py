from django.contrib.auth.models import User
from django.shortcuts import (
    get_object_or_404,
    render
)
from rest_framework.generics import (
    RetrieveAPIView
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    MeSerializer,
    MeFullSerializer
)


# Create your views here.


""" Get infos on current user """
class Me(APIView):
    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)

""" Get infos on current user """
class MeFull(APIView):
    def get(self, request):
        serializer = MeFullSerializer(request.user)
        return Response(serializer.data)



class Test(RetrieveAPIView):

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)
