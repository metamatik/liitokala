from django.conf import settings
from django.db import models
from django.utils import timezone, translation

from model_utils import FieldTracker


"""

Design notes
============

We want to execute a full-text search on the `_search_document` field.
It should contain the whole text upon which to search.

The `_build_search_document` method is responsible for returning this string
according to the specific behavior of the child class.

"""


class SearchableQuerySet(models.QuerySet):

    def search(self, query):
        return self.filter(_search_document__search=query)

    def to_reindex(self):
        return self.filter(_needs_reindexing=True)

    def up_to_date(self):
        return self.filter(_needs_reindexing=False)


class Searchable(models.Model):
    _search_document = models.TextField(blank=True)
    _last_reindexed = models.DateTimeField(blank=True, null=True)
    _needs_reindexing = models.BooleanField(default=True)

    objects = SearchableQuerySet.as_manager()

    _tracked_fields = []

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        dirty_fields = self._tracker.changed().keys()
        if set(dirty_fields).intersection(self._tracked_fields):
            self._needs_reindexing = True
        super().save(*args, **kwargs)

    def _build_search_document(self):
        return NotImplemented

    def reindex(self):
        now = timezone.now()
        search_document = self._build_search_document()
        if search_document != self._search_document:
            self._search_document = search_document
            self._last_reindexed = now
            self._needs_reindexing = False
            self.save()


class MultilingualSearchable(Searchable):

    class Meta:
        abstract = True

    _translatable_fields = []

    def _build_search_document(self):
        """ Build and return a concatenation of all the
        localized versions of the translatable fields. """

        chunks = []

        current_language = translation.get_language() or settings.LANGUAGE_CODE

        for language_code, _ in settings.LANGUAGES:
            translation.activate(language_code)
            for field_name in self._translatable_fields:
                chunks.append(getattr(self, field_name))

        translation.activate(current_language)

        return ' '.join(chunks)
