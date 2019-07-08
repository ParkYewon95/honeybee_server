from django.db import models
import uuid
from django.contrib.auth.models import User
from random import choice
import string 

# class SignupForm(ModelForm):
#     password_check = forms.CharField(max_length=200,widget=forms.PasswordInput())
#     #field_order는 만들어지는 입력양식의 순서 정해주는 것.
#     field_order=['username','password','password_check','email']

#     class Meta:
#         model = User
#         widgets = {'password':forms.PasswordInput}
#         fields = ['username','password','email']

def profile_path(instance, filename): #파라미터 instance는 Photo 모델을 의미 filename은 업로드 된 파일의 파일 이름
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr) # 8자리 임의의 문자를 만들어 파일명으로 지정
    extension = filename.split('.')[-1] # 배열로 만들어 마지막 요소를 추출하여 파일확장자로 지정
    # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
    return '%s/%s.%s' % ("profile", pid, extension) # 예 : wayhome/abcdefgs.png

class HoneyBeeUser(models.Model):
    user = models.OneToOneField(User,related_name='honeybeeuser',on_delete=models.CASCADE,null=True)
    unique_id = models.UUIDField(
        primary_key = True,
        unique = True,
        editable = False,
        default = uuid.uuid4,
        verbose_name = 'pk_id',
    )
    profile_pic = models.ImageField(upload_to = profile_path,null=True)
    introduce = models.TextField(max_length=100,null=True)
    total_like = models.IntegerField(default=0)
    total_down = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.text
    #user_name = User.objects.get()
    
def user_path(instance, filename): #파라미터 instance는 Photo 모델을 의미 filename은 업로드 된 파일의 파일 이름
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr) # 8자리 임의의 문자를 만들어 파일명으로 지정
    extension = filename.split('.')[-1] # 배열로 만들어 마지막 요소를 추출하여 파일확장자로 지정
    # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
    return '%s/%s.%s' % (instance.owner.username, pid, extension) # 예 : wayhome/abcdefgs.png

def tmp_user_path(instance,filename): #파라미터 instance는 Photo 모델을 의미 filename은 업로드 된 파일의 파일 이름
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr) # 8자리 임의의 문자를 만들어 파일명으로 지정
    extension = filename.split('.')[-1] # 배열로 만들어 마지막 요소를 추출하여 파일확장자로 지정
    # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
    return '%s/%s.%s' % ("temp", pid, extension) # 예 : wayhome/abcdefgs.png

class PictureInfo(models.Model):
    pic_address = models.ImageField(upload_to = user_path)
    owner = models.ForeignKey(User,related_name="pic_own",on_delete=models.CASCADE,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    download = models.IntegerField(default=0)
    share = models.BooleanField(default=True)
    
    @property
    def get_username(self):
        return self.owner.username


class TmpPicture(models.Model):
    pic_address = models.ImageField(upload_to = tmp_user_path)
    filter_info = models.CharField(max_length=100)