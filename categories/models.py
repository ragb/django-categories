from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    """ A category for items """
    name = models.CharField(_("name"), max_length=50,
        help_text=_("Name of the Category"))
    slug = models.SlugField(_("slug"), unique=True,
        help_text=_("Slug, normally used in URLs"))
    description = models.TextField(_("description"), help_text=_("Description of this category"))
    parent = models.ForeignKey('self', null=True, blank=True, related_name="subcategories",
        help_text=_("Parent category of this category, leave blank for a top category"))

    class Meta:
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
