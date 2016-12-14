from django.shortcuts import render,redirect,HttpResponse
from .models import Article,Bloger,Tag
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
#---------------------主页--------------------------------------------------
def index(request):
    article = Article.objects.get(id=1)
    content = {
        'article':article
    }
    return render(request,'zxsite/index.html',content)
#---------------------管理页--------------------------------------------------
def manage(request):
    articles = Article.objects.all()
    tags = Tag.objects.all()
    content = {
        'articles':articles,
        'tags':tags
    }
    return render(request,'zxsite/manage.html',content)

#---------------------登录--------------------------------------------------
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            return redirect('/')
        else:
            return redirect('/login/')
    return render(request,'zxsite/login.html')
#---------------------注销--------------------------------------------------
def log_out(request):
    logout(request)
    return redirect('/')

#---------------------注销--------------------------------------------------
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_ins = User.objects.create_user(
            username = username,
            password = password
        )
        Bloger.objects.create(
            user = user_ins
        )
        newuser = authenticate(username=username,password=password)
        login(request,newuser)
        return redirect('/')

    return render(request,'zxsite/register.html')
def verifyname(request):
    print(request.POST)
    username = request.POST.get('name')
    print(username)
    result = User.objects.filter(username__exact=username)
    if len(result):
        content = {
            'data':'F'
        }
    else:
        content = {
            'data':'T'
        }
    return JsonResponse(content)
#---------------------新建文章--------------------------------------------------
def newarticle(request):
    return render(request,'zxsite/newarticle.html')
#保存文章
def savearticle(request):
    if request.method == 'POST':
        print(request.POST)
        userid = int(request.POST.get('userid'))
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags')
        tags_list = handletags(tags) ###处理tags
        print(tags_list)
        status = request.POST.get('status')
        useri = User.objects.get(id=userid)
        print(useri)
        bloger = Bloger.objects.get(user=useri)
        atcid = request.POST.get('atcid')
        print(atcid)
        if atcid == 'new':
            newatc = Article.objects.create(
                title = title,
                content = content,
                author = bloger,
                status = status,
            )
            # newatc = Article.objects.get(title__exact=title)
            print(newatc)
            for i in tags_list:
                newatc.tags.add(i)
            newatc.save()
            content = {
                'atcid':newatc.id
            }
        else:
            atc_ins = Article.objects.get(id=atcid)
            atc_ins.title = title
            atc_ins.content = content
            atc_ins.author = bloger
            atc_ins.status = status
            for i in tags_list:
                atc_ins.tags.add(i)
            atc_ins.save()
            content ={
                'atcid':atc_ins.id
            }
        return JsonResponse(content)

#处理tags
def handletags(tags):
    tags = tags.split(';')
    tags = [i for i in tags if i]
    print(tags)
    tags_list = []
    for tag in tags:
        try:
            j_tag = Tag.objects.get(name__exact=tag)
            # j_tag.related_articles += 1
            # j_tag.save()
        except:
            j_tag = Tag.objects.create(
                name = tag,
                related_articles = 1,
                status = 'L'
            )
        tags_list.append(j_tag)
    return tags_list