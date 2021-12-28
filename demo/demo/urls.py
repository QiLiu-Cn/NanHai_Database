from django.conf.urls import url 
from . import index_view,detail_view
from . import _404_view, overview_view
from . import relation_view
from django.urls import include, path
from django.contrib import admin
from . import question_answering

urlpatterns = [
    url(r'^$', index_view.index),
    url(r'^detail', detail_view.showdetail),
    url(r'^overview', overview_view.show_overview),
    url(r'^404',_404_view._404_),
    path('admin/', admin.site.urls),
    url(r'^search_entity',relation_view.search_entity),
    url(r'^search_relation',relation_view.search_in),
    url(r'^search_road',relation_view.search_relation),
    url(r'^qa', question_answering.question_answering),
    path('user/', include('user.urls')),
    url(r'^zhengminglidaxiao',relation_view.search_on),
    url(r'attribute_contribute',relation_view.search_attribute),
    url(r'^type_display',relation_view.proof),
    url(r'^prooflogic',relation_view.search_logic),

]
