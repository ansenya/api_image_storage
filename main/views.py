import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.views import APIView

from .models import Image
from .serializers import UserSerializer, ImageSerializer

User = get_user_model()


class BaseApiView(APIView):
    def handle_exception(self, exc):
        return Response({'message': str(exc)}, status=400)


class LoginView(APIView):
    def post(self, request):
        password = request.data.get('password')
        username = request.data.get('username')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successfully"})


class UserList(generics.ListAPIView, BaseApiView):
    queryset = User.objects.all()
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveAPIView, BaseApiView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"


class UserEdit(BaseApiView):
    def put(self, request, pk):
        user = get_object_or_404(User, id=pk)
        if request.data.get('password') is not None:
            request.data.pop('password')
        if request.data.get('username') is not None:
            request.data.pop('username')
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(generics.CreateAPIView, BaseApiView):
    serializer_class = UserSerializer


class UserImagesList(BaseApiView):
    def get(self, request, pk):
        images = Image.objects.filter(author=User.objects.get(id=pk))
        images_serialized = ImageSerializer(images, many=True)
        for image in images_serialized.data:
            image['image'] = request.build_absolute_uri(image['image'])
        return Response(images_serialized.data)


class ImageRetrieve(BaseApiView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        image = get_object_or_404(Image, id=pk)
        image_serializer = ImageSerializer(image)
        image_dict = image_serializer.data
        image_dict['image'] = request.build_absolute_uri(image_serializer.data['image'])

        return Response(image_dict)

    def delete(self, request, pk):
        image = get_object_or_404(Image, id=pk)
        if image.author == request.user or request.user.is_superuser:
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)


class UploadImage(generics.CreateAPIView, BaseApiView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AllImagesList(generics.ListAPIView, BaseApiView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

