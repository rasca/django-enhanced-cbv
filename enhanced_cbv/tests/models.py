from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateField()


class Author(models.Model):
    name = models.CharField(max_length=255)

