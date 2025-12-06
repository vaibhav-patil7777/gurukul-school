from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("courses/", views.courses, name="courses"),
    path("course/<int:pk>/", views.course_detail, name="course_detail"),
    path("gallery/", views.gallery, name="gallery"),
    path("media/<int:pk>/", views.media_detail, name="media_detail"),
    path("contact/", views.contact, name="contact"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("upload/", views.upload_media, name="upload_media"),
    path("like/<int:pk>/", views.like_media, name="like_media"),
    path("comment/<int:pk>/", views.comment_media, name="comment_media"),
]
