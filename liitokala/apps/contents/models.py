from django.db import models

from model_utils import FieldTracker
import vinaigrette

from . import mixins


class Content(mixins.MultilingualSearchable):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    text = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to='liitokala/uploads', blank=True)

    _translatable_fields = ['title', 'text']
    _tracked_fields = _translatable_fields
    _tracker = FieldTracker(_tracked_fields)

    def __str__(self):
        return self.title

vinaigrette.register(Content, Content._translatable_fields)
