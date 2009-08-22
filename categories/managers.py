""" Custom managers for categories """

from django.contrib.contenttypes.models import ContentType
from django.db import models

from categories.models import Category, CategorizedItem


class ModelCategoryManager(models.Manager):
    """
    manager for retrieving categories for a particular model
    """

    def get_query_set(self):
        return Category.objects.get_for_model(self.model)

    def get_top_categories(self):
        raise NotImplementedError


class CategoryDescriptor(object):
    """ Simple descriptor to add basic category get and set to models """

    def __get__(self, instance, owner):
        if instance is None:
            categories = ModelCategoryManager()
            categories.model = owner
        else:
            categories = Category.objects.get_for_object(instance)
        return categories

    def __set__(self, instance, value):
        Category.objects.update_category(instance, value)

    def __delete__(self, instance):
        Category.objects.update_categories(instance, [])
