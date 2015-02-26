# from django.contrib import admin
# from myApp.models import Category, Page

# # def PageAdmin():
# # class PageAdmin(admin.models):
# class PageAdmin(admin.ModelAdmin):
# 	list_dispaly = ('title','category', 'url')

# admin.site.register(Category)
# # admin.site.register(Page)
# admin.site.register(Page, PageAdmin)



from django.contrib import admin
from myApp.models import Category, Page, UserProfile

# def PageAdmin():
# class PageAdmin(admin.models):
class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url')

admin.site.register(Category)
# admin.site.register(Page)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)





# from django.contrib import admin
# from myApp.models import Category, Page#, UserProfile

# class PageAdmin(admin.ModelAdmin):
# 	list_display = ('title', 'category', 'url')

# admin.site.register(Category)
# admin.site.register(Page, PageAdmin)
# #admin.site.register(UserProfile)