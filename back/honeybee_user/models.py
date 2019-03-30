import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
'''
class HoneyBeeManager(BaseUserManager):
    def create_user(self, id, name, email, password):
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
        user.save(using=self._db)
        return user

    def create_superuser(self, id, name, email,password):
        user = self.create_user(id,name,email,password)
        user.is_superuser = True
        user.save(using=self._db)
        return user
'''

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

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ('email',)

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
    
    def __str__(self):
        return self.name