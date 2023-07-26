from django.urls import path
from .views import (
    PostUpdateView,
    HomeView,
    RegisterView,
    LoginView,
    LogoutView,
    PostCreateView,
    PostDeleteView,
    PostLikeView,
    PostDislikeView,
    PostCommentsView,
    CommentDeleteView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home-view"),
    path("register/", RegisterView.as_view(), name="register-view"),
    path("login/", LoginView.as_view(), name="login-view"),
    path("logout/", LogoutView.as_view(), name="logout-view"),
    path("post/", PostCreateView.as_view(), name="post-create-view"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update-view"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete-view"),
    path("post/<int:post_id>/like/", PostLikeView.as_view(), name="post-like-view"),
    path(
        "post/<int:post_id>/dislike/",
        PostDislikeView.as_view(),
        name="post-dislike-view",
    ),
    path(
        "post/<int:post_id>/comments/",
        PostCommentsView.as_view(),
        name="post-comments-view",
    ),
    path(
        "comment/<int:pk>/delete/",
        CommentDeleteView.as_view(),
        name="comment-delete-view",
    ),
]
