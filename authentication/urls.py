from django.urls import path
from .views import SignUpView, LoginView, UserView, LogoutView, GetCSRFToken, CheckUsersView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user'),
    path('get-csrf-token/', GetCSRFToken.as_view(), name='get-csrf-token'),
    path('check-users/', CheckUsersView.as_view(), name='check-users'),
]