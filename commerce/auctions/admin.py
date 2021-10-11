from django.contrib import admin

from .models import Listning, Bid, Comment

admin.site.register(Listning)
admin.site.register(Bid)
admin.site.register(Comment)
# Register your models here.
