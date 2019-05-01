from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from honeybee_user import views

urlpatterns = [
    path('honeybee_user/', views.USERLIST.as_view()),
    path('honeybee_user/<pk>/', views.USERDETAIL.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

