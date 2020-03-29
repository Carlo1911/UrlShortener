from django.db import models

# Create your models here.
class URLData(models.Model):
    URLID = models.CharField(max_length=1000)
    ShortURL = models.CharField(max_length=100)
    
    def __str__(self):
        return '{0.URLID}, {0.ShortUrl}'.format(self)