from django.forms import widgets
from django.contrib.auth.models import User
from .models import HoneyBeeUser, PictureInfo,TmpPicture
from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.") 

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password')
        extra_kwargs = {
            'password' : {'write_only':True}
        }
    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
  
class HoneyBeeUserSerializer(serializers.ModelSerializer):
    #user = UserSerializer(required=True)
    #user = self.get_field_names(declared_fields="username",info="") 
    #user = serializers.CharField(User.username)
    #user = serializers.CharField()
    
    class Meta:
        model = HoneyBeeUser
        fields = ('user','profile_pic','introduce','total_like','total_down',)
    
    def create(self, request, *args, **kwargs):
        # Do whatever you want here
        user = HoneyBeeUser.objects.create_user(**validated_data)
        #user = HoneyBeeUser.objects.create_user(**validated_data)
        # Then invoke the create method and create your instance
        return super().create(request, *args, **kwargs)



class PicInfoSerializer(serializers.ModelSerializer):
    #owner = serializers.CharField(max_length=None, min_length=None,trim_whitespace=True,source='get_username',read_only=True)
    class Meta:
        model = PictureInfo
        fields = '__all__'
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

class CreatePictureSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(max_length=None, min_length=None,trim_whitespace=True,source='get_username',read_only=True)
    class Meta:
        model = PictureInfo
        fields =('owner','pic_address','share') 
       
    def create(self,validated_data):
        picture = PictureInfo.objects.create(**validated_data)
        return picture


class TmpPictureInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmpPicture
        fields = ('pic_address','filter_info',)