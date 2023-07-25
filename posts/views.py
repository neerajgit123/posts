from django.shortcuts import render
from django.shortcuts import redirect, render
from .forms import UserRegisterForm, LoginForm
from .models import Posts, Comments
from django.urls import reverse_lazy
from django.contrib.auth import logout as auth_logout, authenticate, login as l
from django.views.generic import RedirectView
from django.views import View
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        posts = Posts.objects.all()
        return render(request, "posts/home.html", context={"posts": posts})


class LogoutView(RedirectView):
    pattern_name = "login-view"

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class LoginView(View):
    form = LoginForm()

    def get(self, request):
        context = {"form": self.form}
        return render(request, "posts/login.html", context)

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                l(request, user)
                return redirect("home-view")
        else:
            context = {"form": form}
            return render(request, "posts/login.html", context)


class RegisterView(View):
    form = UserRegisterForm()

    def get(self, request):
        context = {"form": self.form}
        return render(request, "posts/registration.html", context)

    def post(self, request):
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            if user is not None:
                l(request, user)
                return redirect("home-view")
        else:
            context = {"form": form}
        return render(request, "posts/registration.html", context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    fields = ["title", "image", "desciption"]
    success_url = reverse_lazy("home-view")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Posts
    template_name_suffix = "_update_form"
    fields = ["title", "image", "desciption"]
    success_url = reverse_lazy("home-view")


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Posts.objects.filter(id=post_id).first()
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return redirect("home-view")


class PostDislikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Posts.objects.filter(id=post_id).first()
        user = request.user
        if user in post.dislikes.all():
            post.dislikes.remove(user)
        else:
            post.dislikes.add(user)
        return redirect("home-view")


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Posts
    success_url = reverse_lazy("home-view")


class PostCommentsView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        comments = Comments.objects.filter(post__id=post_id).order_by("-id")
        context = {"comments": comments}
        return render(request, "posts/comments.html", context)

    def post(self, request, post_id=None):
        comment = request.POST.get("comment")
        post = Posts.objects.filter(id=post_id).first()
        Comments.objects.create(user=request.user, comment=comment, post=post)
        return redirect("post-comments-view", post_id=post_id)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comments
    success_url = reverse_lazy("home-view")
