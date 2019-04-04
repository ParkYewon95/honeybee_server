from honeybee_user.models import HoneyBeeUser
from honeybee_user.serializer import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# class USERLIST(APIView):
#     """
#     List all user, or create a new user
#     """
#     def get(self,request,format=None):
#         honeybee_user = HoneyBeeUser.objects.all()
#         serializer = UserSerializer(honeybee_user,many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serailizer = UserSerializer(data=request.data)
#         if serailizer.is_valid():
#             serailizer.save()
#             return Response(serailizer.data, status=status.HTTP_201_CREATED)
#         return Response(serailizer.errors,status=status.HTTP_400_BAD_REQUEST)

# class USERDETAIL(APIView):
#     def get_object(self, pk):
#         try:
#             return HoneyBeeUser.objects.get(pk=pk)
#         except HoneyBeeUser.DoesNotExist:
#             raise Http404
#     def get(self,request,pk,format=None):

#         return Response(serailizer.data)
    

