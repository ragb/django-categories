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
        return self.filter(parent__isnull=True)


