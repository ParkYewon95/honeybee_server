from django.forms import widgets
from honeybee_user.models import HoneyBeeUser, PictureInfo
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):  

    class Meta:
        model = HoneyBeeUser
        fields = ('id','name','profile_pic','introduce','total_like','total_down')
        read_only_fields=('id')

"""
class PicInfoSerializer(serializers.ModelSerializer):
    #user pk
    user = serializers.PrimaryKeyRelatedField(many=True,read_only=True)

    class Meta:
        model = PictureInfo
        field=('user')
"""


