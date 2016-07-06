from django.db import models

import vinaigrette


class Content(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    text = models.TextField()
    image = models.ImageField(upload_to='polytranspoc/uploads')

    def __str__(self):
        return self.title

vinaigrette.register(Content, ['title', 'text'])
