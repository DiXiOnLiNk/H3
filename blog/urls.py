from django.urls import path
from .views import (
    PostListCreate, PostDetail,
    CommentListCreate, CommentDetail,
    RegisterView, CustomTokenObtainPairView,
    AdminOnlyView
)

urlpatterns = [
    # --- Post ---
    path('posts/', PostListCreate.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),

    # --- Comment ---
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),

    # --- Auth ---
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
]

