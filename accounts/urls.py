from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register_user'),
    path('login/', views.UserLoginView.as_view(), name='login_user'),
    path('logout/', views.UserLogoutView.as_view(), name='logout_user'),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
