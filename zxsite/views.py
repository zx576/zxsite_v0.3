from django.shortcuts import render
from .models import Article,Bloger,Tag
# Create your views here.
def index(request):
    article = Article.objects.get(id=1)
    content = {
        'article':article
    }
    return render(request,'zxsite/index.html',content)