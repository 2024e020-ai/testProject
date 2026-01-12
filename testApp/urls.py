from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostEditView,
    PostDeleteView,
    SignUpView,
    PostListAPIView,  # API用ビュー
    like_post,        # いいね機能
    pokemon           # ← ポケモンAPIビュー（新規）
)

urlpatterns = [
    # -----------------------------
    # HTML用ビュー
    # -----------------------------
    path('', PostListView.as_view(), name='timeline'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('signup/', SignUpView.as_view(), name='signup'),

    # -----------------------------
    # 認証用ビュー
    # -----------------------------
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # -----------------------------
    # いいね用（非同期通信）
    # -----------------------------
    path('post/<int:pk>/like/', like_post, name='like_post'),

    # -----------------------------
    # API用ビュー
    # -----------------------------
    path('api/posts/', PostListAPIView.as_view(), name='api-posts'),

    # -----------------------------
    # ポケモンAPI
    # -----------------------------
    path('pokemon/', pokemon, name='pokemon'),
]
