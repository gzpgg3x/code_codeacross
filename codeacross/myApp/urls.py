from django.conf.urls import patterns, url
from myApp import views

urlpatterns = patterns('',
        url(r'^$',views.index, name = 'index'),
        # url(r'/about',views.about, name = 'about')
        # url(r'^about/',views.about, name = 'about'),
        url(r'^about/$',views.about, name = 'about'),
        # url(r'^category/category_name_url/', views.category, name = 'category'),
        # url(r'^category/(?P<category_name_url>\w+)/add_category/$', views.add_category, name='add_category'),  
        url(r'^add_category/$', views.add_category, name='add_category'),
        # url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'), 
        url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'),      
        url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='user_login'),
        )  # New!

        # url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),)    