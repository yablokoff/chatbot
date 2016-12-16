from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Tweet(models.Model):
    id_str = models.CharField(max_length=100, unique=True)
    text = models.CharField(max_length=500, blank=True)
    created_at = models.CharField(max_length=100, blank=True)