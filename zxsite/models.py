from django.db import models
from django.contrib.auth.models import User
#userprofile
class Article(models.Model):
    author = models.ForeignKey('Bloger', verbose_name='作者')
    # tags = models.ManyToManyField('Tag', verbose_name='标签')
    title = models.CharField('标题', max_length=50)
    content = models.TextField('正文')
    # abstract = models.CharField('摘要', max_length=50)
    ARTICLE_STATUS = (
        ('P', 'PUBLIC'),
        ('E', 'EDITING'),
        ('D', 'DELETED'),
        ('C', 'DELETE-COMPELETLY')
    )
    status = models.CharField('文章状态', max_length=1, choices=ARTICLE_STATUS)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    lasted_modified_time = models.DateTimeField('最新修改时间', auto_now=True)
    views = models.PositiveIntegerField('浏览数', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    topped = models.BooleanField('是否置顶', default=False)

    def __str__(self):
        return self.title

    # 按修改时间排列
    class meta:
        ordering = ['-lasted_modified_time']

class Bloger(models.Model):
    user = models.OneToOneField(User)
    likelist = models.ManyToManyField('Bloger', verbose_name='关注列表', null=True, blank=True,
                                      related_name='re_likelists')
    # nickname = models.CharField(max_length=20, null=True, blank=True)
    # age = models.PositiveIntegerField(default=0)
    portrait = models.ImageField('头像', upload_to='pic/', default='pic/timg.jpg')
    GENDER_CHOICE = (
        ('F', 'FEMALE'),
        ('M', 'MALE')
    )
    gender = models.CharField(max_length=5, choices=GENDER_CHOICE)
    signiture = models.CharField(max_length=100)
    # address = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.CharField(verbose_name='标签名',max_length=20)
    TAG_STATUS = (
        ('L','LIVE'),
        ('D','DEAD')
    )
    status = models.CharField(max_length=5,choices=TAG_STATUS)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    related_articles = models.PositiveIntegerField('相关文章数')

    def __str__(self):
        return self.name

    class meta:
        ordering = ['-related_articles']