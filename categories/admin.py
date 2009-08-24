from django.contrib import admin
from categories.models import Category

from categories.forms import CategoryModelForm

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryModelForm
    search_fields = ['name']
    prepopulated_fields = {'slug' : ['name']}


admin.site.register(Category, CategoryAdmin)
