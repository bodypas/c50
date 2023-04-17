
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<str:username>", views.user_profile, name="profile"),
    path("following", views.show_following, name="following"),
    path('posts/<int:post_id>', views.update_post),
    path('posts/<int:post_id>/like', views.like_post),
    path('profile/posts/<int:post_id>/like', views.like_post),
    path('posts/<int:post_id>/likes/', views.get_like_status, name='get_like_status'),
]   
