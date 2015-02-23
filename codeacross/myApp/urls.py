from django.conf.urls import patterns, url
from myApp import views

urlpatterns = patterns('',
        url(r'^$',views.index, name = 'index'),
        # url(r'/about',views.about, name = 'about')
        # url(r'^about/',views.about, name = 'about'),
        url(r'^about/$',views.about, name = 'about'),
        # url(r'^category/category_name_url/', views.category, name = 'category'),
        url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),)  # New!        
        # url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),)    