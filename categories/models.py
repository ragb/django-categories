from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.utils.translation import ugettext_lazy as _

import mptt

#
# Managers
#

class CategoryManager(models.Manager):
    """ custom manager for categories """

    def update_categories(self, obj, categories):
        """ updates the categories for the given object """
        ctype = ContentType.objects.get_for_model(obj)
        current_categorized_items = CategorizedItem.objects.filter(content_type=ctype, object_id=obj.id)
        
        # delete CategorizedItems not present in categories
        current_categorized_items.exclude(category__in=categories).delete()
        
        # Find what categories to add
        # FIXME: is there any optimized query for this?
        categories_to_add = self.exclude(items__in=current_categorized_items).filter(id__in=[c.id for c in categories])
        
        # create categorized items  for this
        for c in categories_to_add:
            CategorizedItem.objects.create(category=c, object=obj)

    def get_top_categories(self):
        """
        Returns the top categories
        
        Top categories are all categories with no parent
        """
        return Category.tree.root_nodes()

    def get_for_object(self, obj):
        """ Returns all categories associated with the given object """
        ctype = ContentType.objects.get_for_model(obj)
        return self.filter(items__content_type=ctype,
            items__object_id=obj.pk)

    def get_for_model(self, model):
        """ Returns all categories associated with instances of the given model """
        ctype = ContentType.objects.get_for_model(model)
        return Category.objects.filter(items__content_type=ctype).distinct()

    def get_tree_for_model(self, model, comulative=True):
        ctype = ContentType.objects.get_for_model(model)
        categories = Category.tree.all()
        Category.tree.add_related_count(categories, CategorizedItem, 'category', 'num_entries', comulative)
        categories = categories.filter(items__content_type=ctype)
        return categories

#
# models
#

class Category(models.Model):
    """ A category for items """
    name = models.CharField(_("name"), max_length=50, unique=True,
        help_text=_("Name of the Category"))
    slug = models.SlugField(_("slug"), unique=True,
        help_text=_("Slug, normally used in URLs"))
    description = models.TextField(_("description"), help_text=_("Description of this category"))
    parent = models.ForeignKey('self', null=True, blank=True, related_name="children",
        help_text=_("Parent category of this category, leave blank for a top category"))
    objects = CategoryManager()

    class Meta:
        ordering =  ['name']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __unicode__(self):
        return self.name

mptt.register(Category, order_insertion_by=['name'])

class CategorizedItem(models.Model):
    category = models.ForeignKey(Category, verbose_name=_("category"), related_name="items")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = (('category', 'content_type', 'object_id'),)
        verbose_name = _("Categorized item")
        verbose_name_plural = _("Categorized items")

    def __unicode__(self):
        return u'%s [%s]' % (self.object, self.category)
