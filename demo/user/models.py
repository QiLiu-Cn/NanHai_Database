from django.db import models

# Create your models here.
class User(models.Model):
    # 加入该说明，类对象可直接通过函数增删改查数据库数据
    objects = models.Manager()

    username = models.CharField('用户名', max_length=11, unique=True)
    password = models.CharField('密码', max_length=200)
    # 用户数据以下两条必须具有
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    update_time = models.DateTimeField('更新时间',auto_now=True)

    class Meta:
        # 数据库名
        # db_table = 'user_user'
        # 后台数据表命名
        verbose_name = '用户注册信息'
        verbose_name_plural = '用户注册信息'

    def __str__(self):
        return '用户 + %s' % self.username

class Note(models.Model):
    # 加入该说明，类对象可直接通过函数增删改查数据库数据
    objects = models.Manager()
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    is_active = models.BooleanField('激活', default=True)
    classify = models.CharField('分类', max_length=10, default='无')
    tag = models.CharField('标签', max_length=100, default='')
    secret = models.BooleanField('是否公开', default='False')

    # 添加外键User，即一个User对象对应多个Note对象
    uers = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        # 数据库名
        # db_table = 'user_note'
        # 后台数据表命名
        verbose_name = '用户生产数据'
        verbose_name_plural = '用户生产数据'


class Comments(models.Model):
    objects = models.Manager()
    name = models.CharField('用户名', max_length=11)
    text = models.TextField('评论内容')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    class Meta:
        # 数据库名
        # db_table = 'user_note'
        # 后台数据表命名
        verbose_name = '用户评论数据'
        verbose_name_plural = '用户评论数据'

class Logs(models.Model):
    objects = models.Manager()
    title = models.CharField('标题', max_length=100)
    content = models.TextField('详情')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    class Meta:
        # 数据库名
        # db_table = 'user_note'
        # 后台数据表命名
        verbose_name = '日志信息'
        verbose_name_plural = '日志信息'

class Zhengju(models.Model):
    objects = models.Manager()
    year = models.IntegerField('年份')
    content = models.TextField('证据内容')
    number = models.CharField('证据编号', max_length=6)
    hassorted = models.IntegerField('排序序号')

    class Meta:
        # 数据库名
        # db_table = 'user_note'
        # 后台数据表命名
        verbose_name = '证据列表'
        verbose_name_plural = '证据列表'


class Like(models.Model):
    objects = models.Manager()
    name = models.CharField('用户名', max_length=11)
    is_like = models.BooleanField('是否点赞', default=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    class Meta:
        # 数据库名
        # db_table = 'user_note'
        # 后台数据表命名
        verbose_name = '用户点赞数据'
        verbose_name_plural = '用户点赞数据'