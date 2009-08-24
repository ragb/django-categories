from django import forms
from django.db import transaction
from django.db.models import Q
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

from categories.models import Category

class CategoryChoiceField(forms.ModelChoiceField):
    """
    Field to select from a list of categories 
    
    Based on ``mptt.forms.TreeChoiceField`
    """

    def __init__(self, level_indicator=u'---', *args, **kwargs):
        self.level_indicator = level_indicator
        if 'queryset' in kwargs.keys():
            if kwargs['queryset'].model != Category:
                raise TypeError, "This field only accepts querysets of Categories"
        else:
            kwargs['queryset'] = Category.objects.all()
        super(CategoryChoiceField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return u'%s %s' % (self.level_indicator * obj.depth,
            smart_unicode(obj))

class CategoryMultipleChoiceField(forms.MultipleChoiceField):
    def __init__(self, level_indicator=u'---', *args, **kwargs):
        self.level_indicator = level_indicator
        if 'queryset' in kwargs.keys():
            if kwargs['queryset'].model != Category:
                raise TypeError, "This field only accepts querysets of categories"
        else:
            kwargs['queryset'] = Category.objects.all()
        super(CategoryMultipleChoiceField, self).__init__(*args, **kwargs)
    # the method is the same so use the same method
    label_from_instance = CategoryChoiceField.label_from_instance


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']

    parent_field = CategoryChoiceField(empty_label=_("Root Node"), required=False)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs.keys():
            instance = kwargs.get('instance')
            
            # set parent queryset to exclude descendants
            descendants = instance.get_descendants()
            qs = Category.objects.exclude(Q(pk__in=descendants.values('pk')) | Q(pk=instance.pk))
            self.fields['parent'].queryset = qs

    def save(self, commit=True):
        parent = self.cleaned_data['parent_field']
        if self.instance.pk is not None:
            super(CategoryModelForm, self).save(commit=Commit)
            self._update_parent(parent)
        else:
            self._create_node(parent)
            # We does not save the m2m callback so create a idiot one
            self.save_m2m = lambda : None

        if commit:
            transaction.commit_unless_managed()
        return self.instance

    def _create_node(self, parent):
        keys = ['name', 'description', 'slug']
        data = {}
        for key in keys:
            data[key] = self.cleaned_data[key]
        if parent is None: # reate a root node
            root = Category.get_first_root_node()
            if root:
                self.instance = root.add_sibling(pos='sorted-sibling', **data)
            else:
                self.instance = Category.add_root(**data)
        else:
            child = parent.get_first_child()
            if child:
                self.instance = child.add_sibling(pos='sorted-sibling', **data)
            else:
                self.instance = parent.add_child(**data)

    def _update_parent(self, parent):
        if self.instance.get_parent() == parent:
            return
        if parent is None: # transform this on a root node
            self.instance.move(Category.get_first_root_node(), pos='sorted-sibling')
        else:
            self.instance.move(parent, pos='sorted-child')
