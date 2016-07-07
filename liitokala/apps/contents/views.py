from django.shortcuts import render

from . import models


def content(request, slug):
    content = models.Content.objects.get(slug=slug)
    context = {
        'content': content,
    }
    return render(request, 'contents/content.html', context)
