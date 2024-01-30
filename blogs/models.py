from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    date = models.DateField("date published")
    content = models.TextField()


class Comments(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    content = models.CharField(max_length=2000)
    date = models.DateTimeField("date published")
