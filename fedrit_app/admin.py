from django.contrib import admin
from .models import SiteUser, Sub, Post

class SubAdmin(admin.ModelAdmin):
    pass#fields = [dstr for dstr in dir(Sub) if dstr[0] != '_']

class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sub, SubAdmin)
admin.site.register(Post, PostAdmin)
