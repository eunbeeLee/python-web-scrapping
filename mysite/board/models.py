from django.db import models

# Create your models here.
class board(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField('date published')
    link = models.CharField(max_length=300)
    category = models.CharField(max_length=50)
