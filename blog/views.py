from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, RegisterSerializer
from .permissions import IsAdmin

# --- POST CRUD ---
class PostListCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Приклад захисту, можна змінити

    @swagger_auto_schema(
        responses={200: PostSerializer(many=True)}
    )
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PostSerializer,
        responses={201: PostSerializer()}
    )
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={200: PostSerializer()}
    )
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PostSerializer,
        responses={200: PostSerializer()}
    )
    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: 'Deleted successfully'}
    )
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- COMMENT CRUD ---
class CommentListCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={200: CommentSerializer(many=True)}
    )
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CommentSerializer,
        responses={201: CommentSerializer()}
    )
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={200: CommentSerializer()}
    )
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CommentSerializer,
        responses={200: CommentSerializer()}
    )
    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: 'Deleted successfully'}
    )
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- AUTH VIEWS ---

# Реєстрація
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Користувача створено"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Логін через JWT (проксі для simplejwt)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass  # можна кастомізувати

# Приклад захищеного вью з IsAdmin
class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"message": "Привіт, адміністраторе!"})
