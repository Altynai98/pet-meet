from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions

from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('sign_up/', views.SignUpAPIView.as_view()),
    path('sign_in/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('sign_in/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.UserIndexAPIView.as_view()),
    path('users/<int:user_id>/', views.UserDetailAPIView.as_view()),
    path('groups/', views.GroupIndexAPIView.as_view()),
    path('groups/<int:group_id>/', views.GroupDetailAPIView.as_view()),  # if we want to see all posts of a group
    path('groups/<int:group_id>/posts/', views.PostIndexAPIView.as_view()),
    path('posts/<int:pk>/', views.PostDetailAPIView.as_view()),
    path('groups/<int:group_id>/meetings/', views.MeetingIndexAPIView.as_view()),
    path('meetings/<int:pk>/', views.MeetingDetailAPIView.as_view()),
    path('meetings/<int:meeting_id>/attend', views.MeetingAttendAPIView.as_view()),
    path('meetings/<int:meeting_id>/unattend', views.MeetingUnattendAPIView.as_view()),
    path('posts/<int:post_id>/comments/', views.CommentIndexAPIView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailAPIView.as_view()),
    path('animals/', views.AnimalCreateAPIView.as_view()),
    path('animals/<int:pk>/', views.AnimalDetailAPIView.as_view()),
    path('users/<int:user_id>/animals/', views.AnimalIndexAPIView.as_view())
]
