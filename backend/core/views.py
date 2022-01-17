from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Post, Comment, PostVotes
from .serializers import (CategorySerializer, 
PostSerializer, 
CommentSerializer, 
UserSerializer, 
UserSerializerWithToken, 
PostVotesSerializer,
MyTokenObtainPairSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

# TODO: Make sure that only the CREATORS of posts can delete them.
# TODO: Maybe create my own permission class.
# TODO: Make ordering case insensitive.
class CategoryView(viewsets.ModelViewSet):
    def get_permissions(self):
        # Only users can create categories.
        if self.request.method == "POST" or self.request.method == "DELETE":
            permission_classes = [permissions.IsAuthenticated(), ]
            
        else:
            permission_classes = [permissions.AllowAny(), ]

        return permission_classes

    serializer_class = CategorySerializer
    queryset = Category.objects.order_by("name")

class PostsView(viewsets.ModelViewSet):
    def get_permissions(self):
        # Only users can create posts.
        if self.request.method == "POST" or self.request.method == "DELETE":
            permission_classes = [permissions.IsAuthenticated(), ]
            return permission_classes
            
        else:
            permission_classes = [permissions.AllowAny(), ]
            return permission_classes

    serializer_class = PostSerializer
    queryset = Post.objects.all()

# This view is for viewing posts under a certain category.
class PostsByCategoryView(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    # Only users can create posts.
    def get_permissions(self):
        # Only users can create posts.
        if self.request.method == "POST" or self.request.method == "DELETE":
            permission_classes = [permissions.IsAuthenticated(), ]
            return permission_classes
            
        else:
            permission_classes = [permissions.AllowAny(), ]
            return permission_classes

    def get_queryset(self):
        self.pk = self.kwargs["pk"]
        queryset = Post.objects.filter(category=self.pk)
        return queryset

# TODO: check if we need this partial true.
class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_permissions(self):
        # Only users can create categories.
        if self.request.method == "POST" or self.request.method == "DELETE":
            permission_classes = [permissions.IsAuthenticated(), ]
            
        else:
            permission_classes = [permissions.AllowAny(), ]

        return permission_classes

    def get_queryset(self):
        self.pk = self.kwargs["pk"]
        queryset = Post.objects.filter(id=self.pk)
        return queryset

class CommentView(viewsets.ModelViewSet):
    # Only users can comment.
    # def get_permissions(self):
    #     # Only users can create categories.
    #     if self.request.method == "POST" or self.request.method == "DELETE":
    #         permission_classes = [permissions.IsAuthenticated(), ]
            
    #     else:
    #         permission_classes = [permissions.AllowAny(), ]
        
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class PostComments(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        self.pk = self.kwargs["pk"]
        queryset = Comment.objects.filter(parent_post=self.pk)
        return queryset

@api_view(["GET"])
@permission_classes((permissions.IsAuthenticated, ))
def current_user(request):
    """
    Determine current user by their token and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    # No authentication here as this view is used to create users.
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializerWithToken(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostVotesView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = PostVotesSerializer
    queryset = PostVotes.objects.all()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer