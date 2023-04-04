from django.urls import path
from .views import users,register,login,logout,AuthenticatedUser,PredictionClass,example_view

urlpatterns = [
    path('users', users),
    path('register',register),
    path('login',login),
    path('logout',logout),
    path('user',AuthenticatedUser.as_view()),
    path('predict',PredictionClass.as_view()), #class not function
    path('check_predict',example_view),
]