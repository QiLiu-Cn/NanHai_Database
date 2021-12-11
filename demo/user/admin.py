from django.contrib import admin
from .models import User, Note, Comments, Logs

# Register your models here.

class UserManager(admin.ModelAdmin):
    # 字段布局
    list_display = ['id', 'username', 'password', 'create_time']
    # 控制list_display中哪些字段是可链接至修改页面
    list_display_links = ['id']

class LogsManager(admin.ModelAdmin):
    list_display = ['id', 'title', 'create_time']
    list_display_links = ['id', 'title']
    search_fields = ['title']

class CommentsManager(admin.ModelAdmin):
    # 字段布局
    list_display = ['name', 'text', 'create_time']
    # 控制list_display中哪些字段是可链接至修改页面
    list_display_links = ['name']

class NoteManager(admin.ModelAdmin):
    # 字段布局
    list_display = ['id', 'title', 'classify', 'tag', 'uers_id', 'is_active']
    # 控制list_display中哪些字段是可链接至修改页面
    list_display_links = ['id']
    # 添加过滤器用于分类查询
    list_filter = ['is_active', 'classify']
    # 添加搜索框(模糊查询)
    search_fields = ['title', 'tag']
    # 添加可在列表页编辑的字段，属于list_display且与list_display_links互斥
    list_editable = ['is_active']

admin.site.register(User, UserManager)
admin.site.register(Note, NoteManager)
admin.site.register(Comments, CommentsManager)
admin.site.register(Logs, LogsManager)