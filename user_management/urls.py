from django.urls import path
from .views import UserCreateView, LoginView, UserRetrieveOrDeleteView, ChangePasswordView, UserListView

urlpatterns = [
    path('account/users', UserCreateView.as_view()),
    path('account/users/all/', UserListView.as_view()),
    path('account/users/<int:id>/', UserRetrieveOrDeleteView.as_view()),
    path('account/users/password_change', ChangePasswordView.as_view()),
    path('account/login', LoginView.as_view())
]