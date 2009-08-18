"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """


>>> from categories.models import Category, CategorizedItem
>>> from django.contenttypes.models import ContentType
>>> c1 = Category.objects.create(name="c1", slug="c1")
>>> c2 = Category.objects.create(name="c2", slug="c2")
>>> Category.objects.update_categories(c1, Category.objects.all())
>>> ctype = ContentType.objects.get_for_model(Category)
>>> c1 in Category.objects.filter(items__object_id=c2.id, items__content_type=ctype)
True
>>> c1 in Category.objects.filter(items__object_id=c1.id, items__content_type=ctype)
True


"""}

