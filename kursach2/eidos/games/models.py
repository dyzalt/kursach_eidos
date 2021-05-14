from django.db import models

class Articles(models.Model):
    title = models.CharField('Title', max_length=50)
    text = models.TextField('Text')
    date = models.DateTimeField('Date')