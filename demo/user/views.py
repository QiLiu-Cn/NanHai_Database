from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Avg, Max, Min, Count, Sum
from django.contrib import messages
from django.db.models import Q
from .models import User, Note, Comments, Like, Logs, Zhengju
import hashlib
from django.core.paginator import Paginator

# 检查登陆，在需要检查的函数前加入@check_login
def check_login(fn):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            # 检查cookies
            c_username = request.COOKIES.get('username')
            c_uid = request.COOKIES.get('uid')
            if not c_uid or not c_username:
                return HttpResponseRedirect('/user/login')
            else:
                # 回写至session
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return fn(request, *args, **kwargs)
    return wrap

# Create your views here.
def reg_view(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        # 获取用户输入的数据
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']

        # 两次输入密码是否一致
        if password_1 != password_2:
            message = '两次输入不一致'
            return render(request, 'user/register.html', locals())

        # 利用哈希算法加密密码
        m = hashlib.md5()
        m.update(password_1.encode())
        password_m = m.hexdigest()

        # 查询数据库。是否重名
        old_name = User.objects.filter(username=username)
        if old_name:
            message = '用户名已被注册'
            return render(request, 'user/register.html', locals())

        try:
            user = User.objects.create(username=username, password=password_m)
        except Exception as e:
            # 可能并发的问题
            print('create user error %s' %(e))
            message = '用户名已被注册'
            return render(request, 'user/register.html', locals())

        # 注册成功后免登陆一天，修改session的存储时间是一天
        request.session['username'] = username
        request.session['uid'] = user.id

        return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'GET':
        # 检查登陆状态，如果session或cookie里存有登录信息，显示“已登陆”
        if request.session.get('username') and request.session.get('uid'):
            # return HttpResponse('已登陆')
            return HttpResponseRedirect('/')

        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        if c_username and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            # return HttpResponse('已登陆')
            return HttpResponseRedirect('/')
        return render(request, 'user/login.html')

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print(e)
            message = '您的用户名或密码错误'
            return render(request, 'user/login.html', locals())

        # 利用哈希算法加密密码，获取密文比对数据库
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()

        if password_m != user.password:
            message = '您的用户名或密码错误'
            return render(request, 'user/login.html', locals())

        # 记录会话状态
        request.session['username'] = username
        request.session['uid'] = user.id

        resp = HttpResponseRedirect('/')

        # 如果选择记住，3天免登陆
        if 'memory' in request.POST:
            resp.set_cookie('username', username, 3600*24*3)
            resp.set_cookie('uid', user.id, 3600*24*3)

        return resp

# 退出登录，退出登陆前删去session信息和cookies信息
def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']

    resp = HttpResponseRedirect('/')

    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp
    # return HttpResponse('退出成功')

def delete_view(request):
    # 传入链接为/user/delete?id={{ note.id }}，问号后是传来的键值对
    id = request.GET.get('id')
    if not id:
        return HttpResponse('请求异常')
    try:
        message = '您是否确定删除？'
        note = Note.objects.get(id=id, is_active=True)
    except:
        print('delete error!')
        return HttpResponse('id is error!')
        # 伪删除
    note.is_active = False
    note.save()
    return HttpResponseRedirect('/user/home')

def artical(request):
    if request.method == 'GET':
        log_id = request.GET['log_id']
        ls = Logs.objects.filter(id=int(log_id))
        for n in ls:
            log = n
            print(log.content)
            break
        return render(request, 'user/artical.html', locals())

def logs(request):
    try:
        page = request.GET["page"]
        if page == '':
            page = 1
    except:
        page = 1
    ls = Logs.objects.all().order_by('-create_time')

    paginator = Paginator(ls, 10)
    page_obj = paginator.get_page(int(page))
    page_range = paginator.page_range
    all_page = page_range[-1]
    return render(request, 'user/home.html', locals())

# 加入检查登陆状态页面，如果没有登陆就跳转至登录页面
def add_note(request):
    if request.method == 'GET':
        # f = open(r'C:\Users\Administrator\Desktop\shixu.txt', 'rb')
        # s = f.readlines()
        # f.close()
        #
        # for sss in s:
        #     sss = sss.decode('utf-8').split('@@')
        #     year = int(sss[0])
        #     content = sss[1]
        #     number = sss[2]
        #     hassorted = int(sss[3].strip())
        #     Zhengju.objects.create(year=year, content=content, number=number, hassorted=hassorted)

        return render(request, 'user/add_note.html')
    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        # 写入数据库关闭
        Logs.objects.create(title=title, content=content)
        return HttpResponseRedirect('/user/home')

def search(request):
    flag = 1
    try:
        entity = request.GET['user_text']
    except:
        entity = ''
    try:
        fil_class = request.GET['fil_class']
    except:
        fil_class = ''
    try:
        page = request.GET["page"]
        if page == '':
            page = 1
    except:
        page = 1
    # 未传参
    if not fil_class and not entity:
        flag = 0
    # 关键词、分类、标签皆有
    elif entity and fil_class:
        zhengjus = Zhengju.objects.filter(Q(content__contains=entity), Q(year=int(fil_class))).order_by('hassorted')

        paginator = Paginator(zhengjus, 25)
        page_obj = paginator.get_page(int(page))
        page_range = paginator.page_range
        all_page = page_range[-1]

        count = len(zhengjus)
        everyyear = Zhengju.objects.values('year').filter(Q(content__contains=entity)).annotate(Count('id'))
        new = sorted(list(everyyear), key=lambda x: x['year'])
    # 仅有关键词
    else:
        zhengjus = Zhengju.objects.filter(Q(content__contains=entity)).order_by('hassorted')

        paginator = Paginator(zhengjus, 25)
        page_obj = paginator.get_page(int(page))
        page_range = paginator.page_range
        all_page = page_range[-1]

        count = len(zhengjus)
        # aggregate:聚合查询
        # annotate: 分组查询
        everyyear = Zhengju.objects.values('year').filter(Q(content__contains=entity)).annotate(Count('id'))
        new = sorted(list(everyyear), key=lambda x:x['year'])

    return render(request, 'user/community.html', locals())

