from django import forms

from django.utils.encoding import smart_unicode

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
        fields = ['name', 'description', 'slug']

    parent = CategoryChoiceField()

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init(*args, **kwargs)
        if 'instance' in kwargs.keys():
            instance = kwargs.get('instnace')
            
            # set parent queryset to exclude descendants
            descendants = instance.get_descendants()
        qs = Category.objects.exclude(pk__in=descendants.values('pk'))
        self['parent'].queryset = qs


