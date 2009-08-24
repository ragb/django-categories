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

__test__ = {"formtest": """


>>> from categories.models import Category
>>> from categories.forms import CategoryModelForm
>>> data = {'name' : 'c1', 'slug' : 'c1'}
>>> f = CategoryModelForm(data)
>>> f.is_valid()
True
>>> c1 = f.save()
>>> data = {'name' : 'c2', 'slug' : 'c2', 'parent_field' : c1.id}
>>> f = CategoryModelForm(data)
>>> f.is_valid()
True
>>> c2 = f.save()
>>> c2.get_parent() == c1
True
>>> data = {'name' : 'c3', 'slug' : 'c3', 'parent_field' : c1.id}
>>> f = CategoryModelForm(data)
>>> f.is_valid()
True
>>> c3 = f.save()
>>> data = {'name' : 'c3', 'slug' : 'c3', 'parent_field' : c2.id}
>>> f = CategoryModelForm(data, instance=c3)
>>> f.is_valid()
True
>>> c3_2 = f.save()
>>>
"""}




