import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth import models as auth_models


class HoneyBeeManager(BaseUserManager):
    def create_user(self, id, name, email, password,**kwargs):
        if not id:
            raise ValueError('ID는 필수입니다!')
        if not name:
            raise ValueError('Name은 필수입니다!')
        if not email:
            raise ValueError('Email은 필수입니다!')

        user = self.model(
            id=id,
            name=name,
            email=email,
        )
        kwargs.setdefault('is_admin', False)
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, id, name, email,password,**kwargs):
        if not id:
            raise ValueError('ID는 필수입니다!')
        if not name:
            raise ValueError('Name은 필수입니다!')
        if not email:
            raise ValueError('Email은 필수입니다!')

        user = self.model(
            id=id,
            name=name,
            email=email,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user


class HoneyBeeUser(AbstractBaseUser):
    unique_id = models.UUIDField(
        primary_key = True,
        unique = True,
        editable = False,
        default = uuid.uuid4,
        verbose_name = 'pk_id',
    )
    id = models.CharField(max_length=20,unique=True,verbose_name="아이디")
    email = models.EmailField(unique=True,verbose_name="이메일")
    name = models.CharField(max_length=20,verbose_name="이름")
    profile_pic = models.ImageField(verbose_name="프로필 사진")
    introduce = models.TextField(verbose_name="소개",max_length=100,null=True,blank=True)
    total_like = models.IntegerField(verbose_name="총 좋아요 수",default=0)
    total_down = models.IntegerField(verbose_name="총 다운로드 수",default=0)

    is_admin = models.BooleanField(default=False, verbose_name='관리자 여부')
    is_staff = models.BooleanField(default=False,verbose_name="스태프 여부")
    is_active = models.BooleanField(default=True,verbose_name="활성 여부")
    is_superuser = models.BooleanField(default=False,verbose_name="슈퍼유저 여부")

    objects = HoneyBeeManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ('email','name',)

    class Meta:
        db_table='honeybee_user'
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True
        return auth_models._user_has_module_perms(self, app_label)
 
    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return auth_models._user_has_perm(self, perm, obj)

    def __str__(self):
        return self.name


def user_path(instance, filename): #파라미터 instance는 Photo 모델을 의미 filename은 업로드 된 파일의 파일 이름
    from random import choice
    import string 
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr) # 8자리 임의의 문자를 만들어 파일명으로 지정
    extension = filename.split('.')[-1] # 배열로 만들어 마지막 요소를 추출하여 파일확장자로 지정
    # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
    return '%s/%s.%s' % (instance.owner.name, pid, extension) # 예 : wayhome/abcdefgs.png

class PictureInfo(models.Model):
    pic_address = models.ImageField(upload_to = user_path)
    owner = models.ForeignKey(HoneyBeeUser,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    download = models.IntegerField(default=0)
    share = models.BooleanField(default=True)

    """
    id를 외래키로 사진에 대한 정보를 저장할 모델
    """
    
