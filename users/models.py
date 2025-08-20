from django.db import models
from django.contrib.auth.models import User




# User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(
    max_length=10,
    choices=[
        ("male", "Male"),
        ("female", "Female"),
    ]
)

    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
    upload_to='profile_pics/',
    default='profile_pics/male-avatar.png'
)
    banner_image = models.ImageField(upload_to='banner_pics/', default='default.jpg')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

