from django.urls import path
from main.views import UserList, UserDetails, UserCreate, LoginView, LogoutView, UploadImage, AllImagesList, UserImagesList, UserEdit, ImageRetrieve

urlpatterns = [
    path('users/', UserList.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/register/', UserCreate.as_view()),
    path('users/<int:id>/', UserDetails.as_view()),
    path('users/<int:pk>/edit/', UserEdit.as_view()),
    path('images/', AllImagesList.as_view()),
    path('images/<int:pk>/', ImageRetrieve.as_view()),
    path('images/create/', UploadImage.as_view()),
    path('users/<int:pk>/images/', UserImagesList.as_view())

]