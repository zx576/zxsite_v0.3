from django.contrib import admin
from .models import Article,Tag,Bloger,Comment
admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Bloger)
admin.site.register(Comment)
# Register your models here.
