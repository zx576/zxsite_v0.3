from django.shortcuts import render,redirect,HttpResponse,render_to_response
from .models import Article,Bloger,Tag,Comment
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
import datetime
from django.template.loader import render_to_string
from .forms import PortraitForm
from django.db.models import Q

#---------------------主页--------------------------------------------------
def index(request):
    articles = Article.objects.all().order_by('-created_time')
    content = {
        'articles':articles
    }
    return render(request,'zxsite/index.html',content)
#---------------------管理页--------------------------------------------------

def manage(request):
    articles = Article.objects.filter(status='P').order_by('-created_time')
    tags = Tag.objects.filter(status='L')
    content = {
        'articles':articles,
        'tags':tags
    }
    return render(request,'zxsite/manage.html',content)

#---------------------登录--------------------------------------------------
def log_in(request):
    print(request.POST)
    print(request.GET)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            if request.GET.get('next'):
                return redirect(request.GET['next'])
            else:
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
        # print(tags_list)
        status = request.POST.get('status')
        useri = User.objects.get(id=userid)
        # print(useri)
        bloger = Bloger.objects.get(user=useri)
        atcid = request.POST.get('atcid')
        # print(atcid)
        abstarct = content[:100]+'......'
        if atcid == 'new':
            newatc = Article.objects.create(
                title = title,
                content = content,
                author = bloger,
                status = status,
                abstract = abstarct
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
            atc_ins.abstract = abstarct
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

#---------------------展示文章--------------------------------------------------

def article_ins(request,atc_id):
    # print(atc_id)
    atc_ins = Article.objects.get(id = atc_id)
    #暂时的解决办法
    atc_ins.views += 1
    atc_ins.save()
    comments = Comment.objects.filter(article=atc_ins).order_by('-created_time')
    content = {
        'article':atc_ins,
        'comments':comments
    }
    return render(request,'zxsite/article_ins.html',content)

#浏览量函数
# def countview(request):
#     article = Article.

#添加评论
def newcomment(request,atc_id):
    if request.method == 'POST':
        context = request.POST.get('context')
        print('step context')
        article = Article.objects.get(id=atc_id)
        if request.user.is_authenticated:
            user = request.user
            blogger = Bloger.objects.get(user=user)
        else:
            user = User.objects.get(username__exact='anonymous_user')
            blogger = Bloger.objects.get(user=user)
        newcomment_ins = Comment.objects.create(
            context = context,
            article = article,
            author = blogger,
            status = 'L'
        )
        # user = serializers.serialize('json',[user])
        comments = Comment.objects.filter(article=article).order_by('-created_time')
        # tags = Tag.objects.all()
        content = {
            'comments':comments
            # 'article':article
            # 'tags':tags
        }

        return render_to_response('zxsite/comment-inner.html',content)


#---------------------About--------------------------------------------------
# @staff_member_required(login_url='/login/',redirect_field_name='next')
# @permission_required('zxsite.add_article',login_url='/login/')
@user_passes_test(lambda u : u.is_staff,login_url='/login/',redirect_field_name='next')
def about(request):
    # return render_to_response('zxsite/about.html')
    return render(request,'zxsite/about.html')

#---------------------index--------------------------------------------------
# def indexbydate(request):
#     articles = Article.objects.all().order_by('-created_time')[:5]
#     content = {
#         'articles':articles
#     }
#     return render(request,'zxsite/indexbydate.html',content)

#bydate
def indexbydate(request):
    article_list = Article.objects.all()
    date_list = datelist(article_list)
    article_list = article_list.order_by('-created_time')
    print(article_list)
    paginator = Paginator(article_list,3)
    total_page = paginator.num_pages
    if request.method == 'POST':
        print(request.POST)
        clicktime = int(request.POST.get('clicktime'))
        page = clicktime
        if page > total_page:
            return HttpResponse('end')
        articles = paginator.page(page)
        articles = serializers.serialize('json',articles)
        content = {
            'articles': articles,
        }

        return JsonResponse(content)
    else:
        articles = paginator.page(1)
        content = {
            'articles':articles,
            'datelist': date_list
        }
        return render(request,'zxsite/indexbydate.html',content)

def datelist(atc_list):
    thisyear = datetime.date.today().year
    year = thisyear
    result = {}
    default_data = {}
    while True:
        atc = atc_list.filter(created_time__year = year)
        if len(atc) > 0 :
            result[year] = default_data
            for i in range(1,13):
                # default_data[i] = []
                atc_month = atc.filter(created_time__month = i).order_by('-created_time')
                print(type(atc_month))
                default_data[i] = atc_month
                print(default_data)
            year -= 1
        else:
            break

    print(result)
    return result
#---------------------indexbytag--------------------------------------------------
#bytag
def indexbytag(request):
    tags = Tag.objects.all().order_by('created_time')

    content = {
        'tags':tags
    }
    return render(request,'zxsite/indexbytag.html',content)

#tag instance
def tag_ins(request,tagid):
    tag = Tag.objects.get(id=tagid)
    articles = tag.article_set.all().order_by('-created_time')
    content ={
        'tag':tag,
        'articles':articles
    }
    return render(request,'zxsite/tag-ins.html',content)

#---------------------edituser--------------------------------------------------
#修改用户信息
#
# def edituser(request,userid):
#     user = request.user
#     bloger = Bloger.objects.get(user=user)
#     if request.method == 'POST':
#         form = PortraitForm(request.POST,request.FILES)
#         print(request.POST)
#         print(request.FILES)
#         if form.is_valid():
#             bloger.portrait = request.FILES['picfile']
#             bloger.save()
#             return redirect('/user/%s'%(userid))
#     else:
#         form = PortraitForm()
#     content = {
#         'user':user,
#         'bloger':bloger,
#         'form':form
#     }
#     return render(request,'zxsite/userinfo.html',content)

def edituser(request,userid):
    user = request.user
    bloger = Bloger.objects.get(user_id=userid)
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        try:
            bloger.portrait = request.FILES['picfile']
            bloger.signiture = request.POST.get('signiture')
            bloger.save()
            return redirect('/user/%s' % (userid))
        except:
            bloger.signiture = request.POST.get('signiture')
            bloger.save()
            return HttpResponse('success')

    content = {
        'user':user,
        'bloger':bloger,
        # 'form':form
    }
    return render(request,'zxsite/userinfo.html',content)

#---------------------search--------------------------------------------------
def search(request):
    # print(request.GET)
    if request.method == 'GET':
        search_content = request.GET.get('search')
        search_article_result = Article.objects.filter(status='P').filter(
            Q(title__contains=search_content) | Q(content__contains=search_content)
        )
        search_user_result = User.objects.filter(is_active=True).filter(
            Q(username__contains=search_content) | Q(email__contains=search_content)
        )
        # search_bloger_result = Bloger.objects.filter(
        #      Q(signiture__contains=search_content)
        # )
        if len(search_article_result) == 0:
            search_article_result = []
        if len(search_user_result) == 0:
            search_user_result = []
        # if len(search_bloger_result) == 0:
        #     search_bloger_result = []

        content = {
            'articles': search_article_result,
            'users': search_user_result,
            # 'blogers': search_bloger_result
        }
        return render(request, 'zxsite/search.html', content)

def managedit(request):
    article_list = Article.objects.filter(status='E').order_by('-created_time')
    paginator = Paginator(article_list,5)
    total_page = paginator.num_pages
    if request.method == 'POST':
        getpage = request.POST.get('getpage')
        if total_page < getpage:
            return HttpResponse('end')
        articles = paginator.page(getpage)
        content = {
            'articles':articles
        }
        return  render_to_response('zxsite/ajaxarticles.html',)
    else:
        articles = paginator.page(1)
        content = {
            'articles': articles
        }
        return render(request,'zxsite/m-edit.html',content)

#删除文章
def deletearticle(request,atc_id):
    article = Article.objects.get(id=atc_id)
    article.status = 'D'
    article.save()
    return redirect('/manage/')

#编辑文章
def editarticle(request,atc_id):
    article = Article.objects.get(id=atc_id)
    tags = Tag.objects.filter(article=article)
    str_tags = ''
    for tag in tags:
        str_tags += tag.name +';'

    print(str_tags)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag_list = request.POST.get('tags')
        tags = handletags(tag_list)
        status = request.POST.get('status')
        article.title = title
        article.content = content
        for tag in tags:
            article.tags.add(tag)
        article.save()
        return HttpResponse('saved')
    content = {
        'article':article,
        'tags':str_tags
    }
    return render(request,'zxsite/editarticle.html',content)

def managedelete(request):
    articles = Article.objects.filter(status='D').order_by('-created_time')
    content = {
        'articles':articles
    }
    return render(request,'zxsite/recyclebin.html',content)

def truelydeletearticle(request,atc_id):
    article = Article.objects.get(id=atc_id)
    article.status = 'C'
    article.save()
    return redirect('/manage/')


def redit(request,atc_id):
    article = Article.objects.get(id=atc_id)
    article.status = 'E'
    article.save()
    return redirect('/manage/')

# def errorpage(request):
#     return render(request,'zxsite/errors.html')

# echarts 学习
def echarts(request):
    content = {}
    return render(request,'zxsite/echarts.html',content)