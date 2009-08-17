from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.utils.translation import ugettext_lazy as _

#
# Managers
#

class CategoryManager(models.Manager):
    """ custom manager for categories """

    def get_top_categories(self):
        """
        Returns the top categories
        
        Top categories are all categories with no parent
        """
        return self.filter(parent__isnull=True)

    def get_for_object(self, obj):
        """ Returns all categories associated with the given object """
        ctype = ContentType.objects.get_for_model(obj)
        return self.filter(items__content_type_pk=ctype.pk,
            items__object_id=obj.pk)

    def get_for_model(self, model):
        """ Returns all categories associated with instances of the given model """
        ctype = ContentType.objects.get_for_model(model)
        return self.filter(items__content_type_pk=ctype.pk).distinct()


#
# models
#

class Category(models.Model):
    """ A category for items """
    name = models.CharField(_("name"), max_length=50,
        help_text=_("Name of the Category"))
    slug = models.SlugField(_("slug"), unique=True,
        help_text=_("Slug, normally used in URLs"))
    description = models.TextField(_("description"), help_text=_("Description of this category"))
    parent = models.ForeignKey('self', null=True, blank=True, related_name="subcategories",
        help_text=_("Parent category of this category, leave blank for a top category"))
    objects = CategoryManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __unicode__(self):
        return self.name

    def get_ancestors(self):
        """
        returns a list with the ancestors of this category
        
        the returned list iis ordered from the parent of this category to a root category
        """
        ancestors = []
        parent = self.parent
        while parent is not None:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors


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
