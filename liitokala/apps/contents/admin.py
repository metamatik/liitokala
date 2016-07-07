from django.contrib import admin

import vinaigrette

from . import models


class ContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'text',
                'notes',
                'image',
            )
        }),
        ('Search-related data', {
            'classes': ('collapse',),
            'fields': (
                '_needs_reindexing',
                '_last_reindexed',
                '_search_document',
            ),
        }),
    )

admin.site.register(models.Content, ContentAdmin)
