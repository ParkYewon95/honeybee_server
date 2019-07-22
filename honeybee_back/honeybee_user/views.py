from .models import HoneyBeeUser,PictureInfo,TmpPicture
from .serializers import CreatePictureSerializer,CreateUserSerializer,HoneyBeeUserSerializer,PicInfoSerializer,UserSerializer,TmpPictureInfoSerializer,LoginUserSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from django.http import Http404
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route
from style_transfer import Transfer
import os
import base64
from pprint import pprint

# class LoginView(KnoxLoginView):
#     authentication_classes = (permissions.IsAuthenticated)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         # login(request, user)
#         return super(LoginView, self).post(request, format=None)

class RegistrationAPI(generics.GenericAPIView): 
    serializer_class= CreateUserSerializer 
        
    def post(self,request,*args, **kwargs):
        
        if len(request.data["username"]) < 4 or len(request.data["password"]) < 4 :
            body = {"message":"short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        (instance, token) = AuthToken.objects.create(user)
       
        return Response(
            {
                "user": UserSerializer(user,context=self.get_serializer_context()).data,
                "token": token,
            }
        )



class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data
        (instance, token) = AuthToken.objects.create(user)
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": token,
            }
        )

class UserList(APIView):
    def get(self,request,format=None):
        honeybee_user = HoneyBeeUser.objects.all()
        serializer = HoneyBeeUserSerializer(honeybee_user,many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serailizer = UserSerializer(data=request.data) #honeybeeuserserializer
        if serailizer.is_valid():
            serailizer.save()
            return Response(serailizer.data, status=status.HTTP_201_CREATED)
        return Response(serailizer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return HoneyBeeUser.objects.get(pk=pk)
        except ValueError :
            raise Http404
    def get(self,request,pk,format=None):
        user = self.get_object(pk)
        serializer = HoneyBeeUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = HoneyBeeUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPI(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    permission_classes=[permissions.IsAuthenticated, ]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    # def get_queryset(self):
    #     return User.objects.all()
   
    # def get_queryset(self):
    #     return self.request.user.objects.all()
    def perform_create(self, serializer):
        serializer.save(username=self.request.user)

# owner별로 picture         
class PictureViewSet(viewsets.ModelViewSet):
    
    permission_classes=[permissions.IsAuthenticated, ]
    serializer_class = PicInfoSerializer

    def get_queryset(self):
        id = self.request.user.id
        # print("{id}".format(id=id))
        pictures = PictureInfo.objects.all()
        result = []
        for picture in pictures:
            # print("picture_owner:{owner}".format(owner=picture.owner))
            # pprint(vars(picture))
            if picture.owner_id == id:
                result.append(picture)
        return result

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
      
#사진 List 표시 - main
class PictureList(APIView):
    #permission_classes=[permissions.IsAuthenticated, ]
    def get(self, request, format=None):
        pictureinfo = PictureInfo.objects.all()
        serializer = PicInfoSerializer(pictureinfo, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PicInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def PictureAPI(request):

#     # if serializer.is_valid():
#     #     serializer.save()
#     #     return Response(serializer.data)
#     # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, format=None):
#         pictureinfo = PictureInfo.objects.all()
#         serializer = PicInfoSerializer(pictureinfo)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CreatePictureSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PictureDetail(APIView):
    def get_object(self, pk):
        try:
            return PictureInfo.objects.get(pk=pk)
        except PictureInfo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pictureinfo = self.get_object(pk)
        serializer = PicInfoSerializer(pictureinfo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        pictureinfo = self.get_object(pk)
        serializer =PicInfoSerializer(pictureinfo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        pictureinfo = self.get_object(pk)
        pictureinfo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Deep Learning - style transfer
class TmpPictureList(APIView):
    def get(self, request, format=None):
        pictureinfo = TmpPicture.objects.all()
        serializer = TmpPictureInfoSerializer(pictureinfo, many=True)
        return Response(serializer.data)

    # post and response to client with style changed image
    def post(self, request, format=None):
        serializer = TmpPictureInfoSerializer(data=request.data)

        if serializer.is_valid():
            # validate filter name
            filter_names = [
                'cezanne',
                'duchamp',
                'kandinsky', 
                'katsushika', 
                'monet', 
                'picabia',
                'vangogh'
            ]
            # filter name by request data
            filter_info = serializer.validated_data['filter_info']

            # if not validate filter name => return error response
            # else => save serializer
            if filter_info not in filter_names:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()

            # picture name for save
            pic_name = serializer.data['pic_address']
            result_pic_name = '/results/rest_'+pic_name.split('/')[-1].split('.')[0]+'.png'

            # style transfer, save image
            transfer = Transfer(filter_info,"honeybee_user")
            transfer.transform_image(os.getcwd()+pic_name, os.getcwd()+result_pic_name)

            # get style changed image
            # encoding base64
            # return response with image
            with open(os.getcwd()+result_pic_name, "rb") as imageFile:
                result_image = base64.b64encode(imageFile.read())
                return HttpResponse(result_image,status=status.HTTP_201_CREATED,content_type="image/png")
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TmpPictureDetail(APIView):
    def get_object(self, pk):
        try:
            return TmpPicture.objects.get(pk=pk)
        except TmpPicture.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pictureinfo = self.get_object(pk)
        serializer = TmpPicInfoSerializer(pictureinfo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        pictureinfo = self.get_object(pk)
        serializer = TmpPicInfoSerializer(pictureinfo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        pictureinfo = self.get_object(pk)
        pictureinfo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)