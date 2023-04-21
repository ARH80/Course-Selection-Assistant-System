from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-change/', views.PasswordChangeAPIView.as_view()),
    path('forget-password/', views.SendForgetPassword.as_view()),
    path('reset-password/', views.ResetPasswordAPIView.as_view()),
    path('profile/', views.UserProfileAPI.as_view()),
    path('check-secret/', views.CheckSecret.as_view())
]
