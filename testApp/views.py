# views.py

# -----------------------------
# 既存のインポート（HTML用）
# -----------------------------
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm

# -----------------------------
# DRF のインポート（API用）
# -----------------------------
from rest_framework import generics
from .serializers import PostSerializer

# -----------------------------
# HTML用ビュー
# -----------------------------
class PostListView(ListView):
    model = Post
    template_name = 'timeline.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('author').prefetch_related('likes')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(content__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return super().get_queryset().select_related('author').prefetch_related('likes')

    def get(self, request, *args, **kwargs):
        post = self.get_object()

        # ★ デバッグ用（runserver のターミナルに表示）
        print("----- ここからデバッグ -----")
        print("投稿者:", post.author)
        print("投稿文:", post.content)
        print("----- ここまでデバッグ -----")

        return super().get(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('timeline')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('timeline')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


# -----------------------------
# API用ビュー（JSON）
# -----------------------------
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.select_related('author').prefetch_related('likes').all()
    serializer_class = PostSerializer


# -----------------------------
# 非同期いいね機能
# -----------------------------
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    context = {
        'liked': liked,
        'count': post.total_likes(),
    }
    return JsonResponse(context)


# -----------------------------
# ポケモンAPIビュー
# -----------------------------
import requests

def pokemon(request):
    pokemon_name = request.GET.get("name", "pikachu")
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        context = {
            "name": data["name"],
            "image": data["sprites"]["front_default"],
            "types": [t["type"]["name"] for t in data["types"]],
            "height": data["height"],
            "weight": data["weight"],
        }

    except Exception:
        context = {
            "error": "ポケモン情報を取得できませんでした。名前を確認してください。",
        }

    return render(request, "pokemon.html", context)
