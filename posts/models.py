from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_soft_deleted = models.BooleanField(default=False)


class User(AbstractUser):

    GENDER = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )
    TYPE = (
        ("student", "Student"),
        ("teacher", "Teacher"),
    )

    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)
    profile = models.ImageField(
        upload_to="users/profile",
        max_length=254,
        default="/users/profile/user-profile.png",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def img_preview(self):
        return mark_safe(f'<img src = "{self.profile.url}" width = "300"/>')

    def __str__(self):
        return "{}".format(self.name)


class Posts(BaseModel):
    PUBLISH_TYPE = (
        ("public", "Public"),
        ("private", "Private"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    dislikes = models.ManyToManyField(User, related_name="dislikes", blank=True)
    image = models.ImageField(blank=True, null=True, upload_to="posts")
    desciption = models.TextField()

    @property
    def likes_count(self):
        return self.likes.all().count()

    @property
    def dislikes_count(self):
        return self.dislikes.all().count()

    @property
    def total_comments(self):
        return self.comments.all().count()

    def __str__(self) -> str:
        return f"{self.user.email} -- {self.title}"


class Comments(BaseModel):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.post.title} -- {self.user.email}"
