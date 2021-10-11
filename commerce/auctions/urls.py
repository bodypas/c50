from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

# I know, there are some spelling mistakes through all this project, but left them, because didn't want to be confused later.

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:category>", views.category_pick, name="category_pick"),
    path("comments/<int:listning_id>", views.comments, name="comments"),
    path("<int:listning_id>/auction_close", views.auction_close, name="auction_close"),
    path("<int:listning_id>", views.item_detail, name="item_detail"),

] 

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
