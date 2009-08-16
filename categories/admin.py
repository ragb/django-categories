from django.contrib import admin
from categories.models import Category

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    prepopulated_fields = {'slug' : ['name']}

admin.site.register(Category, CategoryAdmin)
