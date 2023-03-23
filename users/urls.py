from django.urls import path
from .views import users,register,login,logout,AuthenticatedUser

urlpatterns = [
    path('users', users),
    path('register',register),
    path('login',login),
    path('logout',logout),
    path('user',AuthenticatedUser.as_view()), #class not function
]