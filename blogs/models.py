from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    date = models.DateTimeField("date published")
    content = models.CharField(max_length=2000)


class Comments(models.Model):
    author = models.CharField(max_length=200)
    content = models.CharField(max_length=2000)
    date = models.DateTimeField("date published")
