from django.contrib import admin


from bootest.models import BookInfo,HeroInfo
class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'pub_date']

# Register your models here.
admin.site.register(BookInfo, BookInfoAdmin)

# admin.site.register(BookInfo)
admin.site.register(HeroInfo)