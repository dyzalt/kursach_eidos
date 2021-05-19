from django.db import models


class Articles(models.Model):
    title = models.CharField('Title', max_length=250)
    text = models.TextField('Text')
    date = models.DateTimeField('Date', auto_now_add=True)
    image = models.ImageField('Image')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        permissions = (('can_add_article', 'User can add an article'),)
 