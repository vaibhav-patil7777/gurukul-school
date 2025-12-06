from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    short_desc = models.TextField()
    long_desc = models.TextField(blank=True)
    image = models.ImageField(upload_to="courses/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MediaItem(models.Model):
    MEDIA_TYPES = (("image","Image"),("video","Video"))
    file = models.FileField(upload_to="gallery/")
    type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    event_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.event_name}"


class Like(models.Model):
    media = models.ForeignKey(MediaItem, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    media = models.ForeignKey(MediaItem, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ContactInfo(models.Model):
    school_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    principal = models.CharField(max_length=200)
    chairman = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    open_time = models.CharField(max_length=50)
    close_time = models.CharField(max_length=50)

    def __str__(self):
        return self.school_name
