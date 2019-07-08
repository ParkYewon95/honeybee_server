from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from honeybee_user import views
from django.contrib.auth import views as auth_views
from knox import views as knox_views
from .views import RegistrationAPI,LoginAPI,UserAPI ,UserViewSet


user_list = views.UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
urlpatterns = [
    path('honeybee_user/', views.UserList.as_view()),
    path('honeybee_user/<pk>/', views.UserDetail.as_view()),
    path('picture/',views.PictureList.as_view()),
    path('picture/<pk>',views.PictureDetail.as_view()),
    path('tmppicture/',views.TmpPictureList.as_view(),name='tmppicture-list'),
    path('tmppicture/<int:pk>',views.TmpPictureDetail.as_view(),name='tmppicture-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    
    path('auth/login/',views.LoginAPI.as_view(),name='login'),
    #path('auth/logout/',knox_views.LogoutView.as_view,name='logout'),
    path('auth/register/',views.RegistrationAPI.as_view(),name='sign_up'),
    #path('auth/login/',LoginAPI.as_view()),
    path('auth/user/',views.UserAPI.as_view(),name='user'),
    #path('sign_up/',auth_views.LoginView.as_view(),name='login'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)