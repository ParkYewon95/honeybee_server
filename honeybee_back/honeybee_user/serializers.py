from django.forms import widgets
from django.contrib.auth.models import User
from .models import HoneyBeeUser, PictureInfo
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','first_name',)


class HoneyBeeUserSerializer(serializers.ModelSerializer):  
    
    user = UserSerializer(required=True)
    class Meta:
        model = HoneyBeeUser
        fields = ('user','profile_pic','introduce','total_like','total_down',)
    
    '''
    def create(self,validated_data):
        users_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        #for user_data in users_data:
        User.objects.create()
        #honeybee_user, created = HoneyBeeUser.objects.update_or_create(user=user,profile_pic=validated_data.pop('subject_major'))
    '''

class PicInfoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=True,read_only=True)

    class Meta:
        model = PictureInfo
        field=('user',)




