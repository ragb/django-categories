from django.contrib import admin
from categories.models import Category

from categories.forms import CategoryModelForm

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    prepopulated_fields = {'slug' : ['name']}
    form = CategoryModelForm

admin.site.register(Category, CategoryAdmin)
