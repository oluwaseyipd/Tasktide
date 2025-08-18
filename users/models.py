from django.db import models
from django.contrib.auth.models import User





def get_default_avatar(gender):
    if gender == "female":
        return "media/profile_pics/female-avatar.png"
    return "media/profile_pics/male-avatar.png"


# User Profile
class Profile(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='media/profile_pics/', default='male-avatar.png')
    banner_image = models.ImageField(upload_to='media/banner_pics/', default='default.jpg')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.profile_image:  # if no image uploaded
            self.profile_image = get_default_avatar(self.gender)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Profile"

