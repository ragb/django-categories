from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.utils.translation import ugettext_lazy as _

from treebeard.mp_tree import MP_Node

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

    def get_for_model(self, model):
        ctype = ContentType.objects.get_for_model(model)
        return self.filter(items__content_type=ctype).distinct()

    def get_for_object(self, obj):
        ctype = ContentType.objects.get_for_object(obj)
        return self.filter(items__content_type=ctype,
            object_id=obj.pk).distinct()

#
# models
#

class Category(MP_Node):
    """ A category for items """
    name = models.CharField(_("name"), max_length=50, unique=True,
        help_text=_("Name of the Category"))
    slug = models.SlugField(_("slug"), unique=True,
        help_text=_("Slug, normally used in URLs"))
    description = models.TextField(_("description"), blank=True, help_text=_("Description of this category"))
    objects = CategoryManager()
    node_order_by = 'name'

    class Meta:
        ordering =  ['name']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


    def __unicode__(self):
        return self.name


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
