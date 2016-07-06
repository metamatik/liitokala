from django.contrib import admin

import vinaigrette

from . import models


class ContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(models.Content, ContentAdmin)
